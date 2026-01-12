#!/usr/bin/env bash
set -euo pipefail

if [[ -x ".venv/bin/python" ]]; then
  PYTHON_BIN=".venv/bin/python"
else
  PYTHON_BIN="python"
fi

npm install
npm run build

$PYTHON_BIN manage.py migrate
$PYTHON_BIN manage.py runserver
