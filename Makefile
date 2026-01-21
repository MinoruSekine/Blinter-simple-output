# Top-level targets.
lint: ruff

test: pytest

# Each specific targets.
pytest:
	uv run pytest

ruff:
	uv run ruff check .

.PHONY: pytest ruff
