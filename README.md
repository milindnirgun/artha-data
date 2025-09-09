# artha-data

[![Release](https://img.shields.io/github/v/release/milindnirgun/artha-data)](https://img.shields.io/github/v/release/milindnirgun/artha-data)
[![Build status](https://img.shields.io/github/actions/workflow/status/milindnirgun/artha-data/main.yml?branch=main)](https://github.com/milindnirgun/artha-data/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/milindnirgun/artha-data/branch/main/graph/badge.svg)](https://codecov.io/gh/milindnirgun/artha-data)
[![Commit activity](https://img.shields.io/github/commit-activity/m/milindnirgun/artha-data)](https://img.shields.io/github/commit-activity/m/milindnirgun/artha-data)
[![License](https://img.shields.io/github/license/milindnirgun/artha-data)](https://img.shields.io/github/license/milindnirgun/artha-data)

This is the data collection and processing project consisting of ETL scripts and some APIs. The main purpose of this source is to provide a financial database backend to the main Artha project.

- **Github repository**: <https://github.com/milindnirgun/artha-data/>
- **Documentation** <https://milindnirgun.github.io/artha-data/>

# Documentation about this repo (organization)
The source code is organized as follows:
- .github - contains some workflows that schedule batch execution to automate
the main tasks of downloading datafiles from Nasdaq and storing that data into
our local artha database.
- data - this is the directory containing the database(s)
- datafiles - this is the directory where raw data gets downloaded from Nasdaq
  as json files
- docs - self explanatory
- src/artha-data - this is the main source code repository
  - api - this folder contains code for the database api
  - batch - this folder contains some batch programs that are either scheduled
    in workflows or are run manually.
  - schemas - this folder contains schema definitions for each table as a
  separate file with the file name being the table name
  - tests - holds junits


## Below is standard boilerplate documentation from the original source
## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:milindnirgun/artha-data.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/codecov/).

## Releasing a new version



---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
