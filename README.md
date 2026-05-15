# webmaster-skills

Webmaster skills for indie site owners. Works with Claude Code and any agent that supports the [Agent Skills spec](https://agentskills.io).

## Install

```bash
/plugin install chess99/webmaster-skills
```

Also install [marketing-skills](https://github.com/coreyhaines31/marketingskills) — the `post-launch` skill builds on it:

```bash
/plugin install coreyhaines31/marketingskills
```

## Available Skills

| Skill | Description |
|-------|-------------|
| [performance](skills/performance/) | Diagnose and fix Core Web Vitals (LCP, CLS, INP). Runs PageSpeed Insights automatically and gives targeted fixes. |
| [post-launch](skills/post-launch/) | Full post-launch workflow for new sites — validates files, orchestrates schema, AI SEO, performance, search engine submission, and analytics setup in order. |
| [search-console](skills/search-console/) | Submit your site to Google Search Console, Baidu, and Bing. Handles verification, sitemap submission, and Baidu active push via curl. |

## How Skills Work Together

`post-launch` is the entry point — it calls the other skills in the right order:

```
post-launch
  ├── 1. Validate robots.txt / sitemap.xml / llms.txt
  ├── 2. marketing-skills:schema
  ├── 3. marketing-skills:ai-seo
  ├── 4. webmaster-skills:performance  ←
  ├── 5. webmaster-skills:search-console  ←
  └── 6. marketing-skills:analytics
```

## Contributing

PRs welcome. Each skill is a single `SKILL.md` file under `skills/<name>/`. See [Agent Skills spec](https://agentskills.io/specification.md) for format requirements.
