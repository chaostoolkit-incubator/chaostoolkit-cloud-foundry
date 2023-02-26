# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from fixtures import config, responses, secrets

from chaoscf.probes import list_apps


@patch("chaoscf.probes.call_api", autospec=True)
def test_list_apps(call_api):
    call_api.return_value = responses.FakeResponse(
        status_code=200, text=None, json=lambda: responses.apps
    )

    apps = list_apps(config.config, secrets.secrets)
    assert apps["total_results"] == 1
