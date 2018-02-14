# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger
import requests

from chaoscf import auth

__all__ = ['call_api', 'get_app_by_name', 'get_org_by_name',
           'get_space_by_name', 'get_app_instances', 'get_app_routes_by_host',
           'get_routes_by_host', 'get_bind_by_name']


def call_api(path: str, configuration: Configuration,
             secrets: Secrets, query: Dict[str, Any] = None,
             data: Dict[str, Any] = None, method: str = "GET",
             headers: Dict[str, str] = None) -> requests.Response:
    """
    Perform a Cloud Foundry API call and return the full response to the
    caller.
    """
    if "cf_access_token" not in secrets:
        tokens = auth(configuration, secrets)
    else:
        tokens = {
            "token_type": secrets.get("cf_token_type", "bearer"),
            "access_token": secrets.get("cf_access_token")
        }

    h = {
        "Accept": "application/json",
        "Authorization": "{a} {t}".format(
            a=tokens["token_type"], t=tokens["access_token"])
    }

    if headers:
        h.update(h)

    verify_ssl = configuration.get("cf_verify_ssl", True)
    url = "{u}{p}".format(u=configuration["cf_api_url"], p=path)
    r = requests.request(
        method, url, params=query, data=data, verify=verify_ssl, headers=h)

    request_id = r.headers.get("X-VCAP-Request-ID")
    logger.debug("Request ID: {i}".format(i=request_id))

    if r.status_code > 399:
        raise FailedActivity("failed to call '{u}': {c} => {s}".format(
            u=url, c=r.status_code, s=r.text))

    return r


def get_org_by_name(org_name: str, configuration: Configuration,
                    secrets: Secrets) -> Dict[str, Any]:
    """
    Get the organization with the given name.
    """
    orgs = call_api(
        "/v2/organizations", configuration, secrets, query={
            "q": "name:{o}".format(o=org_name)}).json()

    if not orgs['resources']:
        raise FailedActivity("org '{o}' was not found".format(o=org_name))

    return orgs['resources'][0]


def get_space_by_name(space_name: str, configuration: Configuration,
                      secrets: Secrets, org_name: str = None,
                      org_guid=None) -> Dict[str, Any]:
    """
    Get the space with the given name.

    You may restrict the search by organization by providing the
    various according parameters. When passing the name, the function performs
    a lookup for the org to fetch its GUID.
    """
    if not org_guid and org_name:
        org = get_org_by_name(org_name, configuration, secrets)
        org_guid = org['metadata']['guid']

    query = ["name:{s}".format(s=space_name)]
    if org_guid:
        query.append("organization_guid:{o}".format(o=org_guid))

    spaces = call_api(
        "/v2/spaces", configuration, secrets, query={"q": query}).json()

    if not spaces['total_results']:
        raise FailedActivity("space '{s}' was not found".format(s=space_name))

    return spaces['resources'][0]


def _get_filter_query(configuration: Configuration,
                      secrets: Secrets, space_name: str = None,
                      space_guid: str = None, org_name: str = None,
                      org_guid: str = None) -> List[str]:
    if org_guid is None and org_name:
        org = get_org_by_name(org_name, configuration, secrets)
        org_guid = org['metadata']['guid']

    if space_guid is None and space_name:
        space = get_space_by_name(
            space_name, configuration, secrets, org_name=org_name)
        space_guid = space['metadata']['guid']

    query = []
    if org_guid:
        query.append("organization_guid:{o}".format(o=org_guid))
    if space_guid:
        query.append("space_guid:{s}".format(s=space_guid))

    return query


def get_app_by_name(app_name: str, configuration: Configuration,
                    secrets: Secrets, space_name: str = None,
                    space_guid: str = None, org_name: str = None,
                    org_guid: str = None) -> Dict[str, Any]:
    """
    Get the application with the given name.

    You may restrict the search by organization and/or space by providing the
    various according parameters. When passing the names, the function performs
    a lookup for each of them to fetch their GUID.

    See https://apidocs.cloudfoundry.org/280/apps/list_all_apps.html
    """
    q = _get_filter_query(
        configuration, secrets, space_name, space_guid, org_name, org_guid)
    q.append("name:{n}".format(n=app_name))

    apps = call_api(
        "/v2/apps", configuration, secrets, query={"q": q}).json()

    if not apps['total_results']:
        raise FailedActivity("app '{a}' was not found".format(a=app_name))

    return apps['resources'][0]


def get_routes_by_host(route_host: str, configuration: Configuration,
                       secrets: Secrets, org_name: str = None,
                       org_guid: str = None) -> Dict[str, Any]:
    """
    Get all routes with given host.

    See https://apidocs.cloudfoundry.org/280/routes/list_all_routes.html
    """
    q = _get_filter_query(
        configuration, secrets, org_name=org_name, org_guid=org_guid)
    q.append("host:{h}".format(h=route_host))

    routes = call_api(
        "/v2/routes", configuration, secrets, query={"q": q}).json()

    if not routes['total_results']:
        raise FailedActivity("route with '{h}' was not found".format(
            h=route_host))

    return routes


def get_app_routes_by_host(app_name: str, route_host: str,
                           configuration: Configuration, secrets: Secrets,
                           space_name: str = None, space_guid: str = None,
                           org_name: str = None,
                           org_guid: str = None) -> List[Dict[str, Any]]:
    """
    Get all routes associated with the provided app and the given host.

    See https://apidocs.cloudfoundry.org/280/routes/list_all_routes.html
    """
    routes = get_routes_by_host(
        route_host, configuration, secrets, org_name, org_guid)

    app = get_app_by_name(
        app_name, configuration, secrets, space_name, space_guid, org_name,
        org_guid)

    result = []
    for route in routes['resources']:
        q = _get_filter_query(
            configuration, secrets, space_name, space_guid, org_name, org_guid)

        route = call_api(
            route["entity"]["apps_url"], configuration, secrets,
            query={"q": q, "app_guid": app["metadata"]["guid"]}
        ).json()

        if route["total_results"]:
            result.append(route)

    if not result:
        raise FailedActivity(
            "no routes with host '{h}' was found for app '{a}'".format(
                a=app_name, h=route_host))

    return result


def get_app_instances(app_name: str,  configuration: Configuration,
                      secrets: Secrets, space_name: str = None,
                      space_guid: str = None, org_name: str = None,
                      org_guid: str = None) -> Dict[str, Dict[str, Any]]:
    """
    Get all the instances of a started application.

    See https://apidocs.cloudfoundry.org/280/apps/get_the_instance_information_for_a_started_app.html
    """  # noqa: E501
    app = get_app_by_name(
        app_name, configuration, secrets, space_name, space_guid, org_name,
        org_guid)

    instances = call_api(
        "/v2/apps/{a}/instances".format(a=app["metadata"]["guid"]),
        configuration, secrets).json()

    if not instances:
        raise FailedActivity("app '{a}' has no instances".format(
            a=app_name))

    return instances


def get_bind_by_name(bind_name: str, configuration: Configuration,
                     secrets: Secrets, space_name: str = None,
                     space_guid: str = None, org_name: str = None,
                     org_guid: str = None) -> Dict[str, Any]:
    """
    Get the service bind with the given name.

    You may restrict the search by organization and/or space by providing the
    various according parameters. When passing the names, the function performs
    a lookup for each of them to fetch their GUID.

    See https://apidocs.cloudfoundry.org/280/apps/list_all_apps.html
    """
    q = _get_filter_query(
        configuration, secrets, space_name, space_guid, org_name, org_guid)
    q.append("name:{n}".format(n=bind_name))

    binds = call_api(
        "/v2/service_bindings", configuration, secrets, query={"q": q}).json()

    if not binds['total_results']:
        raise FailedActivity("bind '{a}' was not found".format(a=bind_name))

    return binds['resources'][0]
