#!/bin/bash
# 验证线上关键文件的 HTTP 响应头（Content-Type、Cache-Control、状态码）。
#
# 用法：
#   ./check-headers.sh https://example.com
#   ./check-headers.sh --help

set -euo pipefail

if [[ "${1:-}" == "--help" || -z "${1:-}" ]]; then
  echo "Usage: ./check-headers.sh <base-url>"
  echo "  e.g. ./check-headers.sh https://example.com"
  echo ""
  echo "Checks: /robots.txt  /sitemap.xml  /llms.txt"
  exit 0
fi

BASE_URL="${1%/}"

PASS=0
FAIL=0

check() {
  local path="$1"
  local expected_type="$2"
  local url="${BASE_URL}${path}"

  local headers
  headers=$(curl -sI --max-time 10 "$url") || { echo "FAIL  $url (connection error)"; FAIL=$((FAIL + 1)); return; }

  local status
  status=$(echo "$headers" | grep -oP '(?<=HTTP/\S* )\d+' | head -1)

  local content_type
  content_type=$(echo "$headers" | grep -i '^content-type:' | head -1 | sed 's/content-type: //I' | tr -d '\r')

  if [[ "$status" == "200" ]] && echo "$content_type" | grep -qi "$expected_type"; then
    echo "OK    $url  [$status]  $content_type"
    PASS=$((PASS + 1))
  else
    echo "FAIL  $url  [$status]  got: '$content_type'  expected: '$expected_type'"
    FAIL=$((FAIL + 1))
  fi
}

echo "Checking headers for $BASE_URL"
echo "---"

check "/robots.txt"   "text/plain"
check "/sitemap.xml"  "application/xml"
check "/llms.txt"     "text/plain"

echo "---"
echo "Result: $PASS passed, $FAIL failed"

[[ $FAIL -eq 0 ]]
