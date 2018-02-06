# Chaos Toolkit Cloud Foundry Extension

[![Build Status](https://travis-ci.org/chaostoolkit/chaostoolkit-cloud-foundry.svg?branch=master)](https://travis-ci.org/chaostoolkit/chaostoolkit-cloud-foundry)

This extension package provides probes and actions for Chaos Engineering
experiments against a Cloud Foundry instance using the
[Chaos Toolkit][chaostoolkit].

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install -U chaostoolkit-cloud-foundry
```

## Usage

To use the probes and actions from this package, add a similar payload to your
experiment file:

```json
{
    "type": "action",
    "name": "terminate-random-instance",
    "provider": {
        "type": "python",
        "module": "chaoscf.probes",
        "func": "terminate_some_random_instance",
        "arguments": {
            "name": "my-app",
            "org_name": "my-org",
            "space_name": "my-space"
        }
    }
},
{
    "type": "probe",
    "name": "fetch-app-statistics",
    "provider": {
        "type": "python",
        "module": "chaoscf.probes",
        "func": "get_app_stats",
        "arguments": {
            "name": "my-app",
            "org_name": "my-org",
            "space_name": "my-space"
        }
    }
}
```

That's it!

Please explore the code to see existing probes and actions.

### Discovery

You may use the Chaos Toolkit to discover the capabilities of this extension:

```
$ chaos discover chaostoolkit-cloud-foundry --no-install
```

If you have logged in against a Cloud Foundry environment, this will discover
information about it along the way.

## Configuration

This extension to the Chaos Toolkit need credentials to a Cloud Foundry account
with appropriate scopes. Please add the following sections to your experiment
file:

```json
{
    "configuration": {
        "cf_api_url": "https://api.local.pcfdev.io",
        "cf_verify_ssl": false
    },
    "secrets": {
        "cloudfoundry": {
            "cf_username": "user",
            "cf_password": "pass"
        }
    }
}
```

You may leave `"cf_verifiy_ssl"` out of the configuration when you want to
verify TLS certificates. Usually, local environments are self-signed so it
may be useful to disable that check in that case.

You may also specify the `"cf_client_id"` and `"cf_client_secret"` secrets
when you need. Their default values are `"cf"` and `""` respectively. These
work well against a local [PCF dev][pcfdev] install.

[pcfdev]: https://pivotal.io/pcf-dev

Then in your probe or action:

```json
{
    "type": "probe",
    "name": "fetch-app-statistics",
    "provider": {
        "type": "python",
        "secrets": ["cloudfoundry"],
        "module": "chaoscf.probes",
        "func": "get_app_stats",
        "arguments": {
            "name": "my-app",
            "org_name": "my-org",
            "space_name": "my-space"
        }
    }
}
```


## Test

To run the tests for the project execute the following:

```
$ pip install -r requirements-dev.txt
$ pytest
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit project requires all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works