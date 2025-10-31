# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

# eatnyc - NYC Restaurant Recommender
![Build and Test](https://github.com/swe-students-fall2025/3-python-package-team_avalon/actions/workflows/build.yaml/badge.svg)

**eatnyc** is a lightweight Python package that recommends top-rated NYC restaurants based on cuisine, neighborhood, price, and rating.  
It’s designed to help users explore the city’s dining scene and discover great places through data-driven recommendations — directly from the command line or in Python.

---

## How to install and use this package
### Install from PyPI (users)
```bash
pip install eatnyc
```
### Install locally (developers)
```bash
pipenv install -e .
```
If that set up fails for you, use:
```bash
python3 -m pipenv install -e .
```