#!/usr/bin/env bash
set -euo pipefail

today="$(date +%F)"
out="learnings/daily/${today}.md"

if [[ -f "$out" ]]; then
  echo "Daily log already exists: $out"
  exit 0
fi

cp docs/templates/daily-learning-template.md "$out"
sed -i.bak "s#<YYYY-MM-DD>#${today}#g" "$out"
rm -f "${out}.bak"

echo "Created $out"
