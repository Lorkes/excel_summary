#!/bin/sh

poetry run python src/manage.py collectstatic --no-input
poetry run python src/manage.py migrate
poetry run gunicorn excel_summary.wsgi -b 0.0.0.0:8000
