# webmaster-skills Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `webmaster-workflows` 仓库完整重构为可发布的 Claude Code plugin `webmaster-skills`，包含 3 个 skill：`performance`、`post-launch`、`search-console`。

**Architecture:** 纯 Markdown skill 集合，遵循 Agent Skills spec。每个 skill 一个目录 + `SKILL.md`（YAML frontmatter + 操作指引），详细参考内容放 `references/` 子目录。同时配置 `.claude-plugin/` 元数据使其可通过 `/plugin install` 安装。

**Tech Stack:** Markdown only，无构建步骤，无依赖。

---

## 当前状态

- 仓库本地路径：`/Users/zcs/code2/webmaster-workflows`
- 远程已改名：`git@github.com:chess99/webmaster-skills.git`（本地 remote 尚未更新）
- 需要删除的旧目录：`workflows/`、`templates/`、`scripts/`、`docs/`
- 需要迁移的内容：`workflows/post-launch/performance.md` → `skills/performance/references/`，以此类推

---

## Task 1：更新 git remote + 更新 README 和 CLAUDE.md

**Files:**
- Modify: `README.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: 更新 git remote URL**

```bash
git remote set-url origin git@github.com:chess99/webmaster-skills.git
git remote -v
```

Expected output:
```
origin  git@github.com:chess99/webmaster-skills.git (fetch)
origin  git@github.com:chess99/webmaster-skills.git (push)
```

- [ ] **Step 2: 写新的 README.md**

完整替换 `README.md` 内容：

```markdown
# webmaster-skills

Webmaster skills for indie site owners. Works with Claude Code and any agent that supports the [Agent Skills spec](https://agentskills.io).

## Install

```bash
/plugin install chess99/webmaster-skills
```

Also install [marketing-skills](https://github.com/coreyhaines31/marketingskills) — the `post-launch` skill builds on it:

```bash
/plugin install coreyhaines31/marketingskills
```

## Available Skills

| Skill | Description |
|-------|-------------|
| [performance](skills/performance/) | Diagnose and fix Core Web Vitals (LCP, CLS, INP). Runs PageSpeed Insights automatically and gives targeted fixes. |
| [post-launch](skills/post-launch/) | Full post-launch workflow for new sites — validates files, orchestrates schema, AI SEO, performance, search engine submission, and analytics setup in order. |
| [search-console](skills/search-console/) | Submit your site to Google Search Console, Baidu, and Bing. Handles verification, sitemap submission, and Baidu active push via curl. |

## How Skills Work Together

`post-launch` is the entry point — it calls the other skills in the right order:

```
post-launch
  ├── 1. Validate robots.txt / sitemap.xml / llms.txt
  ├── 2. marketing-skills:schema
  ├── 3. marketing-skills:ai-seo
  ├── 4. webmaster-skills:performance  ←
  ├── 5. webmaster-skills:search-console  ←
  └── 6. marketing-skills:analytics
```

## Contributing

PRs welcome. Each skill is a single `SKILL.md` file under `skills/<name>/`. See [Agent Skills spec](https://agentskills.io/specification.md) for format requirements.
```

- [ ] **Step 3: 写新的 CLAUDE.md**

完整替换 `CLAUDE.md` 内容：

```markdown
# webmaster-skills

Claude Code plugin — webmaster skill collection for indie site owners.

## Skills

- `performance` — Core Web Vitals diagnosis and optimization
- `post-launch` — New site launch workflow (orchestrates other skills)
- `search-console` — Search engine submission (GSC, Baidu, Bing)

## Install

```bash
/plugin install chess99/webmaster-skills
```

## Dependencies

`post-launch` calls marketing-skills. Install both:

```bash
/plugin install coreyhaines31/marketingskills
/plugin install chess99/webmaster-skills
```

## Skill Format

Each skill: one directory + `SKILL.md` with YAML frontmatter (`name` + `description`). Optional `references/` subdirectory for detailed docs loaded on demand.
```

- [ ] **Step 4: 提交**

```bash
git add README.md CLAUDE.md
git commit -m "docs: rewrite README and CLAUDE.md for plugin release"
```

---

## Task 2：创建 `.claude-plugin/` 元数据

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`

- [ ] **Step 1: 创建 `.claude-plugin/plugin.json`**

```json
{
  "name": "webmaster-skills",
  "description": "Webmaster skills for indie site owners — Core Web Vitals optimization, post-launch checklist, and search engine submission",
  "version": "1.0.0",
  "author": { "name": "chess99" },
  "homepage": "https://github.com/chess99/webmaster-skills",
  "repository": "https://github.com/chess99/webmaster-skills",
  "license": "MIT",
  "skills": "./skills"
}
```

- [ ] **Step 2: 创建 `.claude-plugin/marketplace.json`**

```json
{
  "name": "webmaster-skills",
  "owner": { "name": "chess99" },
  "metadata": {
    "description": "3 webmaster skills for indie site owners: performance optimization, post-launch workflow, and search engine submission",
    "version": "1.0.0",
    "repository": "https://github.com/chess99/webmaster-skills"
  },
  "plugins": [
    {
      "name": "webmaster-skills",
      "description": "3 webmaster skills for indie site owners: Core Web Vitals optimization, post-launch checklist workflow, and search engine submission (Google Search Console, Baidu, Bing)",
      "source": "./"
    }
  ]
}
```

- [ ] **Step 3: 提交**

```bash
git add .claude-plugin/
git commit -m "feat: add claude-plugin metadata for plugin install"
```

---

## Task 3：创建 `performance` skill

**Files:**
- Create: `skills/performance/SKILL.md`
- Create: `skills/performance/references/cwv-optimization.md`（从 `workflows/post-launch/performance.md` 迁移并扩充）

- [ ] **Step 1: 创建 `skills/performance/SKILL.md`**

```markdown
---
name: performance
description: "When the user wants to diagnose or fix website performance issues. Use when the user mentions 'slow website,' 'LCP,' 'CLS,' 'INP,' 'Core Web Vitals,' 'CWV,' 'PageSpeed score,' 'web vitals,' 'performance optimization,' 'my site is slow,' 'Google says my page is slow,' 'improve page speed,' 'Time to First Byte,' 'TTFB,' or 'Largest Contentful Paint.' Start with a PageSpeed Insights diagnosis before recommending fixes — don't give generic advice without data. For broader SEO issues, see marketing-skills:seo-audit."
metadata:
  version: 1.0.0
---

# Web Performance Optimization

You are an expert in web performance and Core Web Vitals. Your goal is to diagnose real performance issues and provide targeted, data-driven fixes — not generic checklists.

## Step 1: Diagnose with PageSpeed Insights

Before giving any recommendations, run a real diagnostic. Ask the user for their URL if not provided, then run:

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL_HERE&strategy=mobile" | python3 -m json.tool | grep -E '"id"|"score"|"displayValue"' | head -40
```

If `python3` is not available:
```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL_HERE&strategy=mobile" > psi-result.json
```

Then read `psi-result.json` and extract:
- `lighthouseResult.categories.performance.score` (0-1, multiply by 100)
- `lighthouseResult.audits.largest-contentful-paint.displayValue`
- `lighthouseResult.audits.cumulative-layout-shift.displayValue`
- `lighthouseResult.audits.interactive.displayValue`
- `lighthouseResult.audits.total-blocking-time.displayValue`
- `lighthouseResult.audits.speed-index.displayValue`

Also run desktop:
```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL_HERE&strategy=desktop" | grep -E '"score"' | head -5
```

## Step 2: Triage by Impact

Based on the actual scores, focus on whichever metric is worst:

**LCP > 2.5s** → Look at: render-blocking resources, unoptimized images, slow server response, no preload on hero image
**CLS > 0.1** → Look at: images/embeds without explicit width/height, late-loading content pushing layout, web fonts causing FOUT
**INP > 200ms** → Look at: heavy JavaScript on main thread, large event handlers, third-party scripts
**TBT > 300ms** → Look at: long tasks, synchronous third-party scripts, large JavaScript bundles

## Step 3: Targeted Fixes

Only recommend fixes for issues that actually showed up in the diagnostic. Reference `references/cwv-optimization.md` for implementation details.

### Font Loading (common LCP cause)

```html
<!-- Before: blocking -->
<link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">

<!-- After: async with preload -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=..." as="style"
      onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet"></noscript>
```

### Third-Party Script Delay (common TBT/LCP cause)

For analytics scripts (GA, Clarity, etc.) that don't need to run before first interaction:

```html
<!-- Don't load until first user interaction -->
<script>
function loadScript(src) {
  var s = document.createElement('script');
  s.src = src; s.async = true;
  document.head.appendChild(s);
}
['click','scroll','keydown','touchstart'].forEach(function(e) {
  window.addEventListener(e, function() { loadScript('YOUR_SCRIPT_URL'); }, {once:true,passive:true});
});
</script>
```

### Image Optimization (common LCP + CLS cause)

```html
<!-- Hero image: preload + fetchpriority -->
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">

<!-- Always declare width + height to prevent CLS -->
<img src="image.webp" width="800" height="600" loading="lazy" decoding="async" alt="...">
```

Convert to WebP/AVIF if served as JPEG/PNG. Most static site build tools do this automatically.

### Server Response Time (TTFB > 600ms)

- Switch to a CDN-edge deployment (Cloudflare Pages, Vercel, Netlify) if on origin-only hosting
- Enable HTTP/2
- Add `Cache-Control: public, max-age=31536000, immutable` to static assets

## Step 4: Verify Fix

After implementing, re-run PageSpeed:
```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL_HERE&strategy=mobile" | grep -E '"largest-contentful-paint|cumulative-layout-shift|interactive"' -A 3
```

## Related Skills

- `marketing-skills:seo-audit` — full SEO audit including CWV check
- `webmaster-skills:post-launch` — full post-launch workflow
```

- [ ] **Step 2: 创建 `skills/performance/references/cwv-optimization.md`**

将 `workflows/post-launch/performance.md` 的全部内容复制过来，作为基础。这个文件已经存在，直接读取然后写到新路径。

- [ ] **Step 3: 提交**

```bash
git add skills/performance/
git commit -m "feat: add performance skill (Core Web Vitals diagnosis and optimization)"
```

---

## Task 4：创建 `post-launch` skill

**Files:**
- Create: `skills/post-launch/SKILL.md`
- Create: `skills/post-launch/references/checklist.md`（从 `workflows/post-launch/seo-checklist.md` 迁移）

- [ ] **Step 1: 创建 `skills/post-launch/SKILL.md`**

```markdown
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

If any file is missing or has wrong Content-Type, fix it before proceeding. See `references/checklist.md` for correct file contents.

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
```

- [ ] **Step 2: 创建 `skills/post-launch/references/checklist.md`**

将 `workflows/post-launch/seo-checklist.md` 的全部内容复制到此路径。

- [ ] **Step 3: 提交**

```bash
git add skills/post-launch/
git commit -m "feat: add post-launch skill (orchestration workflow for new site launch)"
```

---

## Task 5：创建 `search-console` skill

**Files:**
- Create: `skills/search-console/SKILL.md`
- Create: `skills/search-console/references/submit-engines.md`（从 `workflows/post-launch/search-console.md` 迁移并扩充百度推送细节）

- [ ] **Step 1: 创建 `skills/search-console/SKILL.md`**

```markdown
---
name: search-console
description: "Submit a website to search engines and manage search engine verification. Use when the user mentions 'Google Search Console,' 'GSC,' 'Baidu webmaster,' 'Baidu submission,' 'Baidu active push,' 'submit sitemap,' 'search engine submission,' 'index my site,' 'get indexed,' 'Bing Webmaster,' 'site verification,' 'sitemap not submitted,' or 'how do I submit my site to Google/Baidu/Bing.' For ongoing SEO auditing after submission, see marketing-skills:seo-audit."
metadata:
  version: 1.0.0
---

# Search Engine Submission

You are a webmaster assistant. Your goal is to get the user's site verified and sitemap submitted to all major search engines, and run Baidu active push automatically.

## What You Need First

Ask for:
1. Site URL (e.g., `https://example.com`)
2. Path to local `sitemap.xml` (for Baidu push) — or the live sitemap URL

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

Verify the sitemap URL directly:
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

This step can be run entirely by the AI — no browser needed.

### Get Your Token

Direct user to: https://ziyuan.baidu.com/linksubmit/index

Path: 用户中心 → 站点管理 → add site → 数据引入 → 链接提交 → 主动推送 → copy the token from the API URL

The token appears in the URL:
`https://data.zz.baidu.com/urls?site=https://YOURDOMAIN&token=YOUR_TOKEN`

### Run the Push

Once the user provides DOMAIN and TOKEN, fetch the sitemap and push all URLs:

```bash
# Fetch sitemap and extract URLs
curl -s https://YOURDOMAIN/sitemap.xml | grep -oP '(?<=<loc>)[^<]+' > /tmp/baidu-urls.txt

# Show how many URLs will be pushed
wc -l /tmp/baidu-urls.txt

# Push to Baidu (max 2000 per call, 10000/day quota)
curl -s -H 'Content-Type:text/plain' \
  --data-binary @/tmp/baidu-urls.txt \
  "https://data.zz.baidu.com/urls?site=https://YOURDOMAIN&token=YOUR_TOKEN"
```

Expected response:
```json
{"remain":9900,"success":100}
```

`success` = URLs accepted. `remain` = daily quota remaining.

If the site is Chinese-language or targets Chinese users, also verify the site in Baidu Webmaster Tools (百度站长工具) at https://ziyuan.baidu.com/ for additional features.

## Bing Webmaster Tools

1. Go to https://www.bing.com/webmasters/
2. Sign in with Microsoft account
3. Add site → enter URL
4. Sitemaps → Submit sitemap → enter `https://YOURDOMAIN/sitemap.xml`

Bing also supports IndexNow, which can speed up indexing. If the site uses a static site generator, check if it has an IndexNow plugin.

## Verify Indexing (After 24-48 Hours)

```bash
# Check Google indexing
# (run in browser): site:YOURDOMAIN

# Check Baidu indexing
# (run in browser): site:YOURDOMAIN on baidu.com
```

In Google Search Console, check:
- Coverage report → Indexed pages count
- Sitemaps → Status should show "Success"

## Related Skills

- `webmaster-skills:post-launch` — full post-launch workflow
- `marketing-skills:seo-audit` — audit after indexing
```

- [ ] **Step 2: 创建 `skills/search-console/references/submit-engines.md`**

将 `workflows/post-launch/search-console.md` 的内容复制到此路径，作为更详细的参考文档。

- [ ] **Step 3: 提交**

```bash
git add skills/search-console/
git commit -m "feat: add search-console skill (GSC, Baidu active push, Bing submission)"
```

---

## Task 6：删除旧目录

**Files:**
- Delete: `workflows/`
- Delete: `templates/`
- Delete: `scripts/`
- Delete: `docs/`

- [ ] **Step 1: 删除旧目录**

```bash
git rm -r workflows/ templates/ scripts/ docs/
```

- [ ] **Step 2: 确认只剩目标文件**

```bash
find . -not -path './.git/*' -type f | sort
```

Expected output（顺序可能不同）：
```
./.claude-plugin/marketplace.json
./.claude-plugin/plugin.json
./CLAUDE.md
./README.md
./skills/performance/SKILL.md
./skills/performance/references/cwv-optimization.md
./skills/post-launch/SKILL.md
./skills/post-launch/references/checklist.md
./skills/search-console/SKILL.md
./skills/search-console/references/submit-engines.md
```

- [ ] **Step 3: 提交**

```bash
git commit -m "chore: remove old workflows, templates, scripts, docs directories"
```

---

## Task 7：推送到远程

- [ ] **Step 1: 确认 remote URL 已是新名称**

```bash
git remote -v
```

Expected:
```
origin  git@github.com:chess99/webmaster-skills.git (fetch)
origin  git@github.com:chess99/webmaster-skills.git (push)
```

如果还是旧名称，执行：
```bash
git remote set-url origin git@github.com:chess99/webmaster-skills.git
```

- [ ] **Step 2: 推送**

```bash
git push -u origin main
```

- [ ] **Step 3: 验证**

```bash
git log --oneline -8
```

确认所有提交都推上去了。

---

## 自查

- [x] 所有 SKILL.md 都有完整 YAML frontmatter（name + description + metadata.version）
- [x] description 字段包含触发词
- [x] 三个 skill 边界清晰，不重复 marketing-skills 内容
- [x] plugin.json / marketplace.json 格式对齐 marketing-skills
- [x] 旧目录有明确删除步骤
- [x] references/ 内容均有迁移来源，无内容丢失
- [x] 每个 task 都有 commit 步骤
- [x] Task 6 删除后有文件树验证步骤
