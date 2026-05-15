# 搜索引擎上报操作步骤

## Google Search Console

### 1. 添加网站（首次）

1. 打开 [Google Search Console](https://search.google.com/search-console/)
2. 点击「添加资源」→ 选择「网址前缀」
3. 输入 `https://YOURDOMAIN`
4. 选择验证方式：

**推荐：HTML 文件验证**

下载验证文件（如 `google1234abcd.html`），上传到网站根目录，确认可访问后点「验证」。

**备选：DNS TXT 记录**

在域名 DNS 管理处添加 TXT 记录，等待 DNS 生效（可能需要几分钟到几小时）。

### 2. 提交 Sitemap

1. 左侧菜单 → 「索引」→「Sitemap」
2. 输入 sitemap URL：`sitemap.xml`
3. 点击「提交」

状态显示「成功」后，Google 会定期抓取 sitemap 中的所有 URL。

### 3. 申请编入索引（可选加速）

对重要页面手动申请：

1. 顶部搜索栏输入完整 URL
2. 点击「请求编入索引」
3. 等待处理（通常 1-3 天）

每天申请配额有限，只对核心页面使用。

### 4. 日常监控

- **覆盖率报告**：检查「已排除」的 URL，确认没有重要页面被意外排除
- **效果报告**：查看展示次数、点击率、平均排名
- **核心网页体验**：验证 CWV 是否通过

---

## 百度站长工具

### 1. 添加网站

1. 打开 [百度搜索资源平台](https://ziyuan.baidu.com/)
2. 注册/登录百度账号
3. 「用户中心」→「站点管理」→「添加网站」
4. 输入网站 URL，选择验证方式

**推荐：文件验证**（同 Google）

### 2. 主动推送（批量）

使用 `scripts/submit-baidu.sh` 脚本批量推送所有 URL：

```bash
BAIDU_TOKEN=你的推送token DOMAIN=yourdomain.com ./scripts/submit-baidu.sh
```

Token 在百度站长平台 →「数据引入」→「链接提交」→「主动推送」中获取。

**手动单条推送（测试用）：**

```bash
curl -H 'Content-Type:text/plain' \
  --data-binary @urls.txt \
  "https://data.zz.baidu.com/urls?site=https://YOURDOMAIN&token=YOUR_TOKEN"
```

`urls.txt` 每行一个 URL，每次最多 2000 条，每天配额 10000 条。

### 3. 抓取诊断

「工具」→「抓取诊断」→ 输入 URL → 提交抓取，验证百度蜘蛛能正常访问。

---

## Bing Webmaster Tools

1. 打开 [Bing Webmaster Tools](https://www.bing.com/webmasters/)
2. 使用 Microsoft 账号登录
3. 「添加网站」→ 输入 URL
4. 提交 sitemap：「Sitemaps」→「提交 sitemap」→ 输入 `https://YOURDOMAIN/sitemap.xml`

Bing 的索引收录通常与 Google 同步（通过 IndexNow 协议），优先级低于 Google 和百度。

---

## 快速自查

- [ ] Google Search Console 已验证，sitemap 提交成功
- [ ] 百度站长工具已验证，主动推送脚本测试通过
- [ ] Bing Webmaster Tools sitemap 已提交
- [ ] 等待 1-7 天后，用 `site:yourdomain.com` 检查各搜索引擎收录情况
