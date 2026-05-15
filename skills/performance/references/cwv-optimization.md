# Core Web Vitals 优化参考

## 目标指标

| 指标 | 优秀 | 需改进 | 差 |
|---|---|---|---|
| LCP（最大内容绘制） | < 2.5s | 2.5–4s | > 4s |
| CLS（累积布局偏移） | < 0.1 | 0.1–0.25 | > 0.25 |
| INP（交互到下一帧） | < 200ms | 200–500ms | > 500ms |

检测工具：[PageSpeed Insights](https://pagespeed.web.dev/)、Chrome DevTools > Lighthouse

---

## 字体优化

字体是 LCP 和 CLS 的主要来源。

### 异步加载 Google Fonts（避免 FOIT）

```html
<!-- preconnect 提前建立连接 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- 异步加载，onload 触发后切换 rel -->
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap"
      as="style" onload="this.onload=null;this.rel='stylesheet'">

<!-- 无 JS 降级 -->
<noscript>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
</noscript>
```

### 在 CSS 中声明 font-display

```css
@font-face {
  font-display: swap; /* 先用系统字体渲染，字体加载完成后替换 */
}
```

---

## 第三方脚本延迟加载

分析脚本（GA4、Microsoft Clarity 等）不需要首屏同步执行。

### 方案 1：defer/async

```html
<!-- 对于不依赖 DOM 的脚本 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXX"></script>
```

### 方案 2：用户交互后加载（最激进，LCP 提升最显著）

```js
// 用户首次交互后再加载 Clarity
function loadClarity() {
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "YOUR_CLARITY_ID");
}

['click', 'scroll', 'keydown', 'touchstart'].forEach(e =>
  window.addEventListener(e, loadClarity, { once: true, passive: true })
);
```

同样的模式适用于任何第三方脚本（把 `loadClarity` 替换为加载目标脚本的逻辑）。

---

## 图片优化

```html
<!-- 首屏关键图片：preload + fetchpriority -->
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">

<!-- 非首屏图片：lazy load -->
<img src="image.webp" loading="lazy" decoding="async" width="800" height="600" alt="...">
```

- 使用 WebP/AVIF 格式（比 JPEG 小 30-50%）
- 始终声明 `width` 和 `height`（防止 CLS）
- 首屏图片不加 `loading="lazy"`

---

## 实测优化记录

以下优化在实际项目中验证有效：

| 优化 | 效果 |
|---|---|
| Google Fonts 改为 `preload` + `onload` 异步加载 | LCP -0.5s，消除 FOIT |
| Microsoft Clarity 改为用户交互后加载 | LCP -0.3s，TBT 降低 |
| 图片添加 `width`/`height` 属性 | CLS 从 0.15 降至 0.02 |

---

## 快速诊断命令

```bash
# PageSpeed Insights API（移动端）
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://YOURDOMAIN&strategy=mobile"

# 桌面端
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://YOURDOMAIN&strategy=desktop"

# 用 Lighthouse CLI（需要 Node.js）
npx lighthouse https://YOURDOMAIN --only-categories=performance --output=json
```

---

## TTFB 优化

Time to First Byte > 600ms 通常是托管问题，不是代码问题：

- 从源站迁移到 CDN-edge 部署（Cloudflare Pages、Vercel、Netlify）
- 确认已启用 HTTP/2
- 静态资源加长期缓存：`Cache-Control: public, max-age=31536000, immutable`
- 如果用 Cloudflare，开启 Rocket Loader（谨慎，会影响 JS 执行顺序）
