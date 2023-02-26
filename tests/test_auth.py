# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

import pytest
import requests_mock
from chaoslib.exceptions import FailedActivity
from fixtures import config, responses, secrets
from oauthlib.oauth2.rfc6749.errors import OAuth2Error

from chaoscf import auth


def test_failed_fetching_api_endpoint_info():
    with requests_mock.mock() as m:
        m.get("https://example.com/v2/info", status_code=400)

        with pytest.raises(FailedActivity) as ex:
            auth(config.config, secrets.secrets)
        assert "failed to retrieve Cloud Foundry information" in str(ex)


@patch("chaoscf.OAuth2Session", autospec=True)
def test_failed_authenticating(SessionClass):
    s = SessionClass()
    s.fetch_token.side_effect = OAuth2Error

    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/info", status_code=200, json=responses.info_response
        )

        with pytest.raises(FailedActivity) as ex:
            auth(config.config, secrets.secrets)
        assert "failed to auth against Cloud Foundry" in str(ex)


@patch("chaoscf.OAuth2Session", autospec=True)
def test_authenticate(SessionClass):
    s = SessionClass()
    s.fetch_token.return_value = responses.auth_response

    with requests_mock.mock() as m:
        m.get(
            "https://example.com/v2/info", status_code=200, json=responses.info_response
        )

        tokens = auth(config.config, secrets.secrets)
        assert tokens["access_token"] == "my-token"
