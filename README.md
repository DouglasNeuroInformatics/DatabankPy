# DatabankPy

[![PyPI - Version](https://img.shields.io/pypi/v/databankpy.svg)](https://pypi.org/project/databankpy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/databankpy.svg)](https://pypi.org/project/databankpy)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```shell
pip install databankpy
```

## Development Setup

### Install Dependencies

```shell
pip install ".[dev]"
```

### Build

```shell
python -m build
```

### Deploy

```shell
python -m twine upload dist/*
```

### Build Docs

```shell
sphinx-build -b html docs/source/ docs/build
http-server docs/build
```