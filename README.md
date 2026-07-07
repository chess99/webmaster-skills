# webmaster-skills

面向独立站长的 Codex / Claude Code 技能集合，用来处理新站上线、性能、搜索提交、SEO 调研等常见站长工作。

## 安装

```bash
/plugin install chess99/webmaster-skills
```

`post-launch` 会编排部分营销技能，建议同时安装 [marketing-skills](https://github.com/coreyhaines31/marketingskills)：

```bash
/plugin install coreyhaines31/marketingskills
```

## 可用技能

| Skill | Description |
|---|---|
| [performance](skills/performance/) | 诊断和优化 Core Web Vitals，包括 LCP、CLS、INP、TTFB 和 PageSpeed 问题。 |
| [post-launch](skills/post-launch/) | 新站上线后的完整检查流程：基础文件、结构化数据、AI SEO、性能、搜索提交、统计。 |
| [seo-research](skills/seo-research/) | SEO 调研流程：竞对关键词、关键词缺口、热词机会、相似网站、对比页/alternative 页、排名诊断、AI 搜索引用检查。 |
| [search-console](skills/search-console/) | 提交站点到 Google Search Console、百度站长和 Bing，包括验证、sitemap 提交、百度主动推送。 |

## 技能如何配合

`post-launch` 适合新站刚上线时使用，它会按顺序调用其他技能：

```text
post-launch
  1. 校验 robots.txt / sitemap.xml / llms.txt
  2. marketing-skills:schema
  3. marketing-skills:ai-seo
  4. webmaster-skills:performance
  5. webmaster-skills:search-console
  6. marketing-skills:analytics
```

`seo-research` 适合在上线前后决定下一批页面要做什么，例如竞品对比页、alternative 页、关键词缺口内容、热词驱动的小工具、AI 搜索引用优化。

## 目录结构

```text
skills/           first-party skills
vendor/marketing/ vendored from coreyhaines31/marketingskills v2.0
.claude/skills    points to skills/ for Claude Code discovery
.agents/skills    points to skills/ for Codex-compatible agents
```

## 编辑规则

不要直接修改 `vendor/` 下的文件，除非是在同步上游 vendored 版本。这些文件来自外部项目，随意改动会让后续更新变难。

每个技能是一个目录加一个 `SKILL.md`，可选 `references/` 存放按需读取的详细说明。

## 贡献

欢迎 PR。技能格式参考 [Agent Skills spec](https://agentskills.io/specification.md)。
