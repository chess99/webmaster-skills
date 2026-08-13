---
name: find-product-opportunities
description: 面向独立开发者发现、验证并排序有证据支撑的软件产品机会。用于“我该做什么产品”“帮我找细分市场/产品机会”“从某行业、受众、能力或技术趋势中找可做的 micro-SaaS、AI 工具、扩展或应用”等开放式机会研究；最终交付 Top 3 与主推荐或明确 NO-GO。不要用于已有网站的常规 SEO 选题，也不要把成熟单一想法的完整尽调误归入本 Skill。
---

# Find Product Opportunities

把“找点子”变成一次由 Agent 主导、可追溯且敢于否定的决策流程。不要让用户手工选词、操作趋势页面、整理表格或自己做最终排序。

核心不是追逐热门赛道，而是识别：**什么刚刚变了，以至于一个长期存在的任务现在出现了新的产品切口。**

## 1. 建立研究简报

从用户原话提取目标、开发者能力/资产、资源上限和禁区。只有缺失信息会实质改变结论时才提问，最多三个问题；其余采用默认值：

- 全球英语市场；
- 技术型独立开发者；
- 4–6 周 MVP、低前期成本；
- 独立软件产品，包括 micro-SaaS、AI 工具、浏览器扩展、桌面和移动工具。

不把纯内容、电商、课程混入同一排名。若用户已有明确想法并只需验证该想法，说明本 Skill 的发现流程不匹配并切换到针对性验证。

## 2. 先设证据边界与发现框架

开始联网研究前完整读取：

- `references/evidence.md`：证据记录、独立信号和禁止性表述；
- `references/source-strategy.md`：公开源优先、来源选择与失败回退；
- `references/opportunity-pattern-library.md`：机会 detector、pattern IDs 与常见误判；
- `references/discovery-playbook.md`：如何从 signal 转成候选并避免 mode collapse。

`references/builderpulse-study.md` 是方法来源研究，仅在需要理解 pattern 背景、维护或扩展模式库时读取；普通执行不需要每次加载。

明确当前能证明什么、不能证明什么。Google Trends 只是方向性信号，不是搜索量，也不是硬依赖。任何单一页面、聚合摘要、pattern 命中或模型推断都不能独立证明需求。

## 3. 双轨发散并初筛

候选生成必须同时跑两条轨道：

- **Stable Jobs**：长期存在的付费任务、手工流程、workaround、迁移、审核、配置、报告、对账、导出等 boring work；
- **Recent Deltas**：成本、能力、规则、价格、供给、默认值、分发、情绪或买家角色最近发生的变化。

优先寻找 `stable job + recent delta`，但有强商业证明的稳定机会可不依赖新闻。

按 `discovery-playbook.md` 使用 pattern library 发散 20–40 个候选：

- 尽量覆盖至少 6 个 pattern families，避免所有候选只是一个热点的变体；
- 每个候选先写 `Signal → Change → Job → Friction → Payer → Wedge → Proof → Counterfactual`；
- 明确 pain type，`Pain != Product Gap`；抱怨可能只是配置、文档、默认值、迁移、价格、验证或信任问题；
- OSS 快速增长只证明 capability adoption，不默认推导出 hosted clone；先检查 team、support、policy、audit、cost、upgrade、backup、vertical workflow 等相邻层；
- 热门品牌/模型必须尝试抽象成持久 job，并标记 `decay_risk`；
- 优先一个独立开发者能快速展示的窄 wedge，不默认完整替代品或大而全 SaaS。

先剔除：

- 没有明确目标用户、job 或高频/高成本问题；
- 只有 end user，没有个人支出或可解释的 payer/责任人；
- 获客路径无法指出；
- 4–6 周内无法形成可收费 MVP；
- 强监管、重线下或高持续运营成本；
- 只有趋势热度、stars 或讨论量，没有行为/付费/责任证据；
- 只是复制现有产品，没有可验证切入点；
- 机会完全依赖短期品牌/新闻热度，且无法抽象成持久任务。

保留 8–12 个进入验证。候选规模和 family 覆盖是研究深度目标，不得为了凑数降低门槛。

## 4. 多源验证与主动反证

为强候选收集至少三类相互独立的信号，例如搜索/趋势、社区痛点、商业证明、竞品缺口、分发可达性或技术变化。Pattern ID 只解释候选如何被发现，不增加证据权重。

对每个 finalist 主动执行至少一次反证检查，寻找：

- 问题已被免费方案充分解决；
- 用户抱怨强但没有付费动作；
- “没有竞品”其实只是搜索不完整，真实替代是脚本、agency、spreadsheet 或上游原生功能；
- 获客被平台或渠道垄断；
- 合规、数据、支持或基础设施成本不可承受；
- 趋势由新闻事件、导航需求或 launch spike 驱动而非持续任务；
- 上游厂商很容易补齐薄弱 wedge。

某来源被登录墙、限流或页面变化阻断时，切换同类来源并记录数据缺口。不要反复重试 Google Trends，也不要绕过付费墙。冲突证据必须保留。

## 5. 评分与裁决

初筛完成后读取 `references/scoring.md`。对候选按八维 0–5 分评分并计算 100 分总分；置信度单独标记为 low/medium/high。

公式排名是比较工具，不是结论。只有证据质量、关键风险或开发者匹配未被总分充分表达时才能覆盖排名，并记录原始名次、最终名次和证据化理由。

最终只能二选一：

- `recommendation`：恰好三个 finalist，并明确一个主推荐；
- `NO-GO`：没有足够证据支持值得做的机会。

## 6. 交付报告

输出前读取 `references/report.md`。默认直接在对话中交付，不主动写文件。报告必须包含结论、Top 3 对比、主推荐、证据与反证、风险/kills、淘汰摘要和 7 天验证实验。来源使用可点击链接并保留采集日期与限制。

主推荐的验证实验优先包含一个**可见 proof artifact**：例如检查结果、成本报告、迁移 readiness、安装矩阵、before/after、calculator result 或真实 workflow output。2 小时 demo 是 value-proposition 压缩测试，不是生产开发时限。

只有用户明确要求保存时，才复制 `assets/report-template.md` 并使用：

```bash
python scripts/opportunity_radar init --output <path>
python scripts/opportunity_radar score --run <path>
python scripts/opportunity_radar validate --run <path>
```

从本 Skill 目录运行这些命令。在交付保存的报告前，`validate` 必须返回成功。私有导出和登录数据只保存在用户指定位置，不进入插件仓库。

## 结束边界

研究在报告处结束。不要自动注册服务、购买数据、联系潜在客户、发布内容或开始开发。7 天实验只给出可执行方案；外部状态变更需要用户另行授权。
