# Anonymizer

A Python module that provides multiple anonymization techniques for text.

![Tests](https://github.com/openredact/anonymizer/workflows/Tests/badge.svg?branch=master)
![Black & Flake8](https://github.com/openredact/anonymizer/workflows/Format%20and%20Lint/badge.svg?branch=master)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

## Install requirements

You can install all requirements using:

```
pip install -r requirements.txt
```

Compared to installation with `setup.py`, [requirements.txt](requirements.txt) additionally installs developer dependencies.

To install the package using `setup.py` run:

```
pip install .
```

## Install the pre-commit hooks for developing

```
pre-commit install
git config --bool flake8.strict true  # Makes the commit fail if flake8 reports an error
```

To run the hooks:
```
pre-commit run --all-files
```

## Testing

The tests can be executed with:
```
pytest --doctest-modules --cov-report term --cov=anonymizer
```
