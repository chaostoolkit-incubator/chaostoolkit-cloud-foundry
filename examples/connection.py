# -*- coding: utf-8 -*-
import json
import os
import os.path
from typing import Any, Dict, Tuple

from chaoslib.types import Configuration, Discovery, DiscoveredSystemInfo, \
    Secrets
from logzero import logger
import requests
import urllib3

urllib3.disable_warnings()

__all__ = ["create_connection_config"]


def create_connection_config() -> Tuple[Configuration, Secrets]:
    """
    Create a configuration and secrets payload suitable for chaostoolkit from
    the local config file.
    """
    cf_local_config = os.path.expanduser("~/.cf/config.json")
    if not os.path.exists(cf_local_config):
        logger.warn(
            "Could not locate a cloud coundry config file at '{s}'.\n"
            "Make sure to run `cf login`".format(s=cf_local_config))
        return

    configuration = {}
    secrets = {}
    with open(cf_local_config) as f:
        cf_conf = json.loads(f.read())
        if "AccessToken" not in cf_conf:
            logger.warn(
                "'{s}' is missing an access token, please run `cf login` "
                "and re-run the discovery command".format(
                    s=cf_local_config))
            return

        token_type, token = cf_conf["AccessToken"].split(" ", 1)
        secrets["cf_token_type"] = token_type
        secrets["cf_access_token"] = token
        configuration["cf_verify_ssl"] = not cf_conf["SSLDisabled"]
        configuration["cf_api_url"] = cf_conf["Target"]
    
    return configuration, secrets
