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

- Creata a **.env** file and fill results from **.env_example**

```sh
touch .env
cp .env.example .env
source .env
```

- Run migrations

```sh
python manage.py migrate
```

- Run server

```sh
python manage.py runserver
```

- Run tests

```sh
python manage.py test
```

## Tools

- Django

- PostgreSQL
