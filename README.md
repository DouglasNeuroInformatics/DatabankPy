<!-- PROJECT LOGO -->
<div align="center">
  <a href="https://github.com/DouglasNeuroInformatics/DatabankPy">
    <img src=".github/assets/logo.png" alt="Logo" width="100" >
  </a>
  <h3 align="center">DatabankPy</h3>
  <p align="center">
    A set of utilities for programmatic access to the DNP databank 
    <br />
    <a href="https://douglasneuroinformatics.github.io/DatabankPy/">
      <strong>Explore the docs »
      </strong>
    </a>
    <br />
    <br />
    <a href="https://databank.douglasneuroinformatics.ca">Access Bank</a>
    ·
    <a href="https://github.com/DouglasNeuroInformatics/DatabankPy/issues">Report Bug</a>
    ·
    <a href="https://github.com/DouglasNeuroInformatics/DatabankPy/issues">Request Feature</a>
  </p>
</div>

<!-- PROJECT SHIELDS -->
<div align="center">

  ![PyPI](https://img.shields.io/pypi/v/databankpy)
  ![PyPI - License](https://img.shields.io/pypi/l/databankpy)
  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/databankpy)
  
</div>
<hr />

## About

This library includes wrapper functions for interacting with the API of our databank.

## Installation

```shell
pip install databankpy
```

## Basic Usage

### Create Dataset

```python

import os

from databankpy.dataset import Dataset

iris = Dataset({
    'name': 'Iris',
    'description': "A small classic dataset from Fisher, 1936",
    'license': 'PUBLIC_DOMAIN',
    'columns': {
        'SEPAL_LENGTH': {
            'description': 'sepal length in cm',
            'nullable': False,
            'type': 'FLOAT'
        },
        'SEPAL_WIDTH': {
            'description': 'sepal width in cm',
            'nullable': False,
            'type': 'FLOAT'
        },
        'PETAL_LENGTH': {
            'description': 'petal length in cm',
            'nullable': False,
            'type': 'FLOAT'
        },
        'PETAL_WIDTH': {
            'description': 'petal width in cm',
            'nullable': False,
            'type': 'FLOAT'
        },
        'SPECIES': {
            'description': 'species of iris',
            'nullable': False,
            'type': 'STRING'
        }
    }
})

iris.append_csv(os.path.abspath(os.path.join('data', 'iris.csv')))

email, password = os.environ['DATABANK_EMAIL'], os.environ['DATABANK_PASSWORD']
iris.upload(email, password)

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
make -C docs html && http-server -c-1 docs/build/html
```
