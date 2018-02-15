# -*- coding: utf-8 -*-
import random
from typing import Any, Dict, List

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaoscf.api import call_api, get_app_by_name, get_app_routes_by_host, \
    get_app_instances, get_bind_by_name, get_routes_by_host

__all__ = ["delete_app", "remove_routes_from_app", "terminate_app_instance",
           "terminate_some_random_instance", "unbind_service_from_app",
           "unmap_route_from_app", "map_route_to_app"]


def delete_app(app_name: str, configuration: Configuration, secrets: Secrets,
               org_name: str = None, space_name: str = None):
    """
    Delete application.

    See https://apidocs.cloudfoundry.org/280/apps/delete_a_particular_app.html
    """
    app = get_app_by_name(
        app_name, configuration, secrets, org_name=org_name,
        space_name=space_name)

    path = "/v2/apps/{a}".format(a=app['metadata']['guid'])
    call_api(path, configuration, secrets, method="DELETE")


def remove_routes_from_app(app_name: str, route_host: str,
                           configuration: Configuration, secrets: Secrets,
                           org_name: str = None, space_name: str = None):
    """
    Remove routes from a given application.

    See
    https://apidocs.cloudfoundry.org/280/apps/remove_route_from_the_app.html
    """
    app = get_app_by_name(
        app_name, configuration, secrets, org_name=org_name,
        space_name=space_name)

    routes = get_app_routes_by_host(
        app_name, route_host, configuration, secrets, org_name=org_name,
        space_name=space_name)

    app_guid = app["metadata"]["guid"]
    for route in routes:
        route_guid = route["metadata"]["guid"]
        path = "/v2/apps/{a}/routes/{r}".format(a=app_guid, r=route_guid)
        call_api(path, configuration, secrets, method="DELETE")


def unmap_route_from_app(app_name: str, host_name: str,
                         configuration: Configuration, secrets: Secrets,
                         org_name: str = None, space_name: str = None):
    """
    Unmap a specific route from a given application.

    As Domains are deprecated in the Cloud Foundry API, they are not
    specified here.
    See
    https://apidocs.cloudfoundry.org/280/#domains--deprecated-
    See
    https://www.cloudfoundry.org/blog/coming-changes-app-manifest-simplification/

    See
    https://apidocs.cloudfoundry.org/280/apps/remove_route_from_the_app.html
    """
    app = get_app_by_name(
        app_name, configuration, secrets, org_name=org_name,
        space_name=space_name)

    routes_path = app["entity"]["routes_url"]
    routes = call_api(routes_path, configuration, secrets).json()

    for route in routes["resources"]:
        if route["entity"]["host"] == host_name:
            call_api(
                "{a}/{r}".format(
                    a=routes_path, r=route["metadata"]["guid"]),
                configuration, secrets, method="DELETE")


def map_route_to_app(app_name: str, host_name: str,
                     configuration: Configuration, secrets: Secrets,
                     org_name: str = None,
                     space_name: str = None) -> List[Dict[str, Any]]:
    """
    Map a specific route to a given application.

    As Domains are deprecated in the Cloud Foundry API, they are not
    specified here.
    See
    https://apidocs.cloudfoundry.org/280/#domains--deprecated-
    See
    https://www.cloudfoundry.org/blog/coming-changes-app-manifest-simplification/

    See
    https://apidocs.cloudfoundry.org/280/apps/remove_route_from_the_app.html
    """
    app = get_app_by_name(
        app_name, configuration, secrets, org_name=org_name,
        space_name=space_name)

    routes_for_host = get_routes_by_host(
        host_name, configuration, secrets, org_name=org_name)

    routes_path = app["entity"]["routes_url"]

    results = []
    for route in routes_for_host["resources"]:
        results.append(call_api(
            "{a}/{r}".format(
                a=routes_path, r=route["metadata"]["guid"]),
            configuration, secrets,
            method="PUT").json())
    return results


def terminate_app_instance(app_name: str, instance_index: int,
                           configuration: Configuration, secrets: Secrets,
                           org_name: str = None, space_name: str = None):
    """
    Terminate the application's instance at the given index.

    See
    https://apidocs.cloudfoundry.org/280/apps/terminate_the_running_app_instance_at_the_given_index.html
    """  # noqa: E501
    app = get_app_by_name(
        app_name, configuration, secrets, org_name=org_name,
        space_name=space_name)

    logger.debug("Terminating instance {i} of application {a}".format(
        i=instance_index, a=app_name))

    path = "/v2/apps/{a}/instances/{i}".format(
        a=app["metadata"]["guid"], i=instance_index)
    call_api(path, configuration, secrets, method="DELETE")


def terminate_some_random_instance(app_name: str, configuration: Configuration,
                                   secrets: Secrets, org_name: str = None,
                                   space_name: str = None):
    """
    Terminate a random application's instance.

    See
    https://apidocs.cloudfoundry.org/280/apps/terminate_the_running_app_instance_at_the_given_index.html
    """  # noqa: E501
    instances = get_app_instances(
        app_name, configuration, secrets, org_name=org_name,
        space_name=space_name)

    indices = [idx for idx in instances.keys()]
    index = random.choice(indices)
    terminate_app_instance(
        app_name, index, configuration, secrets, org_name, space_name)


def unbind_service_from_app(app_name: str, bind_name: str,
                            configuration: Configuration, secrets: Secrets,
                            org_name: str = None, space_name: str = None):
    """
    Unbind the service from the given application.

    See
    https://apidocs.cloudfoundry.org/280/service_bindings/delete_a_particular_service_binding.html
    """  # noqa: E501
    app = get_app_by_name(
        app_name, configuration, secrets, org_name=org_name,
        space_name=space_name)

    service_bind = get_bind_by_name(
        bind_name, configuration, secrets, org_name=org_name,
        space_name=space_name)

    logger.debug("Ubinding service {s} from application {a}".format(
        s=bind_name, a=app_name))

    path = "/v2/service_bindings/{s}".format(
        s=service_bind["metadata"]["guid"])
    call_api(path, configuration, secrets, method="DELETE")
