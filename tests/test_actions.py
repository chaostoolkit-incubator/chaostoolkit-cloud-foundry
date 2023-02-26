# -*- coding: utf-8 -*-
from unittest.mock import call, patch

import pytest
import requests_mock
from chaoslib.exceptions import FailedActivity
from fixtures import config, responses, secrets

import chaoscf
from chaoscf.actions import (
    delete_app,
    map_route_to_app,
    start_all_apps,
    start_app,
    stop_all_apps,
    stop_app,
    terminate_app_instance,
    terminate_some_random_instance,
    unbind_service_from_app,
    unmap_route_from_app,
)


def test_all_lists_the_actions_exposed():
    assert [
        "delete_app",
        "map_route_to_app",
        "remove_routes_from_app",
        "start_all_apps",
        "start_app",
        "stop_all_apps",
        "stop_app",
        "terminate_app_instance",
        "terminate_some_random_instance",
        "unbind_service_from_app",
        "unmap_route_from_app",
    ] == chaoscf.actions.__all__


@patch("chaoscf.actions.get_app_by_name", autospec=True)
@patch("chaoscf.actions.call_api", autospec=True)
def test_fail_to_delete_unknown_app(call_api, get_app_by_name):
    apps = responses.apps.copy()
    apps["total_results"] = 0
    apps["resources"] = []

    app_name = "my-app"
    get_app_by_name.side_effect = FailedActivity(
        "app '{a}' was not found".format(a=app_name)
    )
    call_api.return_value = responses.FakeResponse(status_code=200)

    with pytest.raises(FailedActivity) as exception:
        delete_app(app_name, config.config, secrets.secrets)

    assert "app 'my-app' was not found" in str(exception)


@patch("chaoscf.actions.get_app_by_name", autospec=True)
@patch("chaoscf.actions.call_api", autospec=True)
def test_delete_app(call_api, get_app_by_name):
    get_app_by_name.return_value = responses.app
    call_api.return_value = responses.FakeResponse(status_code=200)
    delete_app("my-app", config, secrets)


@patch("chaoscf.api.auth", autospec=True)
def test_terminate_app_instance(auth):
    auth.return_value = responses.auth_response
    app_guid = responses.app["metadata"]["guid"]
    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?q=name:my-app",
            status_code=200,
            json=responses.apps,
            complete_qs=True,
        )

        m.delete(
            "https://example.com/v2/apps/{a}/instances/0".format(a=app_guid),
            status_code=204,
        )

        terminate_app_instance("my-app", 0, config.config, secrets.secrets)


@patch("chaoscf.actions.random", autospec=True)
@patch("chaoscf.api.auth", autospec=True)
def test_terminate_random_app_instance(auth, rand):
    instances = responses.instances.copy()
    instances["1"] = instances["0"].copy()

    auth.return_value = responses.auth_response
    rand.choice.return_value = "1"

    app_guid = responses.app["metadata"]["guid"]

    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?q=name:my-app",
            status_code=200,
            json=responses.apps,
            complete_qs=True,
        )

        m.get(
            "https://example.com/v2/apps/{a}/instances".format(a=app_guid),
            status_code=200,
            json=instances,
            complete_qs=True,
        )

        m.delete(
            "https://example.com/v2/apps/{a}/instances/1".format(a=app_guid),
            status_code=204,
        )

        terminate_some_random_instance("my-app", config.config, secrets.secrets)


@patch("chaoscf.api.auth", autospec=True)
def test_unbind_service_from_app(auth):
    auth.return_value = responses.auth_response
    bind_guid = responses.bind["metadata"]["guid"]
    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?q=name:my-app",
            status_code=200,
            json=responses.apps,
            complete_qs=True,
        )

        m.get(
            "https://example.com/v2/apps/"
            + responses.app["metadata"]["guid"]
            + "/service_bindings",
            status_code=200,
            json=responses.binds,
            complete_qs=True,
        )

        m.delete(
            "https://example.com/v2/service_bindings/{s}".format(s=bind_guid),
            status_code=204,
        )

        unbind_service_from_app("my-app", "my-bind", config.config, secrets.secrets)


@patch("chaoscf.api.auth", autospec=True)
def test_unmap_route_from_app(auth):
    auth.return_value = responses.auth_response
    route_guid = responses.route["metadata"]["guid"]
    app_guid = responses.app["metadata"]["guid"]
    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?q=name:my-app",
            status_code=200,
            json=responses.apps,
            complete_qs=True,
        )

        m.get(
            "https://example.com/v2/apps/{app}/routes".format(app=app_guid),
            status_code=200,
            json=responses.routes,
            complete_qs=True,
        )

        m.delete(
            "https://example.com/v2/apps/{app}/routes/{s}".format(
                app=app_guid, s=route_guid
            ),
            status_code=204,
        )

        unmap_route_from_app("my-app", "whatever", config.config, secrets.secrets)


@patch("chaoscf.api.auth", autospec=True)
def test_map_route_to_app(auth):
    auth.return_value = responses.auth_response
    route_guid = responses.route["metadata"]["guid"]
    app_guid = responses.app["metadata"]["guid"]
    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?q=name:my-app",
            status_code=200,
            json=responses.apps,
            complete_qs=True,
        )

        m.get(
            "https://example.com/v2/routes?q=host:whatever".format(app=app_guid),
            status_code=200,
            json=responses.routes,
            complete_qs=True,
        )

        m.put(
            "https://example.com/v2/apps/{app}/routes/{s}".format(
                app=app_guid, s=route_guid
            ),
            status_code=201,
            json=responses.route,
        )

        map_route_to_app("my-app", "whatever", config.config, secrets.secrets)


@patch("chaoscf.actions.get_app_by_name", autospec=True)
@patch("chaoscf.api.auth", autospec=True)
def test_stop_app(auth, get_app_by_name):
    auth.return_value = responses.auth_response
    app = responses.app
    get_app_by_name.return_value = app
    with requests_mock.mock() as mock:
        update_url = "https://example.com/v2/apps/%s" % app["metadata"]["guid"]
        mock.put(update_url, status_code=201, json=app)

        stop_app("my-app", config.config, secrets.secrets)

    assert mock.call_count == 1


@patch("chaoscf.actions.start_app", autospec=True)
@patch("chaoscf.actions.get_apps_for_org", autospec=True, return_value=responses.apps)
def test_start_all_apps(get_apps_for_org, start_app):
    org_name = "CF_ORG_NAME"
    start_all_apps(org_name, config.config, secrets.secrets)

    get_apps_for_org.assert_has_calls([call(org_name, config.config, secrets.secrets)])
    start_app.assert_has_calls(
        [
            call(
                app["entity"]["name"], config.config, secrets.secrets, org_name=org_name
            )
            for app in responses.apps["resources"]
        ]
    )


@patch("chaoscf.actions.stop_app", autospec=True)
@patch("chaoscf.actions.get_apps_for_org", autospec=True, return_value=responses.apps)
def test_stop_all_apps(get_apps_for_org, stop_app):
    org_name = "CF_ORG_NAME"
    stop_all_apps(org_name, config.config, secrets.secrets)

    get_apps_for_org.assert_has_calls([call(org_name, config.config, secrets.secrets)])
    stop_app.assert_has_calls(
        [
            call(
                app["entity"]["name"], config.config, secrets.secrets, org_name=org_name
            )
            for app in responses.apps["resources"]
        ]
    )


@patch("chaoscf.actions.get_app_by_name", autospec=True)
@patch("chaoscf.api.auth", autospec=True)
def test_start_app(auth, get_app_by_name):
    auth.return_value = responses.auth_response
    app = responses.app
    get_app_by_name.return_value = app
    with requests_mock.mock() as mock:
        update_url = "https://example.com/v2/apps/%s" % app["metadata"]["guid"]
        mock.put(update_url, status_code=201, json=app)

        start_app("my-app", config.config, secrets.secrets)

    assert mock.call_count == 1
