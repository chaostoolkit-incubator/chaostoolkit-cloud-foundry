# -*- coding: utf-8 -*-
from typing import Any, Callable


class FakeResponse:
    def __init__(self, status_code: int = 200, text: str = None,
                 json: Any = None):
        self.status_code = status_code
        self.text = text
        self.json = json


space_name = "my-space"
org_name = "my-org"

info_response = {
    "authorization_endpoint": "https://uaa.example.com"
}

auth_response = {
    'access_token': 'my-token',
    'token_type': 'bearer',
    'refresh_token': 'refresh-token',
    'expires_in': 599,
    'scope': [
        'network.write',
        'cloud_controller.admin',
        'routing.router_groups.read',
        'cloud_controller.write',
        'network.admin',
        'doppler.firehose',
        'openid',
        'routing.router_groups.write',
        'scim.read', 'uaa.user',
        'cloud_controller.read',
        'password.write',
        'scim.write'
    ],
    'jti': '175fd6b6cb25427b814e2b24c91c739a',
    'expires_at': 1515427259.7878928
}

app = {
    'metadata': {
        'guid': 'a8f47fc8-0d26-4acb-a944-6ae45ed27abe',
        'url': '/v2/apps/a8f47fc8-0d26-4acb-a944-6ae45ed27abe',
        'created_at': '2018-01-04T14:35:55Z',
        'updated_at': '2018-01-08T12:15:31Z'
    },
    'entity': {
        'name': 'my-app',
        'production': False,
        'space_guid': 'dd875b8b-2a1a-4342-80ee-50539c2b07eb',
        'stack_guid': '4cb77e3e-dfcd-486a-83bb-0f2b8b8db622',
        'buildpack': 'nodejs_buildpack',
        'detected_buildpack': '',
        'detected_buildpack_guid': '36d282b5-2f32-45b4-a168-574fd126523e',
        'events_url': '/v2/apps/a8f47fc8-0d26-4acb-a944-6ae45ed27abe/events',
        'service_bindings_url': '/v2/apps/a8f47fc8-0d26-4acb-a944-6ae45ed27abe/service_bindings',
        'route_mappings_url': '/v2/apps/a8f47fc8-0d26-4acb-a944-6ae45ed27abe/route_mappings'
    }
}

apps = {
    'total_results': 1,
    'total_pages': 1,
    'prev_url': None,
    'next_url': None,
    'resources': [app]
}

space = {
    'metadata': {
        'guid': 'd7338989-6ae6-44dc-a29a-d6cfe66d71d5',
        'url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5',
        'created_at': '2018-01-04T14:35:28Z',
        'updated_at': '2018-01-04T14:35:28Z'
    },
    'entity': {
        'name': 'pcfdev-space',
        'organization_guid': '1e4bbba5-e6fa-4187-a664-4c652f0a83e5',
        'space_quota_definition_guid': None,
        'isolation_segment_guid': None,
        'allow_ssh': True,
        'organization_url': '/v2/organizations/1e4bbba5-e6fa-4187-a664-4c652f0a83e5',
        'developers_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5/developers',
        'managers_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5/managers',
        'auditors_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5/auditors',
        'apps_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5/apps',
        'routes_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5/routes',
        'domains_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5/domains',
        'service_instances_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5/service_instances',
        'app_events_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5/app_events',
        'events_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5/events',
        'security_groups_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5/security_groups',
        'staging_security_groups_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5/staging_security_groups'
    }
}

spaces = {
    'total_results': 1,
    'total_pages': 1,
    'prev_url': None,
    'next_url': None,
    'resources': [space]
}

org = {
    'metadata': {
        'guid': '1e4bbba5-e6fa-4187-a664-4c652f0a83e5',
        'url': '/v2/organizations/1e4bbba5-e6fa-4187-a664-4c652f0a83e5',
        'created_at': '2018-01-04T14:27:56Z',
        'updated_at': '2018-01-04T14:27:56Z'
    },
    'entity': {
        'name': 'pcfdev-org',
        'billing_enabled': False,
        'quota_definition_guid': '9fbbb4c1-05de-4c0f-9f78-17d6bcc29ca1',
        'status': 'active',
        'default_isolation_segment_guid': None,
        'quota_definition_url': '/v2/quota_definitions/9fbbb4c1-05de-4c0f-9f78-17d6bcc29ca1',
        'spaces_url': '/v2/organizations/1e4bbba5-e6fa-4187-a664-4c652f0a83e5/spaces',
        'domains_url': '/v2/organizations/1e4bbba5-e6fa-4187-a664-4c652f0a83e5/domains',
        'private_domains_url': '/v2/organizations/1e4bbba5-e6fa-4187-a664-4c652f0a83e5/private_domains',
        'users_url': '/v2/organizations/1e4bbba5-e6fa-4187-a664-4c652f0a83e5/users',
        'managers_url': '/v2/organizations/1e4bbba5-e6fa-4187-a664-4c652f0a83e5/managers',
        'billing_managers_url': '/v2/organizations/1e4bbba5-e6fa-4187-a664-4c652f0a83e5/billing_managers',
        'auditors_url': '/v2/organizations/1e4bbba5-e6fa-4187-a664-4c652f0a83e5/auditors',
        'app_events_url': '/v2/organizations/1e4bbba5-e6fa-4187-a664-4c652f0a83e5/app_events',
        'space_quota_definitions_url': '/v2/organizations/1e4bbba5-e6fa-4187-a664-4c652f0a83e5/space_quota_definitions'
    }
}

orgs = {
    'total_results': 1,
    'total_pages': 1,
    'prev_url': None,
    'next_url': None,
    'resources': [org]
}

route = {
    'metadata': {
        'guid': '7ffd0272-f996-4589-b4e3-56841f45edfd',
        'url': '/v2/routes/7ffd0272-f996-4589-b4e3-56841f45edfd',
        'created_at': '2018-01-09T13:11:05Z',
        'updated_at': '2018-01-09T13:11:05Z'
    },
    'entity': {
        'host': 'whatever',
        'path': '',
        'domain_guid': '4dc09f33-05e3-4db6-a6e1-15e32dcd81de',
        'space_guid': 'd7338989-6ae6-44dc-a29a-d6cfe66d71d5',
        'service_instance_guid': None,
        'port': None,
        'domain_url': '/v2/shared_domains/4dc09f33-05e3-4db6-a6e1-15e32dcd81de',
        'space_url': '/v2/spaces/d7338989-6ae6-44dc-a29a-d6cfe66d71d5',
        'apps_url': '/v2/routes/7ffd0272-f996-4589-b4e3-56841f45edfd/apps',
        'route_mappings_url': '/v2/routes/7ffd0272-f996-4589-b4e3-56841f45edfd/route_mappings'
    }
}

routes = {
    'total_results': 1,
    'total_pages': 1,
    'prev_url': None,
    'next_url': None,
    'resources': [route]
}

instances = {
    '0': {
        'state': 'RUNNING',
        'uptime': 92660,
        'since': 1515413624
    }
}

bind = {
    'metadata': {
        'guid': 'a8f47fc8-0d26-4acb-a944-6ae45ed27abe',
        'url': '/v2/service_bindings/a8f47fc8-0d26-4acb-a944-6ae45ed27abe',
        'created_at': '2018-01-04T14:35:55Z',
        'updated_at': '2018-01-08T12:15:31Z'
    },
    'entity': {
        'name': 'my-bind',
        'production': False
    }
}

binds = {
    'total_results': 1,
    'total_pages': 1,
    'prev_url': None,
    'next_url': None,
    'resources': [bind]
}
