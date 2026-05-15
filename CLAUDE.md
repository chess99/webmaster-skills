# webmaster-skills

Claude Code plugin — webmaster skill collection for indie site owners.

## Skills

- `performance` — Core Web Vitals diagnosis and optimization
- `post-launch` — New site launch workflow (orchestrates other skills)
- `search-console` — Search engine submission (GSC, Baidu, Bing)

## Install

```bash
/plugin install chess99/webmaster-skills
```

## Dependencies

`post-launch` calls marketing-skills. Install both:

```bash
/plugin install coreyhaines31/marketingskills
/plugin install chess99/webmaster-skills
```

## Skill Format

Each skill: one directory + `SKILL.md` with YAML frontmatter (`name` + `description`). Optional `references/` subdirectory for detailed docs loaded on demand.
