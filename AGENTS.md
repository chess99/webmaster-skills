# webmaster-skills

Codex and Claude Code plugin — webmaster skill collection for indie site owners.

## Skills

### Webmaster
- `performance` — Core Web Vitals diagnosis and optimization
- `post-launch` — New site launch workflow (orchestrates other skills)
- `search-console` — Search engine submission (GSC, Baidu, Bing)

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

```
skills/           ← first-party skills (this repo)
vendor/marketing/ ← vendored from coreyhaines31/marketingskills v2.0
.claude/skills/   ← symlink to skills/, auto-discovered by Claude Code
.agents/skills/   ← symlink to skills/, auto-discovered by Codex-compatible agents
```

## Editing Rules

**Do not modify files under `vendor/`** unless explicitly asked. These are vendored verbatim from upstream. Changes create a diff that's hard to reconcile when updating.

## Skill Format

Each skill: one directory + `SKILL.md` with YAML frontmatter (`name` + `description`). Optional `references/` subdirectory for detailed docs loaded on demand.
