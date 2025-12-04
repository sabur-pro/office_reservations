#!/bin/bash
echo "Running ruff check..."
./.venv/bin/ruff check . "$@"
