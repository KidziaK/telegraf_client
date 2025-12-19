bump version_type="patch":
    ./bump.sh {{version_type}}

test:
    uv run maturin develop
    uv run pytest tests