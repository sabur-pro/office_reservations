#!/bin/bash
echo "Running mypy..."
./.venv/bin/mypy . "$@"
