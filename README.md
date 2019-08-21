# Jason Server

![PyPI](https://img.shields.io/pypi/v/jason-server)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jason-server)
![PyPI - Status](https://img.shields.io/pypi/status/jason-server)
![PyPI - License](https://img.shields.io/pypi/l/jason-server)

Get a full fake REST API

## Table of contents

<!-- toc -->

* [Jason Server](#jason-server)
  * [Getting started](#getting-started)
  * [Routes](#routes)
     * [Singular routes](#singular-routes)
     * [Pagination](#pagination)
     * [Alternative host (default: localhost)](#alternative-host-default-localhost)
     * [Alternative port (default: 8080)](#alternative-port-default-8080)

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

### Pagination

Use `_page` and `_limit` to paginate returned data.

In the Link header you'll get first, prev, next and last links.

```
GET /articles?_page=2
GET /articles?_page=3&_limit=15
```

### Alternative host (default: localhost)

You can start JSON Server on other host with the `--host` flag:

```bash
$ json-server --host "0.0.0.0" watch db.json
```

### Alternative port (default: 8080)

You can start JSON Server on other ports with the `--port` flag:

```bash
$ json-server --port 8100 watch db.json
```



