#!/bin/bash
# 百度主动推送：读取 sitemap.xml，批量提交所有 URL 到百度搜索资源平台。
#
# 用法：
#   BAIDU_TOKEN=xxx DOMAIN=example.com ./submit-baidu.sh
#   BAIDU_TOKEN=xxx DOMAIN=example.com SITEMAP=./dist/sitemap.xml ./submit-baidu.sh
#
# 环境变量：
#   BAIDU_TOKEN  必须。百度站长平台 → 数据引入 → 链接提交 → 主动推送 → 获取接口调用地址中的 token
#   DOMAIN       必须。你的域名，如 example.com（不含 https://）
#   SITEMAP      可选。sitemap.xml 路径，默认 sitemap.xml
#
# 限制：每次最多提交 2000 条，每天上限 10000 条。

set -euo pipefail

if [[ -z "${BAIDU_TOKEN:-}" || -z "${DOMAIN:-}" ]]; then
  echo "Error: BAIDU_TOKEN and DOMAIN environment variables are required."
  echo "Usage: BAIDU_TOKEN=xxx DOMAIN=example.com ./submit-baidu.sh"
  exit 1
fi

SITEMAP="${SITEMAP:-sitemap.xml}"

if [[ ! -f "$SITEMAP" ]]; then
  echo "Error: sitemap file not found: $SITEMAP"
  exit 1
fi

# 提取所有 <loc> URL
URLS=$(grep -oP '(?<=<loc>)[^<]+' "$SITEMAP")
COUNT=$(echo "$URLS" | wc -l | tr -d ' ')

echo "Found $COUNT URL(s) in $SITEMAP"
echo "Submitting to Baidu..."

RESPONSE=$(echo "$URLS" | curl -s \
  -H 'Content-Type:text/plain' \
  --data-binary @- \
  "https://data.zz.baidu.com/urls?site=https://${DOMAIN}&token=${BAIDU_TOKEN}")

echo "Response: $RESPONSE"

# 解析结果（百度返回 JSON，如 {"remain":9900,"success":100}）
if echo "$RESPONSE" | grep -q '"success"'; then
  SUCCESS=$(echo "$RESPONSE" | grep -oP '(?<="success":)\d+')
  REMAIN=$(echo "$RESPONSE" | grep -oP '(?<="remain":)\d+')
  echo "Submitted: $SUCCESS URL(s). Daily quota remaining: $REMAIN"
else
  echo "Submission may have failed. Check the response above."
  exit 1
fi
