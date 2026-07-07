# SEO Research Evidence And Exports

Use this reference when collecting or validating evidence for `seo-research`.

## Evidence Strength

| Evidence | Strong for | Weak for |
|---|---|---|
| Google Search Console export | Owned queries, pages, impressions, CTR, average position | Competitor rankings |
| Semrush/Ahrefs/DataForSEO/5118/Aizhan export | Competitor keyword estimates, ranking URLs, keyword gaps | Exact traffic or conversions |
| Public HTML and sitemap | On-page targeting, crawlable page inventory | Rankings, search volume, traffic |
| Public SERP observation | Directional search landscape and visible competitors | Stable rank, personalization-free results |
| Google Trends/Baidu Index | Directional demand movement | Owned ranking or business value |
| Similarweb export | Directional traffic/channel/geography comparison | Keyword-level ranking |
| Backlink export | Referring-domain and authority gap diagnosis | Direct ranking causality |
| AI answer screenshot/log | Citation behavior for exact prompt/platform/date | Universal AI visibility |

## Minimum Export Fields

### Owned GSC Query/Page Export

Required fields: `query`, `page`, `clicks`, `impressions`, `ctr`, `position`, `date_range`, plus `country` and `device` when available.

Quality gate:

- Pages must belong to the user's domain.
- Include at least one non-header data row.
- Keep date range visible in the file or summary.

### Competitor Keyword Export

Required fields: `competitor_domain`, `keyword`, `ranking_url`, `position`, `volume`, `difficulty`, `traffic_estimate`, `source_tool`, `source_date`.

Quality gate:

- `competitor_domain` must match the competitor being analyzed.
- Do not mix multiple tools without a `source_tool` value.
- Treat volume and traffic as estimates, not exact facts.

### Trend Opportunity Log

Required fields: `term`, `market`, `source`, `source_date`, `trend_direction`, `related_queries`, `opportunity_note`, `evidence_label`.

Quality gate:

- Use the platform's native terms where possible.
- Do not convert trend indexes into search volume.

### Similarweb Or Traffic Export

Required fields: `domain`, `date_range`, `visits` or `traffic_estimate`, `traffic_channel`, `country`, `source_tool`, `source_date`.

Quality gate:

- Include both the user's site and the competitor when making comparisons.
- Use directional language such as "appears higher" or "estimated", not exact traffic claims.

### Backlink Export

Required fields: `target_domain`, `referring_domain`, `source_url`, `target_url`, `anchor`, `link_type`, `authority_metric`, `source_tool`, `source_date`.

Quality gate:

- Keep owned and competitor exports separate before summarizing.
- Do not claim causality from backlink count alone.

### AI Answer Log

Required fields: `platform`, `prompt`, `checked_at`, `answer_present`, `cited_sites`, `owned_site_cited`, `competitor_site_cited`, `screenshot_or_log_path`.

Quality gate:

- Record exact prompts.
- Include screenshot or saved log path for every claim.
- Avoid broad statements such as "AI cites us" unless platform/date/prompt coverage supports it.

## Privacy Rule

Private exports should stay in the user's project workspace or a private data folder, not inside the public skill plugin. Public plugin files should contain schemas, examples, and workflows only.
