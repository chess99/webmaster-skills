除非用户主动要求切分支，否则一般都直接在主分支或当前需求分支进行开发。
除非用户主动指定语言，否则 README 之类的文档都用中文。
每完成一个完整迭代（实现、验证、必要文档更新都结束）后，主动提交本次自己修改的文件，不等用户额外要求。提交时只包含本次自己修改的内容，禁止提交其他 agent 或用户并行修改的文件。提交前用 git diff --staged 确认暂存区只包含本次变更。

--- project-doc ---

# webmaster-skills

Codex 和 Claude Code 插件：面向独立开发者的产品发现、建站与增长技能集合。

## Skills

### Product Discovery

- `find-product-opportunities` — 自主发现、验证并排序软件产品机会，交付 Top 3 与主推荐或 NO-GO

### Webmaster

- `performance` — Core Web Vitals 诊断与优化
- `post-launch` — 新站上线工作流，会编排其他技能
- `seo-research` — SEO 调研工作流：竞对关键词、关键词缺口、热词机会、相似网站发现、对比页/alternative 页规划、排名诊断、AI 搜索引用检查
- `search-console` — 搜索引擎提交，包括 GSC、百度、Bing
- `link-ops` — 外链运营系统：竞品反查、机会发现/评分、渠道库、外联准备与效果复盘

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
tests/            first-party skill tests
vendor/marketing/ vendored from coreyhaines31/marketingskills v2.0
.claude/skills    points to skills/, auto-discovered by Claude Code
.agents/skills    points to skills/, auto-discovered by Codex-compatible agents
.catpaw/skills    points to skills/, auto-discovered by CatPaw-compatible agents
```

## Opportunity Research Rules

- `find-product-opportunities` 必须由 Agent 主导完整研究，不得把选词、切换数据页面、整理证据或最终排序交回用户手工完成。
- 公开证据应足以完成基础报告；登录浏览器、付费工具和用户导出只能增强置信度，不能成为硬依赖。
- 不得把趋势指数、SERP 数量、页面文案或模型推断表述为搜索量、排名、流量、收入或付费意愿事实。
- 必须主动寻找反证；证据不足时输出 NO-GO，不得为凑足 Top 3 编造候选或来源。
- 研究默认只在对话中交付。只有用户明确要求保存时才创建研究工件，且私有导出、登录数据和研究工件不得提交到本公开仓库。
- 不自动注册服务、联系潜在客户、购买数据、发布内容或开始开发；这些动作需要单独授权。

## Link Ops Rules

- `link-ops` 的默认输出是研究、prospect 数据、评分、行动队列和草稿；提交目录、发邮件/DM、评论、注册、互链和购买 placement 等外部状态变更需要用户明确授权。
- 不把 backlink 数量、DR/DA 或 dofollow 比例当作目标本身；优先独立 referring domains、主题相关性、编辑选择性、真实 referral 和可复用渠道资产。
- 不自动化批量评论、论坛签名、低质量目录、PBN/站群、规模化互链或其他明显 link-spam。
- 用户提供的 backlink 导出、联系人和 campaign workspace 属于私有运行数据，不得提交到本公开仓库。

## Editing Rules

**Do not modify files under `vendor/`** unless explicitly asked. These are vendored verbatim from upstream. Changes create a diff that's hard to reconcile when updating.

Root `AGENTS.md` and `skills/` are the canonical instruction and skill sources. Compatibility entry points must reference them instead of duplicating content.

Opportunity Radar and Link Ops helper code use only the Python 3.11+ standard library. New helper behavior requires tests, and all tests plus official Skill/plugin validation must pass before committing.

## Skill Format

Each skill: one directory + `SKILL.md` with YAML frontmatter (`name` + `description`). Optional `references/`, `scripts/`, `assets/`, and `evals/` directories hold resources loaded or executed on demand.
