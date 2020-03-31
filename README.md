# Anonymizer

A Python module that provides multiple anonymization techniques for text.

![Tests](https://github.com/paberr/anonymizer/workflows/Tests/badge.svg?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

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
pytest --doctest-modules --cov-report term --cov==anonymizer
```
