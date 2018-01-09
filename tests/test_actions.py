# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from chaoscf.actions import delete_app, terminate_app_instance, \
    terminate_some_random_instance
from chaoslib.exceptions import FailedActivity
import pytest
import requests_mock

from fixtures import config, responses, secrets


@patch('chaoscf.actions.call_api', autospec=True)
def test_fail_to_delete_unknwon_app(call_api):
    apps = responses.apps.copy()
    apps['resources'] = []

    # first call from get_app_by_name, second from delete_app
    call_api.return_value = [
        responses.FakeResponse(status_code=200, json = lambda: apps),
        responses.FakeResponse(status_code=200)
    ]

    with pytest.raises(FailedActivity) as ex:
        delete_app("my-app", config.config, secrets.secrets)


@patch('chaoscf.actions.get_app_by_name', autospec=True)
@patch('chaoscf.actions.call_api', autospec=True)
def test_delete_app(call_api, get_app_by_name):
    get_app_by_name.return_value = responses.app
    call_api.return_value = responses.FakeResponse(status_code=200)
    delete_app("my-app", config, secrets)


@patch('chaoscf.api.auth', autospec=True)
def test_terminate_app_instance(auth):
    auth.return_value = responses.auth_response
    app_guid = responses.app["metadata"]["guid"]
    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?q=name:my-app", status_code=200,
            json=responses.apps, complete_qs=True)

        m.delete(
            "https://example.com/v2/apps/{a}/instances/0".format(a=app_guid),
            status_code=204)

        terminate_app_instance("my-app", 0, config.config, secrets.secrets)


@patch('chaoscf.actions.random', autospec=True)
@patch('chaoscf.api.auth', autospec=True)
def test_terminate_random_app_instance(auth, rand):
    instances = responses.instances.copy()
    instances["1"] = instances["0"].copy()

    auth.return_value = responses.auth_response
    rand.choice.return_value = "1"

    app_guid = responses.app["metadata"]["guid"]

    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/apps?q=name:my-app", status_code=200,
            json=responses.apps, complete_qs=True)

        m.get(
            "https://example.com/v2/apps/{a}/instances".format(a=app_guid),
            status_code=200, json=instances, complete_qs=True)

        m.delete(
            "https://example.com/v2/apps/{a}/instances/1".format(a=app_guid),
            status_code=204)

        terminate_some_random_instance(
            "my-app", config.config, secrets.secrets)
