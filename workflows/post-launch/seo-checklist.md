# SEO 完整清单

新站上线后的 SEO 配置逐项核查。

## 1. 爬虫配置

### robots.txt

```
User-agent: *
Allow: /

# AI search bots
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://YOURDOMAIN/sitemap.xml
```

验证：`curl https://YOURDOMAIN/robots.txt`

### sitemap.xml

- 包含所有公开页面
- `<lastmod>` 使用实际修改日期
- 文件大小 < 50MB，URL 数 < 50,000
- 使用脚本自动生成：`node scripts/generate-sitemap.js --dir ./dist --domain https://YOURDOMAIN`

### llms.txt

放在根目录，内容为网站摘要，帮助 AI 搜索引擎理解网站。格式参考 `templates/llms.txt.tmpl`。

---

## 2. 页面 Meta 标签

每个页面需要：

```html
<title>页面标题 | 网站名（60 字符以内）</title>
<meta name="description" content="页面描述（120-160 字符）">
<link rel="canonical" href="https://YOURDOMAIN/page-url">

<!-- Open Graph -->
<meta property="og:title" content="页面标题">
<meta property="og:description" content="页面描述">
<meta property="og:url" content="https://YOURDOMAIN/page-url">
<meta property="og:type" content="website">
<meta property="og:image" content="https://YOURDOMAIN/og-image.png">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="页面标题">
<meta name="twitter:description" content="页面描述">
```

---

## 3. 结构化数据（JSON-LD）

每个站点至少需要：

- **WebSite + Organization**（首页）：见 `templates/schema/website-org.json`
- **页面专属 schema**：FAQPage、Product、BreadcrumbList 等

使用 [Google Rich Results Test](https://search.google.com/test/rich-results) 验证。

---

## 4. 多语言支持（如有）

```html
<link rel="alternate" hreflang="zh-CN" href="https://YOURDOMAIN/">
<link rel="alternate" hreflang="en" href="https://YOURDOMAIN/en">
<link rel="alternate" hreflang="x-default" href="https://YOURDOMAIN/">
```

Sitemap 使用多语言版本：`templates/sitemap-multilang.xml.tmpl`

---

## 5. 响应头配置

使用 `templates/_headers`（Cloudflare Pages）或等效配置：

- 文本文件 Content-Type 正确（`text/plain; charset=UTF-8`）
- XML 文件 Content-Type 正确（`application/xml; charset=UTF-8`）
- HTML/JS 合理设置 Cache-Control

验证：`./scripts/check-headers.sh https://YOURDOMAIN`

---

## 自查清单

- [ ] robots.txt 可正常访问，包含正确 Sitemap URL
- [ ] sitemap.xml 可正常访问，所有 URL 均可达
- [ ] llms.txt 可正常访问
- [ ] 首页 title 和 description 符合规范
- [ ] JSON-LD 通过 Rich Results Test 验证
- [ ] hreflang 标签（多语言站点）
- [ ] _headers / Nginx 响应头配置正确
