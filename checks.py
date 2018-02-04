from requests import codes

from exceptions import CheckFailed


class BaseCheck(object):
    def __init__(self, options):
        self.options = options

    def check(self, response):
        raise NotImplementedError()


class RedirectTo(BaseCheck):
    def check(self, response):
        if response.url != self.options['redirect_uri']:
            raise CheckFailed(f"Unexpected redirection to: '{response.url}'")


class HttpOK(BaseCheck):
    def check(self, response):
        if response.status_code != codes.ok:
            raise CheckFailed(
                f"Unexpected status code: '{response.status_code}'",
            )
