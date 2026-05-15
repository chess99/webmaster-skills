---
name: post-launch
description: "Full post-launch workflow for new websites. Use when the user says 'my site just launched,' 'new site is live,' 'what do I do after launch,' 'post-launch checklist,' 'just deployed,' 'site is online now,' or 'what should I do after going live.' This skill orchestrates the complete sequence: file validation, structured data, AI SEO, performance, search engine submission, and analytics. Requires marketing-skills to be installed for steps 2, 3, and 6."
metadata:
  version: 1.0.0
---

# Post-Launch Workflow

You are a webmaster assistant. Your goal is to guide the user through the complete post-launch optimization sequence for a new website, step by step.

## Prerequisites

This skill calls other skills. Confirm the user has both installed:
- `marketing-skills` (for schema, ai-seo, analytics steps)
- `webmaster-skills` (this plugin, for performance and search-console steps)

If marketing-skills is not installed, tell the user:
```
/plugin install coreyhaines31/marketingskills
```

## Step 1: Validate Essential Files

Ask for the site URL, then check these files exist and have correct Content-Type headers:

```bash
# Check each file — expect HTTP 200 and correct Content-Type
curl -sI URL/robots.txt | grep -E "HTTP|content-type"
curl -sI URL/sitemap.xml | grep -E "HTTP|content-type"
curl -sI URL/llms.txt | grep -E "HTTP|content-type"
```

**robots.txt** must return `content-type: text/plain`
**sitemap.xml** must return `content-type: application/xml`
**llms.txt** must return `content-type: text/plain`

If any file is missing or has wrong Content-Type, fix it before proceeding. See `references/checklist.md` for correct file contents and Cloudflare Pages `_headers` config.

## Step 2: Structured Data

Run:
```
marketing-skills:schema
```

Goal: Add at minimum WebSite + Organization JSON-LD on the homepage. Add page-specific schema (FAQPage, Product, BreadcrumbList) where applicable.

## Step 3: AI Search Optimization

Run:
```
marketing-skills:ai-seo
```

Goal: Create or improve `llms.txt`, ensure content is structured for AI citation, add appropriate meta tags.

## Step 4: Performance

Run:
```
webmaster-skills:performance
```

Goal: Score ≥ 90 on PageSpeed Insights mobile. Fix any LCP > 2.5s, CLS > 0.1, or INP > 200ms issues.

## Step 5: Search Engine Submission

Run:
```
webmaster-skills:search-console
```

Goal: Site verified and sitemap submitted to Google Search Console, Baidu, and Bing.

## Step 6: Analytics

Run:
```
marketing-skills:analytics
```

Then add Baidu Analytics if targeting Chinese users:
1. Register at [tongji.baidu.com](https://tongji.baidu.com)
2. Add site → copy the tracking JS snippet
3. Paste before `</head>` in your HTML template
4. Verify: visit your site, check Baidu Analytics real-time report

## Completion Check

After all steps, run a final validation:

```bash
# Re-check files
curl -sI URL/robots.txt | grep -E "HTTP|content-type"
curl -sI URL/sitemap.xml | grep -E "HTTP|content-type"

# Quick PageSpeed check
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL&strategy=mobile" | grep '"score"' | head -3
```

Then check Google Search Console for any crawl errors 24-48 hours after submission.

## Related Skills

- `webmaster-skills:performance` — deep CWV diagnosis
- `webmaster-skills:search-console` — search engine submission detail
- `marketing-skills:seo-audit` — ongoing SEO health checks
