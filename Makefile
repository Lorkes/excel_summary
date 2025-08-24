format:
	poetry run ruff format
	poetry run ruff check . --fix

check:
	poetry run ruff format --check
	poetry run ruff check .
	poetry run mypy src

start:
	docker compose up app --build

stop:
	docker compose stop
