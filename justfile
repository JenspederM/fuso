docs:
    uv run mkdocs serve --livereload

bump *args:
    python scripts/bump.py {{args}}

test:
    uv run pytest tests

check: lint format types

lint:
    uv run ruff check --fix

format:
    uv run ruff format

types:
    uv run ty check
