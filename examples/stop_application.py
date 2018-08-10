# -*- coding: utf-8 -*-
import argparse

from connection import create_connection_config

from chaoscf.actions import stop_app


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', dest='app_name', help='application name')
    parser.add_argument('--org', dest='org_name', help='org name')
    parser.add_argument('--space', dest='space_name', help='space name')
    return parser.parse_args()


def run(app_name: str, org_name: str = None,
        space_name: str = None):
    """
    Stop a given application. The org and space are not required arguments.
    """
    config, secrets = create_connection_config()
    stop_app(app_name, configuration=config, secrets=secrets, org_name=org_name, space_name=space_name)


if __name__ == '__main__':
    args = cli()
    run(args.app_name, args.org_name, args.space_name)
