# -*- coding: utf-8 -*-
import json
import os
import os.path
from typing import Any, Dict, List

from chaoslib.discovery.discover import discover_actions, discover_probes, \
    initialize_discovery_result
from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Discovery, DiscoveredActivities, \
    Secrets
from logzero import logger
from oauthlib.oauth2 import LegacyApplicationClient
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
import requests
from requests_oauthlib import OAuth2Session
import urllib3

urllib3.disable_warnings()

__version__ = '0.5.0'
__all__ = ["__version__", "auth", "discover"]


def auth(configuration: Configuration, secrets: Secrets) -> Dict[str, str]:
    """
    Authenticate with the Cloud Foundry API endpoint.

    The `configuration` mapping must include `"api_url"` key associated to the
    URL of the API server, for example: `"https://api.local.pcfdev.io"`.

    When testing against a secured endpoint exposing self-signed certificate,
    you should set `"verify_ssl"` to `True`.

    The `secrets` mapping must contain:

    `"username"`: the user to authenticate with
    `"password"`: the user's password
    `"client_id"` the client id to authenticate with, defaults to `"cf"`
    `"client_secret"`: the client's secret, defaults to `""`

    Returns a mapping with the `access_token` and `refresh_token` keys as per
    http://docs.cloudfoundry.org/api/uaa/version/4.8.0/index.html#password-grant
    """

    api_url = configuration.get("cf_api_url")
    verify_ssl = configuration.get("cf_verify_ssl", True)

    username = secrets.get("cf_username")
    password = secrets.get("cf_password")
    client_id = secrets.get("cf_client_id", "cf")
    client_secret = secrets.get("cf_client_secret", "")

    logger.debug(
        "Querying a new access token for client '{c}'".format(c=client_id))
    return get_tokens(api_url, username, password, client_id, client_secret,
                      verify_ssl)


def get_tokens(api_url: str, username: str, password: str,
               client_id: str = "cf", client_secret: str = "",
               verify_ssl: bool = True) -> Dict[str, str]:
    """
    Private function that authorizes against the UAA OAuth2 endpoint.
    """
    info_url = "{u}/v2/info".format(u=api_url)
    r = requests.get(info_url, verify=verify_ssl)
    if r.status_code != 200:
        logger.debug("failed to fetch Cloud Foundry API info from "
                     "'{u}': {c} => {s}".format(
                         u=info_url, c=r.status_code, s=r.text))
        raise FailedActivity("failed to retrieve Cloud Foundry information, "
                             "cannot proceed further")

    info = r.json()
    authorization_endpoint = info["authorization_endpoint"]
    auth_url = "{u}/oauth/token".format(u=authorization_endpoint)
    client = LegacyApplicationClient(username, password=password)
    s = OAuth2Session(client=client)
    try:
        r = s.fetch_token(auth_url, verify=verify_ssl, username=username,
                          password=password, auth=(client_id, client_secret))
    except OAuth2Error as x:
        logger.debug("failed to auth with the Cloud Foundry API at "
                     "{u}".format(u=auth_url), exc_info=x)
        raise FailedActivity("failed to auth against Cloud Foundry, "
                             "cannot proceed further")

    return r


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Cloud Foundry capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-cloud-foundry")

    discovery = initialize_discovery_result(
        "chaostoolkit-cloud-foundry", __version__, "cloud-foundry")
    discovery["activities"].extend(load_exported_activities())
    return discovery


###############################################################################
# Private functions
###############################################################################
def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_actions("chaoscf.actions"))
    activities.extend(discover_probes("chaoscf.probes"))
    return activities
