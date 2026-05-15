# Post-Launch 工作流

新站上线后的完整优化流程，建议按以下顺序执行。

## 执行顺序

### 第一步：运行自动化清单（优先）

```
/static-site-post-launch
```

在网站项目目录中运行，skill 会逐步引导完成所有检查项。

### 第二步：SEO 基础配置

参考 `seo-checklist.md`，确认以下文件已正确配置：

- [ ] `robots.txt` — 允许爬虫 + 声明 sitemap 地址
- [ ] `sitemap.xml` — 包含所有页面 URL
- [ ] `llms.txt` — AI 搜索引擎摘要
- [ ] JSON-LD 结构化数据（WebSite、Organization、页面专属 schema）
- [ ] meta 标签（title、description、OG、Twitter Card）
- [ ] `_headers` — Content-Type + Cache-Control

### 第三步：搜索引擎上报

参考 `search-console.md`，完成：

- [ ] Google Search Console 验证 + 提交 sitemap
- [ ] 百度站长工具验证 + 主动推送（使用 `scripts/submit-baidu.sh`）
- [ ] Bing Webmaster Tools 提交

### 第四步：性能优化

参考 `performance.md`，检查 Core Web Vitals：

- [ ] LCP < 2.5s
- [ ] CLS < 0.1
- [ ] INP < 200ms
- [ ] 字体异步加载（避免 FOIT）
- [ ] 第三方脚本延迟加载（Analytics、Clarity 等）

### 第五步：验证上线状态

```bash
# 验证响应头
./scripts/check-headers.sh https://yourdomain.com
```

## 相关文档

- [SEO 详细清单](./seo-checklist.md)
- [性能优化指南](./performance.md)
- [搜索引擎上报步骤](./search-console.md)
- [可用模板](../../templates/)
- [自动化脚本](../../scripts/)
