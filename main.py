import requests
from configparser import ConfigParser
from argparse import ArgumentParser
from requests.exceptions import RequestException
import logging


logger = logging.getLogger()


class CheckFailed(Exception):
    pass


def check_redirect(site):
    uri = site['uri']
    response = requests.get(uri)
    if response.url != site['redirect_uri']:
        raise CheckFailed(uri)


def format_errors_as_email_body(errors):
    strings = [
        "The following site checks failed:"
    ]

    for site_name, exception in errors:
        strings.append(f' * {site_name}: {str(exception)}')

    return '\n'.join(strings)


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '--config',
        required=True,
    )
    parser.add_argument(
        '--email-on-error',
        help='''Sends a notification e-mail upon failure.
        Recipients are specified in the config file.''',
    )
    return parser


def main():
    argument_parser = get_argument_parser()
    options = argument_parser.parse_args()

    config = ConfigParser()
    config.read(options.config)

    failed_sites = []

    for site_name in config.sections():
        site = config[site_name]

        try:
            check_redirect(site)
        except (RequestException, CheckFailed) as e:
            logger.error(f'Site check "{site_name}" failed: {repr(e)}')
            failed_sites.append([site_name, e])

    if failed_sites and options.email_on_error:
        email_body = format_errors_as_email_body(failed_sites)

        app_config = config['DEFAULT']
        recipients = app_config['notification-recipients']

        mailgun_domain = app_config['mailgun-api-domain']
        message_endpoint = f'https://api.mailgun.net/v3/{mailgun_domain}/messages'  # noqa: E501

        requests.post(
            message_endpoint,
            auth=("api", app_config['mailgun-api-key']),
            data={
                "from": "Server Check <noreply@leonaard.me>",
                "to": recipients,
                "subject": "Server Check Failures",
                "text": email_body
            })


if __name__ == '__main__':
    main()
