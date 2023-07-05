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
