# va-spec-python

**VA-Spec-Python** provides Python language support and a reference implementation for
the [GA4GH Variant Annotation Specification (VA-Spec)](https://github.com/ga4gh/va-spec).

## Information

[![license](https://img.shields.io/badge/license-Apache-green)](https://github.com/ga4gh/va-spec-python/blob/main/LICENSE)

## Releases

[![gitHub tag](https://img.shields.io/github/v/tag/ga4gh/va-spec-python.svg)](https://github.com/ga4gh/va-spec-python/releases) [![pypi](https://img.shields.io/pypi/v/ga4gh.va_spec.svg)](https://pypi.org/project/ga4gh.va_spec/)

## Development

[![action status](https://github.com/ga4gh/va-spec-python/actions/workflows/python-cqa.yaml/badge.svg)](https://github.com/ga4gh/va-spec-python/actions/workflows/python-cqa.yaml) [![issues](https://img.shields.io/github/issues-raw/ga4gh/va-spec-python.svg)](https://github.com/ga4gh/va-spec-python/issues)
[![GitHub Open Pull Requests](https://img.shields.io/github/issues-pr/ga4gh/va-spec-python.svg)](https://github.com/ga4gh/va-spec-python/pull/) [![GitHub license](https://img.shields.io/github/contributors/ga4gh/va-spec-python.svg)](https://github.com/ga4gh/va-spec-python/graphs/contributors/) [![GitHub stars](https://img.shields.io/github/stars/ga4gh/va-spec-python.svg?style=social&label=Stars)](https://github.com/ga4gh/va-spec-python/stargazers) [![GitHub forks](https://img.shields.io/github/forks/ga4gh/va-spec-python.svg?style=social&label=Forks)](https://github.com/ga4gh/va-spec-python/network)

## Features

- Pydantic implementation of VA-Spec models

## Known Issues

**You are encouraged to** [browse issues](https://github.com/ga4gh/va-spec-python/issues).
All known issues are listed there. Please report any issues you find.

## Developers

This section is intended for developers who contribute to VA-Spec-Python.

### Installing for development

#### Prerequisites

- Python >= 3.10
  - _Note: Python 3.12 is required for developers contributing to VA-Spec-Python_

Fork the repo at <https://github.com/ga4gh/va-spec-python/>.

Install development dependencies and `pre-commit`:

```shell
git clone --recurse-submodules git@github.com:YOUR_GITHUB_ID/va-spec-python.git
cd va-spec-python
make devready
source venv/3.12/bin/activate
pre-commit install
```

Check style with `ruff`:

```shell
make format; make lint
```

#### Submodules

va-spec-python embeds va-spec as a submodule, only for testing purposes. When checking
out va-spec-python and switching branches, it is important to make sure that the
submodule tracks va-spec-python correctly. The recommended way to do this is
`git config --global submodule.recurse true`. **If you don't set submodule.recurse,
developers and reviewers must be extremely careful to not accidentally upgrade or
downgrade schemas with respect to va-spec-python.**

If you already cloned the repo, but forgot to include `--recurse-submodules` you can run:

```shell
git submodule update --init --recursive
```

### Testing

To run tests:

```shell
make test
```

## Security Note (from the GA4GH Security Team)

A stand-alone security review has been performed on the specification itself.
This implementation is offered as-is, and without any security guarantees. It
will need an independent security review before it can be considered ready for
use in security-critical applications. If you integrate this code into your
application it is AT YOUR OWN RISK AND RESPONSIBILITY to arrange for a security
audit.
