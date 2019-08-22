# Jason Server

![PyPI](https://img.shields.io/pypi/v/jason-server)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jason-server)
![PyPI - Status](https://img.shields.io/pypi/status/jason-server)
![PyPI - License](https://img.shields.io/pypi/l/jason-server)

Get a full fake REST API

## Table of contents

<!-- toc -->

- [Jason Server](#jason-server)
  - [Getting started](#getting-started)
  - [Routes](#routes)
    - [Singular routes](#singular-routes)
    - [Filter](#filter)
    - [Pagination](#pagination)
    - [Sorting](#sorting)
    - [Database](#database)
  - [Extras](#extras)
    - [Alternative Host](#alternative-host)
    - [Alternative Port](#alternative-port)
    - [CLI Usage](#cli-usage)

<!-- tocstop -->

## Getting started

Install Jason Server

```python
pip3 install jason-server
```

Create a `db.json` file with some data

```json
{
  "articles": [
    { "id": 1, "title": "jason-server", "author": "1" },
    { "id": 2, "title": "jason-routes", "author": "1" }
  ],
  "authors": [
    { "id": 1, "name": "bob"}
  ]
}
```

Start JSON Server

```bash
jason-server watch db.json
```

Now if you go to [http://localhost:8080/articles](http://localhost:8080/articles), you'll get

```json
{ "id": 1, "title": "jason-server", "author": "1" },
{ "id": 2, "title": "jason-routes", "author": "1" }
```

## Routes

### Singular routes

```
GET /authors
```

### Filter

```
GET /articles?title=title&author=eminem
```

### Pagination

Use `_page` and `_limit` to paginate data.

In the `Link` header you'll get `first`, `prev`, `next` and `last` links.

```
GET /articles?_page=2
GET /articles?_page=3&_limit=15
```

### Sorting

Use `_sort` and `_order` (defaults order: asccendant)

```
GET /persons?_sort=age
GET /persons?_sort=name&_order=desc
```

### Database

```
GET /db
```

## Extras

### Alternative Host

You can start JSON Server on other host with the `--host` flag:

```bash
$ json-server --host "0.0.0.0" watch db.json
```

Default: `localhost`

### Alternative Port

You can start JSON Server on other ports with the `--port` flag:

```bash
$ json-server --port 8100 watch db.json
```

Default: `8080`

### CLI Usage

```bash
Usage: jason-server [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --host TEXT     Host adress
  -p, --port INTEGER  Port
  -q, --quiet
  --version           Show the version and exit.
  --help              Show this message and exit.

Commands:
  watch  Run your database as REST Api
  ```



