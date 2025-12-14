docs:
    uv run mkdocs serve --livereload

bump *args:
    python scripts/bump.py {{args}}

test:
    uv run pytest tests

lint:
    uv run ruff check --fix

format:
    uv run ruff format

types:
    uv run ty check
