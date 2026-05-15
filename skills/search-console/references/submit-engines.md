# Search Engine Submission Reference

搜索引擎上报详细操作步骤和 API 文档。

## Google Search Console

### 添加网站（首次）

1. 打开 [Google Search Console](https://search.google.com/search-console/)
2. 点击「添加资源」→ 选择「网址前缀」
3. 输入 `https://YOURDOMAIN`
4. 选择验证方式：

**推荐：HTML 文件验证**

下载验证文件（如 `google1234abcd.html`），上传到网站根目录，确认可访问后点「验证」。

**备选：DNS TXT 记录**

在域名 DNS 管理处添加 TXT 记录，等待 DNS 生效（可能需要几分钟到几小时）。

### 提交 Sitemap

左侧菜单 → 「索引」→「Sitemap」→ 输入 `sitemap.xml` → 点击「提交」

状态显示「成功」后，Google 会定期抓取 sitemap 中的所有 URL。

### 申请编入索引

对重要页面手动申请：

1. 顶部搜索栏输入完整 URL
2. 点击「请求编入索引」

每天申请配额有限（约 10 次），只对核心页面使用。

### 日常监控

- **覆盖率报告**：检查「已排除」的 URL
- **效果报告**：展示次数、点击率、平均排名
- **核心网页体验**：CWV 是否通过

---

## 百度站长工具

### 添加网站

1. 打开 [百度搜索资源平台](https://ziyuan.baidu.com/)
2. 注册/登录百度账号
3. 「用户中心」→「站点管理」→「添加网站」
4. 输入网站 URL，选择文件验证（同 Google）

### 主动推送 API

**获取 Token**：百度站长平台 → 数据引入 → 链接提交 → 主动推送

API endpoint：
```
POST https://data.zz.baidu.com/urls?site=https://YOURDOMAIN&token=YOUR_TOKEN
Content-Type: text/plain

https://YOURDOMAIN/
https://YOURDOMAIN/page1
https://YOURDOMAIN/page2
```

**限制**：
- 每次请求最多 2000 条 URL
- 每天配额 10000 条
- 配额每日重置

**AI 执行命令**：
```bash
# 从线上 sitemap 提取 URL 并推送
curl -s https://YOURDOMAIN/sitemap.xml | grep -oP '(?<=<loc>)[^<]+' > /tmp/baidu-urls.txt
curl -s -H 'Content-Type:text/plain' \
  --data-binary @/tmp/baidu-urls.txt \
  "https://data.zz.baidu.com/urls?site=https://YOURDOMAIN&token=YOUR_TOKEN"
```

成功响应示例：
```json
{"remain":9900,"success":100}
```

错误响应示例：
```json
{"error":401,"message":"token is invalid"}
```
→ 检查 token 和 site 参数是否与百度站长后台完全一致（包括 https/http）。

### 抓取诊断

「工具」→「抓取诊断」→ 输入 URL → 提交抓取，验证百度蜘蛛能正常访问页面。

---

## Bing Webmaster Tools

1. 打开 [Bing Webmaster Tools](https://www.bing.com/webmasters/)
2. 使用 Microsoft 账号登录
3. 「添加网站」→ 输入 URL
4. 提交 sitemap：「Sitemaps」→「提交 sitemap」→ 输入 `https://YOURDOMAIN/sitemap.xml`

### IndexNow（可选加速）

IndexNow 让搜索引擎实时感知内容变更。生成一个 key 文件，放到网站根目录，然后在内容更新时调用 API：

```bash
curl "https://api.indexnow.org/indexnow?url=https://YOURDOMAIN/new-page&key=YOUR_KEY"
```

详见：https://www.indexnow.org/

---

## 验收检查

提交完成后，等待 1-7 天，用以下方式确认收录：

| 搜索引擎 | 验证命令 |
|---|---|
| Google | 在 Google 搜索 `site:YOURDOMAIN` |
| Baidu | 在百度搜索 `site:YOURDOMAIN` |
| Bing | 在 Bing 搜索 `site:YOURDOMAIN` |

同时在 Google Search Console 检查：Coverage report → Indexed 数量是否增长。
