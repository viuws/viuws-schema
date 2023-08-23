# viuws-schema

[![pypi](https://img.shields.io/pypi/v/viuws-schema?label=pypi)](https://pypi.org/project/viuws-schema/)
[![python](https://img.shields.io/pypi/pyversions/viuws-schema?label=python)](https://www.python.org)
[![test-and-deploy](https://img.shields.io/github/actions/workflow/status/viuws/viuws-schema/test-and-deploy.yml?label=test-and-deploy)](https://github.com/viuws/viuws-schema/actions/workflows/test-and-deploy.yml)
[![coverage](https://img.shields.io/codecov/c/gh/viuws/viuws-schema?label=coverage)](https://app.codecov.io/gh/viuws/viuws-schema)
[![issues](https://img.shields.io/github/issues/viuws/viuws-schema?label=issues)](https://github.com/viuws/viuws-schema/issues)
[![pull requests](https://img.shields.io/github/issues-pr/viuws/viuws-schema?label=pull%20requests)](https://github.com/viuws/viuws-schema/pulls)
[![license](https://img.shields.io/github/license/viuws/viuws-schema?label=license)](https://github.com/viuws/viuws-schema/blob/main/LICENSE)

ViUWS Schema

## Requirements

[Python](https://www.python.org) 3.9 or later

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install viuws-schema:

    pip install viuws-schema

## Usage

To list all available `$VERSION` values:

    viuws-schema versions

To list all available `$MODEL` values for the specified `$VERSION`:

    viuws-schema models --version $VERSION

To generate a JSON Schema for the specified `$VERSION` and `$MODEL`:

    viuws-schema generate --version $VERSION $MODEL

To upgrade an existing instance of `$MODEL` to the specified `$VERSION`:

    viuws-schema upgrade --to-version $VERSION $MODEL myinstance.json

To validate an existing instance of `$MODEL` against the specified `$VERSION`:

    viuws-schema validate --expect-version $VERSION $MODEL myinstance.json

## Support

For each `$VERSION` and `$MODEL` (lower case), a JSON Schema is hosted on:

    https://viuws.github.io/viuws-schema/$VERSION/$MODEL.json

The JSON Schema of each `$VERSION` and `$MODEL` (lower case) is documented on:

    https://viuws.github.io/viuws-schema/$VERSION/$MODEL.html

If you find a bug, please [raise an issue](https://github.com/viuws/viuws-schema/issues/new).

## Contributing

Pull requests are welcome.

For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Changelog

[Changelog](https://github.com/viuws/viuws-schema/blob/main/CHANGELOG.md)

## Authors

[Jonas Windhager](mailto:jonas@windhager.io)

## License

[MIT](https://github.com/viuws/viuws-schema/blob/main/LICENSE)
