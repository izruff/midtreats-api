# Midtreats

This repository contains the source code for the official API used by Midtreats Web, as well as documentation to our public API. Work is in progress.

## API Quickstart

Work is in progress!

## Developer Setup

We use [Django REST framework](https://www.django-rest-framework.org/) and [Docker](https://www.docker.com/) to build a multi-container application which powers our API.

While our database is not publicly accessible, you can take advantage of the `geodata/` routes, which contain most of the functions we use to produce personalized suggestions of trips and places. You will need a Google Maps API key for this.

### Setting up environment variables

Copy the contents of `.env.example` in the project root directory into `.env` in the same directory, replacing the values with your own.

You will need to supply a Django secret key (you may use any secure random string for this) and a Google Maps API key.

You also need to supply PostgreSQL details to access your own database. If you are using Docker, then you may leave them unchanged (only changing the password if necessary). If you are not, then you might want to use a custom database name, and make sure it is already created before proceeding (the build steps do not automatically create the database).

If creating a database does not suit your use case and you only need to utilize the geospatial functions, you may want to use our dedicated [Python package](https://www.github.com/izruff/midtreats-api#python-package) instead.

### Using Docker containers

We recommend having Docker installed as it simplifies the setup process and takes away most of dependency-related issues.

Before building on Docker, you need to run the following command on your project directory (in the host machine) to modify permission rights for the Docker entrypoints:

```sh
chmod +x docker/*/entrypoint.sh
```

Then, you can run:

```sh
docker compose up -d
```

Everything should be working out-of-the-box. By default, you can access the API endpoints from `localhost:8000` in your host machine. You can change this by editing the `DJ_ADDRPORT` environment variable.

To make changes, see the [Contributing](https://www.github.com/izruff/midtreats-api#contributing) section.

### Not using Docker

If you wish to not use Docker, you can still follow along with your local environment. You will need to install [Python](https://www.python.org/) and [PostgreSQL](https://www.postgresql.org/). In our project, we use the Docker images containing Python 3.10.12 and Postgres 16.

Note that Django supports only a few of the most recent versions of Python: in Django 5.0 - the version this project uses - only Python 3.10, 3.11, and 3.12 are supported.

Create a Python [virtual environment](https://docs.python.org/3/library/venv.html) by running

```sh
python -m venv venv
source venv/bin/activate
```

in your project directory (these commands are for Linux). Then, install the dependencies by running:

```sh
pip install -r requirements.txt
```

Migrate the database by running:

```sh
python manage.py makemigrations
python manage.py migrate
```

Before that, remember to create the database manually (`CREATE DATABASE your-database`). Finally, run the server with the command:

```sh
python manage.py runserver ${DJ_ADDRPORT}
```

where `${DJ_ADDRPORT}` is the `address:port` to run the server (see the environment variable). Alternatively, you can omit it and it will run at `localhost:8000` by default.

### Python package

We have plans to migrate most of these functionalities into an open-source Python package, but this is still far down our roadmap. Stay tuned!

## Contributing

Work is in progress!
