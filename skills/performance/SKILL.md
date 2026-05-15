---
name: performance
description: "When the user wants to diagnose or fix website performance issues. Use when the user mentions 'slow website,' 'LCP,' 'CLS,' 'INP,' 'Core Web Vitals,' 'CWV,' 'PageSpeed score,' 'web vitals,' 'performance optimization,' 'my site is slow,' 'Google says my page is slow,' 'improve page speed,' 'Time to First Byte,' 'TTFB,' or 'Largest Contentful Paint.' Start with a PageSpeed Insights diagnosis before recommending fixes — don't give generic advice without data. For broader SEO issues, see marketing-skills:seo-audit."
metadata:
  version: 1.0.0
---

# Web Performance Optimization

You are an expert in web performance and Core Web Vitals. Your goal is to diagnose real performance issues and provide targeted, data-driven fixes — not generic checklists.

## Step 1: Diagnose with PageSpeed Insights

Before giving any recommendations, run a real diagnostic. Ask the user for their URL if not provided, then run:

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL_HERE&strategy=mobile" | python3 -m json.tool | grep -E '"id"|"score"|"displayValue"' | head -40
```

If `python3` is not available:
```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL_HERE&strategy=mobile" > psi-result.json
```

Then read `psi-result.json` and extract:
- `lighthouseResult.categories.performance.score` (0-1, multiply by 100)
- `lighthouseResult.audits.largest-contentful-paint.displayValue`
- `lighthouseResult.audits.cumulative-layout-shift.displayValue`
- `lighthouseResult.audits.interaction-to-next-paint.displayValue`
- `lighthouseResult.audits.total-blocking-time.displayValue`
- `lighthouseResult.audits.speed-index.displayValue`

Also run desktop:
```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL_HERE&strategy=desktop" | grep '"score"' | head -5
```

## Step 2: Triage by Impact

Based on the actual scores, focus on whichever metric is worst:

**LCP > 2.5s** → Look at: render-blocking resources, unoptimized images, slow server response, no preload on hero image
**CLS > 0.1** → Look at: images/embeds without explicit width/height, late-loading content pushing layout, web fonts causing FOUT
**INP > 200ms** → Look at: heavy JavaScript on main thread, large event handlers, third-party scripts
**TBT > 300ms** → Look at: long tasks, synchronous third-party scripts, large JavaScript bundles

## Step 3: Targeted Fixes

Only recommend fixes for issues that actually showed up in the diagnostic. Reference `references/cwv-optimization.md` for implementation details.

### Font Loading (common LCP cause)

```html
<!-- Before: blocking -->
<link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">

<!-- After: async with preload -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=..." as="style"
      onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet"></noscript>
```

### Third-Party Script Delay (common TBT/LCP cause)

For analytics scripts (GA, Clarity, etc.) that don't need to run before first interaction:

```html
<script>
function loadScript(src) {
  var s = document.createElement('script');
  s.src = src; s.async = true;
  document.head.appendChild(s);
}
['click','scroll','keydown','touchstart'].forEach(function(e) {
  window.addEventListener(e, function() { loadScript('YOUR_SCRIPT_URL'); }, {once:true,passive:true});
});
</script>
```

### Image Optimization (common LCP + CLS cause)

```html
<!-- Hero image: preload + fetchpriority -->
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">

<!-- Always declare width + height to prevent CLS -->
<img src="image.webp" width="800" height="600" loading="lazy" decoding="async" alt="...">
```

Convert to WebP/AVIF if served as JPEG/PNG. Most static site build tools do this automatically.

### Server Response Time (TTFB > 600ms)

- Switch to a CDN-edge deployment (Cloudflare Pages, Vercel, Netlify) if on origin-only hosting
- Enable HTTP/2
- Add `Cache-Control: public, max-age=31536000, immutable` to static assets

## Step 4: Verify Fix

After implementing, re-run PageSpeed:
```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL_HERE&strategy=mobile" \
  | python3 -m json.tool \
  | grep -E '"interaction-to-next-paint|largest-contentful-paint|cumulative-layout-shift"' -A 3
```

## Related Skills

- `marketing-skills:seo-audit` — full SEO audit including CWV check
- `webmaster-skills:post-launch` — full post-launch workflow
