# timber

Project to download timber prices from timbercut4u & store in a SQLite
database.

## Requirements

* Python 3.11
* Pipenv

## Setup

Clone repo and run

```bash
$ cd timber/
$ pipenv install --python python3.11
```

## Instructions

1. Run `create_db.py` (within pipenv) to create `timber.db` with applicable schema
2. Run `update_db.py` (within pipenv) to download prices & write to `timber.db`

`timbercut4u.py` can also be imported to provide some functions for downloading prices.

## Scheduling db update

Can schedule db update via cron e.g.

```bash
30 5 * * 6 cd ~/git/timber && ~/.local/bin/pipenv run python update_db.py >>update_log.txt 2>&1
```
