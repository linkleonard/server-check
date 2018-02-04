import requests


class CheckFailed(Exception):
    pass


def main():
    checks = [
        {
            'uri': 'http://leonaard.me/',
            'redirect_to': 'https://linkleonard.me/',
        },
    ]
    for check in checks:
        uri = check['uri']
        response = requests.get(uri)
        if response.url != check['redirect_to']:
            raise CheckFailed(uri)


if __name__ == '__main__':
    main()
