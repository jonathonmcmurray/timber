# timber

Project to download timber prices from timbercut4u & store in a SQLite
database.

## Requirements

* Python 3.11
* Pipenv (optional)

## Setup

Clone repo and run

```bash
$ cd timber/
$ pipenv install --python python3.11
```

or (without pipenv)

```bash
$ cd timber/
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

## Instructions

1. Run `create_db.py` (within pipenv) to create `timber.db` with applicable schema
2. Run `update_db.py` (within pipenv) to download prices & write to `timber.db`

`timbercut4u.py` can also be imported to provide some functions for downloading prices.

