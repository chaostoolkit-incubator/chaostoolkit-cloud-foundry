# -*- coding: utf-8 -*-
import argparse

from connection import create_connection_config

from chaoscf.actions import start_all_apps


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--org', dest='org_name', help='org name')
    return parser.parse_args()


def run(org_name: str):
    """
    Starts all given applications in an CF Org.
    """
    config, secrets = create_connection_config()
    start_all_apps(org_name, configuration=config, secrets=secrets)


if __name__ == '__main__':
    args = cli()
    run(args.org_name)
