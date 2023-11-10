# Store API

A simple online store API with DRF

## Getting Started

- Clone the repo

- Create a virtual environment and activate it

```sh
python -m venv venv && . venv/bin/activate
```

- Install the development dependencies

```sh
pip install --upgrade pip
pip install -r requirements/dev.txt
```

- Add **pre-commit** hooks

```sh
pre-commit install
```

- Creata a **.env** directory and create the following files:

  - `.django.env`
  - `.postgres.env`

```sh
mkdir .env
touch .env/.django.env
touch .env/.postgres.env
```

- Fill in the **.env** files from **.env.example**

- Create **local_settings.py** from **local_settings.py.template**

```sh
touch api/settings/environment/local_settings.py
cp api/settings/environment/local_settings.py.template api/settings/environment/local_settings.py
```

- Start server

```sh
make buildup
```

- Run tests

```sh
# Run all tests
make test

# Run specific tests
make test APP=users.tests.test_models

# Run coverage tests
make coverage-run

# Run coverage report
make coverage-report

# Run coverage HTML report
make coverage-html
```

**NOTE:** When using `make` commands, you may need to prepend `sudo`.

## Tools

- Django

- PostgreSQL

- Docker
