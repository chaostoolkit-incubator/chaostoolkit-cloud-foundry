# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch
from urllib.parse import urlencode

from chaoslib.exceptions import FailedActivity
from chaoscf.api import call_api, get_app_by_name, get_org_by_name, \
    get_space_by_name, get_routes_by_host, get_app_routes_by_host, \
    get_app_instances
import pytest
import requests_mock

from fixtures import config, responses, secrets


@patch('chaoscf.api.call_api', autospec=True)
def test_get_app_by_name_returns_the_app_with_exact_name(call_api):
    call_api.return_value = responses.FakeResponse(
        status_code=200, text=None, json=lambda: responses.apps)

    app = get_app_by_name("my-app", config.config, secrets.secrets)
    assert app["entity"]["name"] == "my-app"


@patch('chaoscf.api.call_api', autospec=True)
def test_get_app_by_name_expect_fullname(call_api):
    apps = responses.apps.copy()
    apps['total_results'] = 0
    apps['resources'] = []

    call_api.return_value = responses.FakeResponse(
        status_code=200, text=None, json=lambda: apps)

    with pytest.raises(FailedActivity) as ex:
        get_app_by_name("my-", config.config, secrets.secrets)


@patch('chaoscf.api.auth', autospec=True)
def test_get_app_by_name_and_org(auth):
    auth.return_value = responses.auth_response

    q = "q=name:my-app&q=organization_guid:{o}".format(
        o=responses.org["metadata"]["guid"])

    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?{q}".format(q=q), status_code=200,
            json=responses.apps, complete_qs=True)

        app = get_app_by_name(
            "my-app", config.config, secrets.secrets,
            org_guid=responses.org["metadata"]["guid"])
        assert app["entity"]["name"] == "my-app"


@patch('chaoscf.api.auth', autospec=True)
def test_get_app_by_name_and_space(auth):
    auth.return_value = responses.auth_response

    q = "q=name:my-app&q=space_guid:{s}".format(
        s=responses.space["metadata"]["guid"])

    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?{q}".format(q=q), status_code=200,
            json=responses.apps, complete_qs=True)

        app = get_app_by_name(
            "my-app", config.config, secrets.secrets,
            space_guid=responses.space["metadata"]["guid"])
        assert app["entity"]["name"] == "my-app"


@patch('chaoscf.api.auth', autospec=True)
def test_get_app_by_name_and_org_and_space(auth):
    auth.return_value = responses.auth_response

    q = "q=name:my-app&q=space_guid:{s}&q=organization_guid:{o}".format(
        s=responses.space["metadata"]["guid"],
        o=responses.org["metadata"]["guid"])

    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?{q}".format(q=q), status_code=200,
            json=responses.apps, complete_qs=True)

        app = get_app_by_name(
            "my-app", config.config, secrets.secrets,
            space_guid=responses.space["metadata"]["guid"],
            org_guid=responses.org["metadata"]["guid"])
        assert app["entity"]["name"] == "my-app"


@patch('chaoscf.api.auth', autospec=True)
def test_get_space_by_name_and_org(auth):
    auth.return_value = responses.auth_response

    q = "q=name:pcfdev-space&q=organization_guid:{o}".format(
        o=responses.org["metadata"]["guid"])

    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/spaces?{q}".format(q=q), status_code=200,
            json=responses.spaces, complete_qs=True)

        space = get_space_by_name(
            "pcfdev-space", config.config, secrets.secrets,
            org_guid=responses.org["metadata"]["guid"])
        assert space["entity"]["name"] == "pcfdev-space"


@patch('chaoscf.api.auth', autospec=True)
def test_get_org_by_name(auth):
    auth.return_value = responses.auth_response

    q = "q=name:pcfdev-org"

    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/organizations?{q}".format(q=q),
            status_code=200, json=responses.orgs, complete_qs=True)

        org = get_org_by_name(
            "pcfdev-org", config.config, secrets.secrets)
        assert org["entity"]["name"] == "pcfdev-org"


@patch('chaoscf.api.auth', autospec=True)
def test_get_routes_by_host(auth):
    auth.return_value = responses.auth_response
    q = "q=host:whatever"
    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/routes?{q}".format(q=q),
            status_code=200, json=responses.routes, complete_qs=True)

        routes = get_routes_by_host(
            "whatever", config.config, secrets.secrets)
        assert routes["total_results"] == 1


@patch('chaoscf.api.auth', autospec=True)
def test_get_routes_for_app_by_host(auth):
    auth.return_value = responses.auth_response
    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?q=name:my-app", status_code=200,
            json=responses.apps, complete_qs=True)

        m.get(
            "https://example.com/v2/routes?q=host:whatever",
            status_code=200, json=responses.routes, complete_qs=True)

        m.get(
            "https://example.com/v2/routes/{r}/apps?app_guid={a}".format(
                r=responses.route["metadata"]["guid"],
                a=responses.app["metadata"]["guid"]),
            status_code=200, json=responses.routes, complete_qs=True)

        routes = get_app_routes_by_host(
            "my-app", "whatever", config.config, secrets.secrets)
        assert len(routes) == 1


@patch('chaoscf.api.auth', autospec=True)
def test_get_app_instances(auth):
    auth.return_value = responses.auth_response
    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?q=name:my-app", status_code=200,
            json=responses.apps, complete_qs=True)

        m.get(
            "https://example.com/v2/apps/{a}/instances".format(
                a=responses.app["metadata"]["guid"]),
            status_code=200, json=responses.instances, complete_qs=True)

        instances = get_app_instances(
            "my-app", config.config, secrets.secrets)
        assert len(instances) == 1
