---
name: link-ops
description: 面向独立开发者建立、执行和复盘外链运营系统。用于“怎么给这个站铺外链”“分析竞品 backlinks”“建立外链渠道库”“找可复制的 referring domains”“给新词站做 launch backlinks”“筛选 guest post/资源页/榜单机会”“做外链 outreach 和效果复盘”等任务。不要把它当成批量垃圾外链生成器；自动群发、批量评论、购买链接或其他外部状态变更都需要用户单独授权。
---

# Link Ops

把外链从一次性“发链接”变成可积累的运营系统：**发现机会 → 归一化入库 → 判断链接原因 → 质量/风险评分 → 排行动队列 → 个性化执行 → 验证结果 → 沉淀渠道资产。**

目标不是追求 backlink 数量，而是获得更多独立、相关、能带来真实用户或编辑引用的 referring domains，并不断缩短下一次新站/新词的执行时间。

## 1. 建立 Campaign Brief

先明确：

- 站点与目标页面；
- 目标关键词/主题簇；
- 当前阶段：新站发现、关键词冲榜、排名防守、品牌/PR、linkable asset；
- 3–10 个真实搜索竞品；
- 可接受的执行方式与禁区；
- 用户是否授权外部提交、联系或付费。

如果用户只要求研究或规划，默认停在行动队列和草稿，不自动提交目录、不发邮件、不评论、不购买链接。

开始执行前读取：

- `references/playbook.md`：完整发现和执行工作流；
- `references/scoring.md`：机会评分与风险门槛；
- `references/schema.md`：workspace 数据字段；
- `references/policy.md`：Google link spam 边界与外部动作规则。

## 2. 先区分链接任务

每条机会至少标记一个主要目的：

- `discovery`：帮助爬虫、用户和社区发现产品；
- `ranking`：争取主题相关、具有编辑选择性的引用；
- `referral`：直接获得真实访问、注册和品牌传播；
- `defense`：补齐竞争者正在建立的链接优势；
- `asset`：让数据、工具、模板、API 或研究持续自然获得引用。

不要把 `nofollow` / `ugc` 自动等同于无价值，也不要把第三方 DR/DA 当作 Google 排名分数。它们只能是筛选上下文，不是最终判断。

## 3. 双轨发现机会

同时跑两条轨道，避免只靠“外链网站大全”。

### 轨道 A：竞品反查

优先找目标关键词前 20 中、与你页面类型和站点体量相近的 3–10 个竞品。用当前可用的 backlink 数据源、用户提供的 Ahrefs/Semrush/Bing 导出、公开网页和搜索结果收集 referring pages/domains。

重点找：

- 同时链接两个以上竞品但没有链接你的页面；
- 链到竞品具体功能页而非只链首页；
- 排名页面的正文编辑引用；
- 可解释的榜单、资源页、教程、测评、集成、数据引用；
- 指向已失效竞品页面的 broken links；
- 竞争者最近新增、与你目标页直接相关的链接。

### 轨道 B：原因驱动发现

从“别人为什么愿意链接”反推渠道：

- 产品/插件/模板/生态市场；
- Best X、Alternatives、资源页；
- 教程和 workflow 内容；
- 社区问题与垂直论坛；
- 开源仓库、Awesome List、示例项目；
- Integration / Partner / Case Study；
- 原创数据、免费工具、可引用数据库；
- 数字 PR 与记者 source request；
- broken-link replacement；
- 高质量 guest contribution。

`references/playbook.md` 包含搜索模式、渠道分类和优先级。

## 4. 入库、去重和评分

需要保存大量候选时，在用户指定的私有工作目录初始化 workspace：

```bash
python scripts/link_ops.py init --output <path> --site https://example.com
```

导入 backlink CSV：

```bash
python scripts/link_ops.py import \
  --run <path> \
  --input <export.csv> \
  --source ahrefs \
  --competitor competitor.com
```

脚本会归一化常见导出字段、提取来源域并按 `source_url + target_url + competitor` 去重。原始私有导出留在用户工作目录，不提交到本公开仓库。

对 shortlist 人工/Agent 补齐 0–5 分后：

```bash
python scripts/link_ops.py score --run <path>
python scripts/link_ops.py validate --run <path>
```

评分只做排序，不代替判断。`spam_risk >= 4` 的机会即使基础分高，也默认 reject。详见 `references/scoring.md`。

## 5. 排行动队列

默认按下面顺序处理：

1. **已有关系/官方生态**：真实 integration、marketplace、合作伙伴、开源项目；
2. **竞品 Link Intersect**：多个竞品都拿到、且原因可复制的链接；
3. **高相关资源页 / Best X / 教程**；
4. **broken link 与失效产品替代**；
5. **有真实读者的社区问题和垂直讨论**；
6. **linkable asset + 定向 PR/outreach**；
7. **高质量 guest contribution**；
8. 普通目录/泛社区，只作为发现和品牌分发，不追求数量。

每个 priority prospect 都必须写清楚：

`Why this page → Why us → What action → Expected user value → Risk`

无法说明“为什么这个页面应该链接我们”的候选降级。

## 6. 执行与外联

先研究来源页面，再生成个性化动作。外联必须引用页面中的具体上下文，并提供可验证的增加价值理由，例如：

- 更完整/更新的数据；
- 免费可用的工具；
- 竞品缺失的细分能力；
- 失效链接的等价替代；
- 对文章某一步骤的直接增强；
- 可测试的 integration、demo、API 或模板。

不要自动制造大量精确匹配锚文本。优先品牌名、页面名、裸 URL 和自然上下文。

以下动作必须获得用户明确授权后才执行：

- 发邮件、DM 或提交联系表单；
- 在论坛/社区发布内容或评论；
- 提交目录、注册账号；
- 购买赞助、guest post、link insertion；
- 建立互链合作；
- 修改外部网站状态。

可以在授权前完成研究、联系人定位、草稿、优先级和批次计划。

## 7. 新词 / 新站 Sprint

对竞争尚未稳定的新词，速度来自整套动作，不来自“第一天必须发 200 条”：

- 先确保页面可抓取、内链和 sitemap 正常；
- 立即完成少量真实基础分发；
- 反查最早进入 SERP 的竞品；
- 优先抢官方生态、社区问题、资源页和可复用渠道；
- 起量后继续补内页、产品体验和高质量引用；
- 每天观察 GSC/Bing、referral、排名和新增 referring domains。

高频批量目录、自动评论、模板 footer/widget 关键词链接、站群、付费 followed links、规模化互链不属于本 Skill 的推荐动作。

## 8. 复盘并沉淀资产

不要只记录“发了多少条”。至少追踪：

- 新增独立 referring domains；
- 链接页面是否仍存活/收录；
- priority prospect 成功率；
- 不同渠道的回复率、上线率；
- referral visits、注册和付费；
- 目标页 impressions / clicks / ranking movement；
- 链接存活 30/90 天情况；
- 哪些渠道可跨项目复用；
- 哪些链接是自然二次引用。

每次 campaign 后更新 `channels.csv` 的 wins/failures/last_verified，把“渠道列表”升级成有历史胜率的运营资产。

## 结束边界

默认交付研究结果、prospect shortlist、评分、执行批次和草稿。除非用户明确授权，不自动向外部网站提交、联系、购买、注册或发布。
