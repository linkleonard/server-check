# server-check

Checks that requests to a specific URI behaves according to a spec, configurable via a config file. If a failure is detected, email notifications are sent out.

The kinds of checks currently supported are:
* Redirects - URI redirects to another URI
* HttpOK - URI returns a HTTP 400 OK

## Usage

```py
python main.py --config [config_filename]
```

## Configuration

Configs are provided via an ini file. An example can be found at `config.ini`.
