# webmaster-skills Plugin Design

**Date:** 2026-05-15
**Goal:** 把 `webmaster-workflows` 仓库重构为可发布的 Claude Code plugin，命名为 `webmaster-skills`，对标 marketing-skills 的形式和发布方式。

---

## 背景

当前仓库（`webmaster-workflows`）是一个"知识库 + 脚本"形式的仓库，包含 `workflows/`、`templates/`、`scripts/` 目录。这个形式与目标（可安装 plugin）不符。

**目标形式**：和 [marketing-skills](https://github.com/coreyhaines31/marketingskills) 完全一致——纯 skill 集合，通过 `/plugin install` 安装，工具无关、框架无关，面向所有独立站长。

---

## 仓库结构

```
webmaster-skills/
├── .claude-plugin/
│   ├── plugin.json        # Claude Code plugin 元数据
│   └── marketplace.json   # 插件市场清单
├── skills/
│   ├── performance/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── cwv-optimization.md
│   ├── post-launch/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── checklist.md
│   └── search-console/
│       ├── SKILL.md
│       └── references/
│           └── submit-engines.md
├── CLAUDE.md
└── README.md
```

**删除**：`workflows/`、`templates/`、`scripts/`、`docs/`（含本 spec，在实现前提交）

---

## Plugin 元数据

### `.claude-plugin/plugin.json`

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

### `.claude-plugin/marketplace.json`

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

---

## Skill 定义

### 1. `performance`

**触发词**：网站慢、LCP、CLS、INP、Core Web Vitals、CWV、PageSpeed 分低、网页速度、性能优化、web vitals

**Skill 行为**：
1. 用 PageSpeed Insights API（`curl`，零工具依赖）诊断目标 URL
2. 根据实际诊断结果对症给出优化建议，而不是通用清单
3. 覆盖的优化领域：字体异步加载、第三方脚本延迟加载（GA/Clarity 等）、图片优化（格式/尺寸/lazy load）、TTFB、CSS/JS 阻塞

**references/**：
- `cwv-optimization.md`：从现有 `workflows/post-launch/performance.md` 迁移，补充更多实战案例

**与其他 skill 的边界**：
- `marketing-skills:seo-audit` 里的 CWV 章节只是检查清单；本 skill 负责深度诊断和修复
- 被 `post-launch` skill 在第四步调用

---

### 2. `post-launch`

**触发词**：新站上线、刚部署完、上线后该做什么、post-launch、网站上线了、上线清单

**Skill 行为**：编排 workflow，按顺序调度其他 skill，自身不重复实现已有 skill 的内容。

执行顺序：
1. **基础文件验证**（AI 直接用 `curl` 检查）：`/robots.txt`、`/sitemap.xml`、`/llms.txt` 是否存在且 Content-Type 正确
2. **结构化数据** → 调用 `marketing-skills:schema`
3. **AI 搜索优化** → 调用 `marketing-skills:ai-seo`（含 llms.txt）
4. **性能优化** → 调用 `webmaster-skills:performance`
5. **搜索引擎提交** → 调用 `webmaster-skills:search-console`
6. **统计接入** → 调用 `marketing-skills:analytics`，并补充百度统计接入说明（复制 JS 片段到 `<head>`）

**前置条件说明**：步骤 2-6 依赖 marketing-skills 已安装。Skill 开头注明依赖。

**references/**：
- `checklist.md`：每个步骤的详细自查项，从现有 `seo-checklist.md` 迁移

---

### 3. `search-console`

**触发词**：Google Search Console、GSC、百度站长、百度收录、提交 sitemap、搜索引擎上报、主动推送、Bing Webmaster、网站验证、索引提交

**Skill 行为**：
1. **Google Search Console**：验证网站所有权（文件验证 / DNS TXT）→ 提交 sitemap → 对核心页面申请手动索引
2. **百度站长工具**：验证 → 主动推送（AI 直接执行 `curl` 命令，读取用户提供的 sitemap URL 提取 `<loc>`，批量推送到百度 API）
3. **Bing Webmaster Tools**：提交 sitemap（可选，优先级低）

**AI 可执行操作**：百度主动推送全程可由 AI 完成（curl 命令），GSC 的 sitemap 提交需要用户在浏览器操作（AI 给出步骤说明）。

**references/**：
- `submit-engines.md`：各引擎的 API 文档、token 获取路径、推送配额说明

---

## CLAUDE.md（更新后内容）

```markdown
# webmaster-skills

Claude Code plugin — 面向独立站长的 webmaster skill 集合。

## 这个仓库是什么

可安装的 skill plugin，提供 3 个互补的 webmaster skill：
- `performance` — Core Web Vitals 诊断与优化
- `post-launch` — 新站上线完整 workflow（编排其他 skill）
- `search-console` — 搜索引擎上报（GSC、百度、Bing）

## 安装

（待 GitHub 仓库创建后填写 /plugin install 命令）

## 依赖

`post-launch` skill 会调用 marketing-skills。建议同时安装：
/plugin install coreyhaines31/marketingskills

## Skill 格式

遵循 Agent Skills spec：每个 skill 一个目录，SKILL.md 含 YAML frontmatter（name + description）。
```

---

## README.md（结构）

- 一句话介绍
- 安装命令
- Skill 列表（表格，对齐 marketing-skills 风格）
- 依赖说明（marketing-skills）
- Contributing

---

## 迁移说明

| 现有文件 | 处置 |
|---|---|
| `workflows/post-launch/performance.md` | 迁移到 `skills/performance/references/cwv-optimization.md` |
| `workflows/post-launch/seo-checklist.md` | 迁移到 `skills/post-launch/references/checklist.md` |
| `workflows/post-launch/search-console.md` | 迁移到 `skills/search-console/references/submit-engines.md` |
| `workflows/post-launch/README.md` | 内容折叠进 `skills/post-launch/SKILL.md` |
| `workflows/content-refresh/README.md` | 删除（待扩展，暂不做 skill） |
| `workflows/analytics/README.md` | 删除（由 marketing-skills:analytics 覆盖） |
| `templates/` | 删除（模板不属于 skill 形式） |
| `scripts/` | 删除（脚本逻辑折叠进 `search-console` skill 的 references） |
| `docs/superpowers/plans/` | 删除（历史计划文档，已执行完） |

---

## 自查

- [x] 无 TBD 或占位符
- [x] 三个 skill 边界清晰，不重复 marketing-skills 已有内容
- [x] plugin.json / marketplace.json 格式对齐 marketing-skills
- [x] 迁移路径明确，无内容丢失（均有目标位置）
- [x] `post-launch` 依赖声明明确
