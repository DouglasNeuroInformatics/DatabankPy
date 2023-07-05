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
