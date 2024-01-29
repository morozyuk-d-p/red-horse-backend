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

There is one route: `/invoke`.

It takes POST requests with JSON body:

```json
{
    "query": "your_request_here"
}
```

and returns a JSON response:

```json
{
    "response": "answer_goes_here"
}
```