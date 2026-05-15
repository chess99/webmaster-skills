---
name: search-console
description: "Submit a website to search engines and manage search engine verification. Use when the user mentions 'Google Search Console,' 'GSC,' 'Baidu webmaster,' 'Baidu submission,' 'Baidu active push,' 'submit sitemap,' 'search engine submission,' 'index my site,' 'get indexed,' 'Bing Webmaster,' 'site verification,' 'sitemap not submitted,' 'how do I submit my site to Google,' 'how do I submit to Baidu,' 'Baidu indexing,' or 'not showing up in Baidu.' For ongoing SEO auditing after submission, see marketing-skills:seo-audit."
metadata:
  version: 1.0.0
---

# Search Engine Submission

You are a webmaster assistant. Your goal is to get the user's site verified and sitemap submitted to all major search engines, and run Baidu active push automatically.

## What You Need First

Ask for:
1. Site URL (e.g., `https://example.com`)
2. Baidu push token (you'll guide them to get it below)

## Google Search Console

### 1. Add Property

Direct the user to: https://search.google.com/search-console/

Steps:
1. Click "Add property" → choose "URL prefix"
2. Enter `https://YOURDOMAIN`
3. Download the HTML verification file (e.g., `google1234abcd.html`)
4. Upload it to the site root so it's accessible at `https://YOURDOMAIN/google1234abcd.html`
5. Verify the file is accessible:
```bash
curl -sI https://YOURDOMAIN/google1234abcd.html | grep HTTP
```
Expected: `HTTP/2 200`
6. Click "Verify" in Search Console

### 2. Submit Sitemap

In Search Console: Sitemaps → enter `sitemap.xml` → Submit

Verify the sitemap URL first:
```bash
curl -sI https://YOURDOMAIN/sitemap.xml | grep -E "HTTP|content-type"
```
Expected: `HTTP/2 200` and `content-type: application/xml`

### 3. Request Indexing for Key Pages

For each important page (homepage, main landing pages):
1. Paste the URL into the Search Console URL inspection tool
2. Click "Request indexing"

Limit: ~10 requests per day. Use only for the most important pages.

## Baidu Active Push

This step can be run entirely by the AI — no browser needed after getting the token.

### Get Your Token

Direct user to: https://ziyuan.baidu.com/linksubmit/index

Path: 用户中心 → 站点管理 → add site → 数据引入 → 链接提交 → 主动推送

The token appears in the API endpoint URL shown on that page:
`https://data.zz.baidu.com/urls?site=https://YOURDOMAIN&token=YOUR_TOKEN`

Copy only the token value.

### Run the Push

Once the user provides DOMAIN and TOKEN, run:

```bash
# Fetch sitemap and extract all URLs
curl -s https://YOURDOMAIN/sitemap.xml | grep -oP '(?<=<loc>)[^<]+' > /tmp/baidu-urls.txt

# Show count before pushing
echo "URLs to push: $(wc -l < /tmp/baidu-urls.txt)"

# Push to Baidu (max 2000 per request, 10000/day quota)
curl -s -H 'Content-Type:text/plain' \
  --data-binary @/tmp/baidu-urls.txt \
  "https://data.zz.baidu.com/urls?site=https://YOURDOMAIN&token=YOUR_TOKEN"
```

Expected response:
```json
{"remain":9900,"success":100}
```

`success` = URLs accepted this call. `remain` = daily quota remaining.

If `success` is 0, check that the DOMAIN in the API URL exactly matches the domain registered in Baidu Webmaster Tools.

## Bing Webmaster Tools

1. Go to https://www.bing.com/webmasters/
2. Sign in with Microsoft account
3. Add site → enter URL
4. Sitemaps → Submit sitemap → enter `https://YOURDOMAIN/sitemap.xml`

Bing also supports IndexNow for faster indexing. If using a static site generator, check for an IndexNow plugin.

## Verify Indexing (After 24-48 Hours)

Check Google:
```bash
# In your browser, search:
# site:YOURDOMAIN
```

In Google Search Console:
- Coverage report → Indexed pages count
- Sitemaps → Status should show "Success"

Check Baidu:
```bash
# In your browser on baidu.com, search:
# site:YOURDOMAIN
```

## Related Skills

- `webmaster-skills:post-launch` — full post-launch workflow
- `marketing-skills:seo-audit` — audit after indexing

For detailed API error responses, IndexNow setup, and Baidu crawl diagnostics, see `references/submit-engines.md`.
