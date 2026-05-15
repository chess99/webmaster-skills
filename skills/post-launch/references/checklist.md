# Post-Launch SEO Checklist

新站上线后的 SEO 配置逐项核查。

## 1. 爬虫配置

### robots.txt

```
User-agent: *
Allow: /

# AI search bots — allow citation
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://YOURDOMAIN/sitemap.xml
```

验证：`curl -sI https://YOURDOMAIN/robots.txt | grep content-type`
Expected: `content-type: text/plain`

### sitemap.xml

- 包含所有公开页面
- `<lastmod>` 使用实际修改日期
- 文件大小 < 50MB，URL 数 < 50,000

验证：`curl -sI https://YOURDOMAIN/sitemap.xml | grep content-type`
Expected: `content-type: application/xml`

### llms.txt

放在根目录，内容为网站摘要，帮助 AI 搜索引擎理解网站。

最简结构：
```
# SITE_NAME

> 一句话描述这个网站是什么

## What

网站功能的 2-3 句描述。

## Key Pages

- [Home](https://YOURDOMAIN/) — 首页描述
```

验证：`curl -sI https://YOURDOMAIN/llms.txt | grep content-type`
Expected: `content-type: text/plain`

### _headers（Cloudflare Pages）

```
/*.txt
  Content-Type: text/plain; charset=UTF-8

/*.xml
  Content-Type: application/xml; charset=UTF-8

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/*.js
  Cache-Control: public, max-age=0, must-revalidate
```

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

每个站点首页至少需要 WebSite + Organization：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "name": "SITE_NAME",
      "url": "https://YOURDOMAIN",
      "description": "SITE_DESCRIPTION"
    },
    {
      "@type": "Organization",
      "name": "SITE_NAME",
      "url": "https://YOURDOMAIN"
    }
  ]
}
</script>
```

页面专属 schema：FAQPage、Product、BreadcrumbList（用 `marketing-skills:schema`）

验证：[Google Rich Results Test](https://search.google.com/test/rich-results)

---

## 4. 多语言支持（如有）

```html
<link rel="alternate" hreflang="zh-CN" href="https://YOURDOMAIN/">
<link rel="alternate" hreflang="en" href="https://YOURDOMAIN/en">
<link rel="alternate" hreflang="x-default" href="https://YOURDOMAIN/">
```

多语言 sitemap 在 `<url>` 块里加 `<xhtml:link>` hreflang 标签。

---

## 自查清单

- [ ] robots.txt 可访问，Content-Type: text/plain，包含 Sitemap URL
- [ ] sitemap.xml 可访问，Content-Type: application/xml，所有 URL 均可达
- [ ] llms.txt 可访问，Content-Type: text/plain
- [ ] 首页 title（< 60 字符）和 description（120-160 字符）
- [ ] WebSite + Organization JSON-LD 通过 Rich Results Test
- [ ] OG / Twitter Card meta 标签
- [ ] hreflang 标签（多语言站点）
- [ ] _headers / Nginx 响应头配置正确
