#!/bin/bash
echo "Running ruff format..."
./.venv/bin/ruff format . "$@"
