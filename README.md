# Anonymizer

A Python module that provides multiple anonymization techniques for text.

[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![Moved](https://img.shields.io/badge/project-moved-blue)](https://gitlab.opencode.de/bmbf/datenlabor/openredact)

# ⚠️ Moved

This project has moved to: https://gitlab.opencode.de/bmbf/datenlabor/openredact

This repository is archived and no longer maintained.

---

_**⚠️ Disclaimer ⚠️:**_ This is a prototype. Do not use for anything critical.

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

## License

MIT
