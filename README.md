# webmaster-workflows

个人站长可复用工作流知识库，覆盖 SEO、性能、搜索引擎上报、内容维护。不绑定任何具体项目。

## 快速开始

**新站刚上线？**

```
/static-site-post-launch
```

在任意网站项目中运行该 skill，按清单逐步执行 SEO + 性能完整优化。

## 目录结构

```
webmaster-workflows/
├── workflows/                 # 操作手册（按工作域分类）
│   ├── post-launch/           # 新站上线后优化
│   │   ├── README.md          # 执行顺序总览
│   │   ├── seo-checklist.md   # SEO 完整清单
│   │   ├── performance.md     # Core Web Vitals 优化
│   │   └── search-console.md  # 搜索引擎上报步骤
│   ├── content-refresh/       # 内容定期维护（待扩展）
│   └── analytics/             # 数据分析（待扩展）
│
├── scripts/                   # 可直接运行的自动化脚本
│   ├── generate-sitemap.js    # 扫描 HTML 文件生成 sitemap.xml
│   ├── submit-baidu.sh        # 百度主动推送所有 URL
│   └── check-headers.sh       # 验证线上响应头
│
└── templates/                 # 可复制粘贴的配置模板
    ├── robots.txt
    ├── _headers               # Cloudflare Pages 响应头
    ├── llms.txt.tmpl
    ├── sitemap.xml.tmpl
    ├── sitemap-multilang.xml.tmpl
    └── schema/                # JSON-LD 结构化数据模板
        ├── website-org.json
        ├── faqpage.json
        ├── product.json
        └── breadcrumb.json
```

## 相关 Skills

| Skill | 用途 |
|---|---|
| `/static-site-post-launch` | 新站上线完整清单（SEO + 性能 + 上报） |
| `marketing-skills:seo-audit` | 全站 SEO 诊断 |
| `marketing-skills:schema-markup` | 结构化数据实现 |
| `marketing-skills:ai-seo` | AI 搜索引擎优化 |
| `web-performance-optimization` | Core Web Vitals 专项优化 |
