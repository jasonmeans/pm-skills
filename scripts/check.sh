#!/usr/bin/env bash
# Run before every commit: skill contract lint, script tests, token audit.
# Usage: bash scripts/check.sh
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/lint_skills.py
python3 -m unittest discover -s scripts/tests -q
python3 scripts/token_audit.py --strict > /dev/null || {
  echo "token_audit found warnings; run: python3 scripts/token_audit.py" >&2
  exit 1
}
echo "check: OK"
