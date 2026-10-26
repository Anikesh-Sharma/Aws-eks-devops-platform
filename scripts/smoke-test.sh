#!/usr/bin/env bash
# Smoke test: checks key endpoints of a running TaskFlow API.
# Usage: ./scripts/smoke-test.sh [base_url]
set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"
FAILED=0

check() {
  local path="$1" expected="$2" code
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "${BASE_URL}${path}" || echo "000")
  if [[ "$code" == "$expected" ]]; then
    echo "PASS  ${path}  (${code})"
  else
    echo "FAIL  ${path}  (got ${code}, expected ${expected})"
    FAILED=1
  fi
}

echo "Smoke testing ${BASE_URL}"
check "/health" 200
check "/version" 200
check "/tasks" 200
check "/does-not-exist" 404

if [[ "$FAILED" -ne 0 ]]; then
  echo "Smoke test FAILED"
  exit 1
fi
echo "All smoke tests passed"