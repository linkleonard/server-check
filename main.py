import requests
from configparser import ConfigParser


class CheckFailed(Exception):
    pass


def main():
    config = ConfigParser()
    config.read('config.ini')

    for site_name in config.sections():
        site = config[site_name]
        uri = site['uri']
        response = requests.get(uri)
        if response.url != site['redirect_uri']:
            raise CheckFailed(uri)


if __name__ == '__main__':
    main()
