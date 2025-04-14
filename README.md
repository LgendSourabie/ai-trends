<p style="font-family: system-ui, sans-serif;font-size:40px; font-weight:700">
TREND INFORMATION FROM THE PIPELINE - API DOCUMENTATION
</p>

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Endpoints Overview](#endpoints-overview)
4. [Swagger OpenAPI Documentation](#swagger-openapi-documentation)
   4.1. [Redoc Documentation](#redoc-documentation)
   4.2. [Testing the API with swagger UI](#swagger-ui-testing)
5. [Task queue with celery](#task-queue)
6. [Celery and Redis: Caching, Task Queuing and Scheduling](#task-scheduling)
7. [Periodic Data Import Export](#db-export)

All the packages use in the projects are listed in the requirement.txt data with their corresponding version. For a brief summary: The trend API allow authentication through the authentication endpoints (for now only required for the admin page and for administrator). Staff users can authenticate with email and password. The next lines show how to set up an environment to run the project and the services allowed.

---

## 1. Prerequisites

Before running the project, ensure you have the following dependencies installed:

### Redis Installation

- **Windows**: [Download Redis](https://github.com/tporadowski/redis) and follow [this installation guide](https://github.com/tporadowski/redis)
- **Mac**: Install via Homebrew:

```sh
brew install redis
```

- **Linux**: Install via package manager:

```sh
sudo apt update && sudo apt install redis-server
```

### PostgreSQL 16 Installation

- **Windows**: [Download and Install PostgreSQL](https://www.postgresql.org/download/windows/)
- **Mac**: Install via Homebrew:

```sh
brew install postgresql@16
```

- **Linux**: Install via package manager:

```sh
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update
sudo apt install postgresql-16
```

### Verify Installations

After installation, confirm everything is installed correctly:

```sh
redis-server --version
psql --version
```

If everything have successfully been installed:

## Access PostgreSQL as the postgres User

```sh
sudo psql -U postgres
```

or for window users

```sh
psql -U postgres
```

## Change the Password for postgres

```sh
ALTER USER postgres WITH PASSWORD 'your_password';
```

## Create a New Database

```sh
CREATE DATABASE 'your_database_name';
```

## Exit PostgreSQL

```sh
\q
```

## Configuration Parameters

Create a folder named <b>/config</b> and create a file named <b>secrets.py</b> Copy and paste the following parameters and update with your data:

Please set ups all the password otherwise you will need to make changes in settings.py to run the project.

```sh
SQL_USER="postgres"
SQL_PWD="your_postgres_password"  # Password of your postgreSQL
REDIS_PWD = "your_redis_password" # Password of redis you installed
DB_NAME="your_database_name" # name of database created in postgreSQL
DB_HOST="127.0.0.1"
```

## 2. Project Setup

#### 2.1. Create a virtual environment (venv)

    python -m venv <name_of_the_virtual_env>  (for Windows users)
    python3 -m venv <name_of_the_virtual_env> (for MAC or Linux users)
    e.x. : python -m venv env

#### 2.2. Activate the venv

    .\<name_of_env>\Scripts\activate  (for Windows users)
    source <name_of_env>/bin/activate (for MAC or Linux users)

#### 2.3. Install packages from requirements.txt

    pip install -r requirements.txt

#### 2.4. Run migration

<h6>For Windows users:</h6>

    python manage.py makemigrations user file_upload trend_app
    python manage.py migrate

<h6>For MAC or Linux users:</h6>

    python3 manage.py makemigrations user file_upload trend_app
    python3 manage.py migrate

#### 2.6. Run the development server

    python manage.py runserver (for Windows users)
    python3 manage.py runserver (for MAC or Linux users)

## 3. Endpoints Overview

Since the endpoints are fully documented with OpenAPI specification, no further in-depth details will be given in this section. Visit the two links below after running your server to consult the documentation.

    http://localhost:8000/redoc/

## 4. Swagger OpenAPI Documentation

The trend API was documented using the openAPI standard with swagger-ui. This allow a browsable testing view of the API like the rest framework does but with more sophisticated and customizable UI. The OpenAPI documentation can be access via the "redoc/" endpoint and the Swagger UI endpoint "swagger/" can be used to test the API and interact with the available routes.
You can read the documentation or test the API through the following urls if you are using the development server and serve to the port 8000. Feel free to update the domain and the port number with your own domain (e.x.: <a>https://you_domain_name.com/<endpoint_name></a>).

#### 4.1 Redoc Documentation

    http://localhost:8000/redoc/

#### 4.2 Testing the API with swagger UI

    http://localhost:8000/swagger/

## 5. Task queue with celery

If you want to allow the auto import of data to the database, you will have to start <a href="https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#starting-the-worker-process" target="_blank">celery</a> worker, which uses <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a> as broker, for queuing heavy task in the background while you can continue with other tasks. Celery and django celery beat are documented in section 5.

    celery -A trends worker -l INFO                                                                                             |

## 6. Celery beat and Redis: Caching, Task Queuing and Scheduling

For requests optimization to the endpoint, <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a> was used to cache request data every 2 minutes (for test, you can update it in settings.py) since the data are not intended to be changed very often.
<a href="https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#starting-the-worker-process" target="_blank">Celery</a> and <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a>

## 7. Periodic Data Import Export

The Data can be imported or/and exported either manually or let be done by the task runner: <a href="https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#starting-the-worker-process" target="_blank">celery worker</a>

The manual export or import can be achieve via the django admin interface but only by site admin or staff members:

the automatic import or export are done by celery beat which look up at the scheduled date and time into the '/media' for new csv file. If any file is present, then celery_beat send an import task to celery for running in the background. Celery will then import all data from the csv file to the DB, create a backup file and delete the csv file from the folder so at a next schedule time it get only new files. For the purpose of testing the task have been schedule for every 2 minutes as well.

For this purpose the django celery beat service should also be started the same way we did with celery(please make sure <a href="https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html" target="_blank">Redis</a> is also running and update the password of redis in settings.py). The command to start django celery beat service is as follow:

    celery -A trends beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

In production this need to be done by the daemon of your system, for instance systemd or a supervisor. However, the periodic tasks will be set up when celery worker starts and do not need to be done manually in the admin panel. Visit the admin panel to see the setting under Interval.

## Author

Ibrahima Sourabie
contact@ibrahima-sourabie.com
