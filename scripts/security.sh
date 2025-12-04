#!/bin/bash
echo "Running bandit..."
./.venv/bin/bandit -r src -c pyproject.toml 2>/dev/null || ./.venv/bin/bandit -r src
