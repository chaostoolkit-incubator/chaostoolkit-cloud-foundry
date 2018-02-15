# -*- coding: utf-8 -*-
import argparse

from chaoscf.actions import unmap_route_from_app

from connection import create_connection_config


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', dest='app_name', help='application name')
    parser.add_argument('--hostname', dest='host_name', help='host name')
    parser.add_argument('--org', dest='org_name', help='org name')
    parser.add_argument('--space', dest='space_name', help='space name')
    return parser.parse_args()


def run(app_name: str, host_name: str, org_name: str=None,
        space_name: str=None):
    """
    Unmap a route from a given application. The org and space are not
    required arguments.
    """
    config, secrets = create_connection_config()
    unmap_route_from_app(
        app_name, host_name, configuration=config, secrets=secrets,
        org_name=org_name, space_name=space_name)


if __name__ == '__main__':
    args = cli()
    run(args.app_name, args.host_name, args.org_name, args.space_name)