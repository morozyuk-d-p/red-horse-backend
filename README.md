# TIDON - THE RED NEURO-HORSE

## Running server

### Run via Docker (recommended)

Use `docker compose` to launch all needed containers.

### Run manually

Pipenv required. Use .env and .env_pg files to specify parameters of Yandex API and PostgreSQL DBMS.

```bash
pipenv install
pipenv shell
./main.py
```

## Using API

Refer to `/docs` URL to learn how to use API