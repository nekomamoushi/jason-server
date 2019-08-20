# Jason Server 

![PyPI](https://img.shields.io/pypi/v/jason-server)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jason-server)
![PyPI - Status](https://img.shields.io/pypi/status/jason-server)
![PyPI - License](https://img.shields.io/pypi/l/jason-server)

Get a full fake REST API

## Table of contents

<!-- toc -->

- [Getting started](#getting-started)
  - [Singular routes](#singular-routes)
  - [Alternative port](#alternative-port)

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
GET    /profile
```

### Alternative host (default: localhost)

You can start JSON Server on other host with the `--host` flag:

```bash
$ json-server --watch db.json --host "0.0.0.0"
```

### Alternative port (default: 8080)

You can start JSON Server on other ports with the `--port` flag:

```bash
$ json-server --watch db.json --port 8100
```



