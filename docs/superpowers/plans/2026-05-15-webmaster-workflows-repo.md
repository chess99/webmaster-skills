# Webmaster Workflows Repo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立 `webmaster-workflows` 仓库，作为个人站长所有工作流的知识库和 skill 中心，可复用到任意网站。

**Architecture:** 仓库本身不部署任何网站，只存放工作流文档、脚本、和 skill 定义。每个工作域（SEO/性能/数据分析/内容更新）有独立目录，每个目录包含操作手册和可执行脚本。

**Tech Stack:** Markdown 文档 + Node.js/Python 脚本（零依赖优先）+ Claude Code skill 引用

---

## 当前状态

仓库已创建：`/Users/zcs/code2/webmaster-workflows`，只有初始 commit。

已完成的工作（在 coding-plan 项目中积累，需迁移/记录到这里）：
- `static-site-post-launch` skill：`/Users/zcs/.claude/skills/static-site-post-launch/SKILL.md`
- coding-plan 项目的 `scripts/fetch-arena-ranks.js`（数据抓取脚本范例）

---

## 目录结构设计

```
webmaster-workflows/
├── README.md                      # 仓库用途 + 快速导航
├── CLAUDE.md                      # AI agent 入口：告诉 Claude 这个仓库是什么
│
├── workflows/                     # 核心工作流文档（按域分类）
│   ├── post-launch/               # 新站上线后优化
│   │   ├── README.md              # 工作流概述 + 执行顺序
│   │   ├── seo-checklist.md       # SEO 执行清单（详细版）
│   │   ├── performance.md         # Core Web Vitals 优化指南
│   │   └── search-console.md     # 搜索引擎上报操作步骤
│   │
│   ├── content-refresh/           # 内容定期维护
│   │   └── README.md              # 如何更新/检查内容过期
│   │
│   └── analytics/                 # 数据分析工作流（待扩展）
│       └── README.md
│
├── scripts/                       # 可执行脚本
│   ├── generate-sitemap.js        # 扫描 src/ 目录自动生成 sitemap.xml
│   ├── submit-baidu.sh            # 百度主动推送所有 URL
│   └── check-headers.sh           # 验证线上 Content-Type 响应头
│
├── templates/                     # 可复制的模板文件
│   ├── robots.txt                 # 含 AI 机器人白名单的标准 robots.txt
│   ├── _headers                   # Cloudflare Pages 响应头配置
│   ├── llms.txt.tmpl              # llms.txt 模板（含占位符）
│   ├── sitemap.xml.tmpl           # 单语言 sitemap 模板
│   ├── sitemap-multilang.xml.tmpl # 多语言 hreflang sitemap 模板
│   └── schema/                    # JSON-LD schema 模板集合
│       ├── website-org.json       # WebSite + Organization
│       ├── faqpage.json           # FAQPage
│       ├── product.json           # Product + offers
│       └── breadcrumb.json        # BreadcrumbList
│
└── skills/                        # 本仓库专属 skill（非 ~/.claude/skills）
    └── README.md                  # 说明：通用 skill 在 ~/.claude/skills/，
                                   # 项目特定的放这里
```

---

## Task 1：完善 README 和 CLAUDE.md

**Files:**
- Modify: `README.md`
- Create: `CLAUDE.md`

- [ ] **Step 1: 写 README.md**

内容：仓库用途一句话、目录结构、快速开始（"新站上线了，跑 `/static-site-post-launch`"）

- [ ] **Step 2: 写 CLAUDE.md**

内容：告诉 Claude agent 这个仓库是什么，有哪些可用资源，skill 在哪里

```markdown
# webmaster-workflows

个人站长工作流知识库。

## 这个仓库是什么

可复用的网站运营工作流，覆盖：SEO 优化、性能调优、搜索引擎上报、数据分析。
不绑定任何具体项目，所有内容均为通用模板或工作流指引。

## 核心资源

- `workflows/` — 各工作域的操作手册
- `scripts/` — 可直接运行的自动化脚本
- `templates/` — 可复制粘贴的配置文件模板

## 关键 Skill

- `/static-site-post-launch` — 新站上线后 SEO + 性能完整清单（在 ~/.claude/skills/）
- `marketing-skills:seo-audit` — 全站 SEO 诊断
- `marketing-skills:schema-markup` — 结构化数据实现
- `marketing-skills:ai-seo` — AI 搜索引擎优化
- `web-performance-optimization` — Core Web Vitals 专项

## 使用方式

对新网站运行：`/static-site-post-launch`，按 skill 的清单逐步执行。
```

- [ ] **Step 3: 提交**

```bash
git add README.md CLAUDE.md
git commit -m "docs: add README and CLAUDE.md with repo overview"
```

---

## Task 2：创建 workflows 目录结构

**Files:**
- Create: `workflows/post-launch/README.md`
- Create: `workflows/post-launch/seo-checklist.md`
- Create: `workflows/post-launch/performance.md`
- Create: `workflows/post-launch/search-console.md`
- Create: `workflows/content-refresh/README.md`
- Create: `workflows/analytics/README.md`

- [ ] **Step 1: post-launch/README.md**

工作流概述 + 执行顺序（与 skill 对应，这里是更详细的人工参考文档）

- [ ] **Step 2: post-launch/seo-checklist.md**

从 `static-site-post-launch` skill 提取 SEO 相关内容，展开为完整操作手册

- [ ] **Step 3: post-launch/performance.md**

Core Web Vitals 优化，记录 coding-plan 实际做过的具体优化（Clarity 延迟、字体异步等）

- [ ] **Step 4: post-launch/search-console.md**

Google Search Console + 百度站长工具的详细操作步骤（含截图说明）

- [ ] **Step 5: 占位文档**

content-refresh 和 analytics 目录先放 README 说明"待扩展"，保留结构

- [ ] **Step 6: 提交**

```bash
git add workflows/
git commit -m "docs: add post-launch workflow docs (SEO, perf, search console)"
```

---

## Task 3：模板文件

**Files:**
- Create: `templates/robots.txt`
- Create: `templates/_headers`
- Create: `templates/llms.txt.tmpl`
- Create: `templates/sitemap.xml.tmpl`
- Create: `templates/sitemap-multilang.xml.tmpl`
- Create: `templates/schema/website-org.json`
- Create: `templates/schema/faqpage.json`
- Create: `templates/schema/product.json`
- Create: `templates/schema/breadcrumb.json`

- [ ] **Step 1: 从 coding-plan 提取实际用过的模板**

直接复制 `/Users/zcs/code2/coding-plan/src/robots.txt`、`_headers` 作为基础，替换具体域名为 `YOURDOMAIN` 占位符

- [ ] **Step 2: 写 JSON-LD 模板**

从 coding-plan 的 `src/index.html`、`src/plans/zhipu.html` 提取 schema 代码，去掉业务特定内容，保留通用结构

- [ ] **Step 3: 提交**

```bash
git add templates/
git commit -m "feat: add reusable templates (robots.txt, _headers, sitemap, JSON-LD schemas)"
```

---

## Task 4：工具脚本

**Files:**
- Create: `scripts/generate-sitemap.js`
- Create: `scripts/submit-baidu.sh`
- Create: `scripts/check-headers.sh`

- [ ] **Step 1: generate-sitemap.js**

扫描指定目录下的 `.html` 文件，自动生成 `sitemap.xml`。输入：目录路径 + 域名。零 npm 依赖（用 Node.js 内置模块）。

```js
// 用法：node generate-sitemap.js --dir ./dist --domain https://example.com
// 输出：sitemap.xml 到当前目录
const fs = require('fs');
const path = require('path');
// ... 实现
```

- [ ] **Step 2: submit-baidu.sh**

读取 sitemap.xml，提取所有 `<loc>` URL，批量提交到百度主动推送 API。

```bash
#!/bin/bash
# 用法：BAIDU_TOKEN=xxx DOMAIN=example.com ./submit-baidu.sh
```

- [ ] **Step 3: check-headers.sh**

对线上关键文件（`/robots.txt`、`/sitemap.xml`、`/llms.txt`）发 curl 请求，验证 Content-Type 响应头。

- [ ] **Step 4: 提交**

```bash
git add scripts/
git commit -m "feat: add automation scripts (sitemap gen, baidu push, header check)"
```

---

## 待扩展工作域（未来）

以下是规划中的工作流，等有具体项目经验后再填充：

- `workflows/analytics/` — GA4 数据分析、关键词排名追踪、流量异常诊断
- `workflows/content-refresh/` — 定期内容检查（过期信息、404 链接、竞品对比更新）
- `scripts/check-404.sh` — 扫描站内死链
- `scripts/fetch-rankings.js` — 基于 coding-plan 的 fetch-arena-ranks.js 抽象的通用排名抓取框架

---

## 自查清单

- [ ] README 包含"新站上线，我该怎么用这个仓库"的快速路径
- [ ] CLAUDE.md 里的 skill 引用都能在实际环境里触发
- [ ] 所有模板文件里的占位符格式统一（`YOURDOMAIN`、`YOUR_TOKEN` 等）
- [ ] 脚本有 `--help` 或注释说明用法
