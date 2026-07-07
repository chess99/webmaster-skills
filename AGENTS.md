除非用户主动要求切分支，否则一般都直接在主分支或当前需求分支进行开发。
除非用户主动指定语言，否则 README 之类的文档都用中文。
每完成一个完整迭代（实现、验证、必要文档更新都结束）后，主动提交本次自己修改的文件，不等用户额外要求。提交时只包含本次自己修改的内容，禁止提交其他 agent 或用户并行修改的文件。提交前用 git diff --staged 确认暂存区只包含本次变更。

--- project-doc ---

# webmaster-skills

Codex 和 Claude Code 插件：面向独立站长的 webmaster 技能集合。

## Skills

### Webmaster

- `performance` — Core Web Vitals 诊断与优化
- `post-launch` — 新站上线工作流，会编排其他技能
- `seo-research` — SEO 调研工作流：竞对关键词、关键词缺口、热词机会、相似网站发现、对比页/alternative 页规划、排名诊断、AI 搜索引用检查
- `search-console` — 搜索引擎提交，包括 GSC、百度、Bing

### Marketing (from [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills))

- `seo-audit` / `ai-seo` / `programmatic-seo` / `site-architecture` / `schema` — SEO & Discovery
- `cro` / `signup` / `onboarding` / `popups` / `paywalls` — Conversion Optimization
- `copywriting` / `copy-editing` / `cold-email` / `emails` / `social` / `image` — Content & Copy
- `ads` / `ad-creative` — Paid & Distribution
- `analytics` / `ab-testing` — Measurement & Testing
- `referrals` / `free-tools` / `co-marketing` / `community-marketing` / `churn-prevention` — Growth
- `marketing-ideas` / `marketing-psychology` / `launch` / `pricing` — Strategy
- `revops` / `sales-enablement` / `competitors` / `competitor-profiling` / `directory-submissions` / `aso` / `lead-magnets` / `customer-research` / `video` / `product-marketing` — Sales & Other

## Install

```bash
/plugin install chess99/webmaster-skills
```

## Directory Structure

```text
skills/           first-party skills (this repo)
vendor/marketing/ vendored from coreyhaines31/marketingskills v2.0
.claude/skills    points to skills/, auto-discovered by Claude Code
.agents/skills    points to skills/, auto-discovered by Codex-compatible agents
```

## Editing Rules

**Do not modify files under `vendor/`** unless explicitly asked. These are vendored verbatim from upstream. Changes create a diff that's hard to reconcile when updating.

## Skill Format

Each skill: one directory + `SKILL.md` with YAML frontmatter (`name` + `description`). Optional `references/` subdirectory for detailed docs loaded on demand.
