# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Configuration, Secrets

from chaoscf.api import call_api, get_app_by_name

__all__ = ["get_app_stats", "list_apps"]


def list_apps(configuration: Configuration,
              secrets: Secrets) -> Dict[str, Any]:
    """
    List all applications available to the authorized user.

    See https://apidocs.cloudfoundry.org/280/apps/list_all_apps.html to
    understand the content of the response.
    """
    return call_api("/v2/apps", configuration, secrets).json()


def get_app_stats(app_name: str, configuration: Configuration,
                  secrets: Secrets, org_name: str = None,
                  space_name: str = None) -> Dict[str, Any]:
    """
    Fetch the metrics of the given application.

    See https://apidocs.cloudfoundry.org/280/apps/get_detailed_stats_for_a_started_app.html
    for more information.
    """  # noqa: E501
    app = get_app_by_name(
        app_name, configuration, secrets, org_name=org_name,
        space_name=space_name)

    return call_api(
        "/v2/apps/{a}/stats".format(a=app["metadata"]["guid"]),
        configuration, secrets).json()


def get_app_summary(app_name: str, configuration: Configuration,
                    secrets: Secrets, org_name: str = None,
                    space_name: str = None) -> Dict[str, Any]:
    """
    Fetch the application summary.

    See https://apidocs.cloudfoundry.org/280/apps/get_app_summary.html
    for more information.
    """
    app = get_app_by_name(
        app_name, configuration, secrets, org_name=org_name,
        space_name=space_name)

    return call_api(
        "/v2/apps/{a}/summary".format(a=app["metadata"]["guid"]),
        configuration, secrets).json()
