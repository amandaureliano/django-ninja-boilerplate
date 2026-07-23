.PHONY: run migrate migrations shell test coverage lint format

run:
	uv run python app/manage.py runserver

migrate:
	uv run python app/manage.py migrate

migrations:
	uv run python app/manage.py makemigrations

shell:
	uv run python app/manage.py shell

test:
	uv run pytest

coverage:
	uv run pytest --cov --cov-report=term-missing

lint:
	uv run ruff check app/

format:
	uv run ruff format app/
