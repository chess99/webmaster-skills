# Opportunity Discovery Playbook

> 用于 `find-product-opportunities` 的候选生成阶段。目标是让 Agent 像 builder 一样从变化中识别产品机会，而不是随机脑暴关键词。

开始前同时读取：

- `opportunity-pattern-library.md`：机会 detector 与 pattern IDs；
- `evidence.md`：什么能证明、什么不能证明；
- `source-strategy.md`：来源和失败回退。

## 0. 先把问题写成“寻找什么变化”

研究简报除了目标市场、builder fit、资源上限，还应增加一条：

> 在这个市场里，哪些成本、能力、规则、价格、供给、默认值、分发、情绪或买家角色最近发生了变化？

若用户没有指定行业，默认不仅扫“当前热门赛道”，也要扫 boring/stable workflows，防止 daily-news bias。

---

## 1. 两轨扫描：Stable Jobs + Recent Deltas

不要只做热点扫描。

### Track A — Stable Jobs

寻找长期存在、反复发生的任务：

- 人们持续付费的工作；
- 高频手工流程；
- 持续存在的抱怨；
- spreadsheet / script / agency / VA workaround；
- 迁移、对账、审核、导出、排班、报告、审批、配置等 boring work。

目的：防止漏掉“没有新闻但一直赚钱”的软件。

### Track B — Recent Deltas

使用 `opportunity-pattern-library.md` 扫最近变化：

- incumbent disruption；
- OSS adoption；
- technology unlock；
- workflow friction；
- search/language shift；
- buyer/economics；
- distribution leverage；
- market structure。

目的：找到“为什么现在”。

强候选通常来自：

`stable job + recent delta`

例如：长期存在的迁移任务 + 竞品涨价；长期存在的 QA + AI 生成代码变快；长期存在的备份需求 + self-hosted wave。

---

## 2. 扫描覆盖规则：避免 mode collapse

发散 20–40 个候选时：

1. 至少覆盖 **6 个 pattern families**；
2. 单个 family 默认最多贡献 25% 候选；
3. 单个热门品牌/模型/项目默认最多派生 3 个候选；
4. 至少 30% 候选来自 stable jobs，不依赖最近新闻；
5. 至少 30% 候选要能指出明确 payer，而不只是 end user；
6. 至少 30% 候选应有非订阅形态的可能性，如一次性工具、usage-based、report、CLI、productized service；不要默认所有机会都是 SaaS。

这些比例是防偏差约束，不是评分项；研究范围过窄时允许说明理由后偏离。

---

## 3. Signal → Candidate 转换

每个原始信号先走一次转换，不直接起产品名。

### Step 1 — Signal

记录可观察事实：

- 谁说了什么；
- 什么词在变；
- 哪个项目增长；
- 哪个价格/规则/能力变化；
- 哪个工作流有明确支出。

### Step 2 — Change

写一句：

> 相对过去，真正变化的是 ______。

如果只能写“大家最近在讨论 X”，说明 change 尚未找到。

### Step 3 — Job

写成用户任务，而不是功能：

> 当 ______ 时，______ 需要 ______，以便 ______。

### Step 4 — Friction type

必须选择最接近的一类或两类：

- missing-capability
- bad-ux
- setup-config
- fragmentation
- integration-tax
- hidden-cost
- trust-privacy
- migration-portability
- verification
- documentation-defaults
- approval-governance
- distribution-discovery

`Pain != Product Gap`：如果是 docs/defaults 问题，不要自动生成完整替代品。

### Step 5 — Payer

区分：

- user；
- team lead；
- founder/owner；
- finance；
- security/compliance；
- operations；
- client/customer；
- procurement。

没有 payer 的候选默认降低优先级，但 consumer utility 可以用明确个人支出替代。

### Step 6 — Wedge

优先选择最小价值层：

- checker
- calculator
- report
- importer/exporter
- migration assistant
- CLI
- browser extension
- local desktop utility
- workflow adapter
- team policy layer
- managed operation
- productized service
- narrow SaaS

不要一开始写“完整 X 替代品”，除非 platform gap 本身已被多源验证。

### Step 7 — Proof artifact

要求回答：

> 2 小时内，什么输出物能让目标用户判断这东西有没有用？

优先：

- 前后对比；
- 安装/兼容矩阵；
- 成本报告；
- 权限/数据流报告；
- migration readiness；
- audit result；
- offline/export packet；
- calculator result；
- benchmark；
- demo workflow。

### Step 8 — Counterfactual

立即写一个最可能的替代解释：

- 只是新闻尖峰；
- 只是导航搜索；
- 只是极客偏好；
- 没商业版是因为没人付费；
- 抱怨的是文档而不是软件；
- 原厂即将补功能；
- 成功案例依赖创始人手工能力；
- 目标买家销售周期不适合 indie。

无法生成 counterfactual 的候选通常是过早爱上自己的想法。

---

## 4. Candidate Card

发散阶段每个候选至少记录：

```json
{
  "name": "working title, not a brand decision",
  "target_user": "specific user",
  "payer": "who owns budget or consequence",
  "job": "job to be done",
  "change": "what changed and why now",
  "friction_type": ["verification"],
  "pattern_ids": ["C5", "D3", "F5"],
  "current_workaround": "what they do now",
  "wedge": "smallest useful product",
  "proof_artifact": "what a 2h demo outputs",
  "distribution_hypothesis": "first reachable channel",
  "alternate_explanation": "most plausible counter-story",
  "decay_risk": "low | medium | high",
  "evidence_ids": []
}
```

### decay_risk

- `high`：产品价值依赖某个刚发布模型/品牌/短期事件；
- `medium`：依赖新技术或平台变化，但 job 本身持久；
- `low`：核心 job 长期存在，近期变化只改善 timing。

优先选择 `stable job + medium/low decay`，而不是纯热点。

---

## 5. Pattern combination：从“信号”升级为“机会”

单一 detector 只能生成观察，多个独立模式组合后才更像机会。

### Rule A — 至少尝试一次跨家族组合

例如：

- `price change + alternative query + migration community`
- `OSS growth + team adoption + security owner`
- `cost drop + paid manual workflow + vertical distribution`
- `complaint cluster + repeated workaround + high cost of error`

### Rule B — 找共同 latent job

多个不同品牌上涨时，不要分别生成 N 个品牌工具。先问：

> 它们共同满足的持久 job 是什么？

例如多个 self-hosted 笔记/聊天/文件工具同时上涨，latent job 可能是“控制关键工作数据”，后续再寻找 export、backup、deployment、migration 等可收费 wedge。

### Rule C — 找 adoption 的第二阶问题

新能力 adoption 增长时，不只问“能做什么”，还要问：

> 大家真的开始使用以后，会新增什么责任？

常见第二阶问题：成本、权限、审计、支持、兼容、迁移、治理、可重复性。

---

## 6. 初筛：先杀掉“有趣但不像生意”的东西

20–40 个候选生成后，先不做完整尽调，用以下 gates 缩到 8–12：

### Gate 1 — Job clarity

能否一句话说明谁在什么情境下完成什么任务？

### Gate 2 — Why now

能否说明一个真实 delta？若没有，stable job 必须有强商业证明才能保留。

### Gate 3 — Payer / spend

是否有已有支出、明确责任或高成本 workaround？

### Gate 4 — Indie wedge

是否有 4–6 周以内可收费版本？能否比 incumbent 更窄、更快？

### Gate 5 — Distribution

是否至少能提出一条可验证的第一分发路径？

### Gate 6 — Counter-story survival

如果最合理的 alternate explanation 为真，机会是否完全消失？若是，优先淘汰或降低验证成本后再看。

### Gate 7 — Decay

若品牌/新闻热度 30 天后归零，job 还存在吗？

---

## 7. 多源验证：模式负责发现，证据负责裁决

进入 8–12 后恢复现有 Skill 的严谨流程：

- 至少三类独立 signal families；
- 优先行为/搜索 + 用户原话 + 商业证明；
- 主动反证；
- 不把 trend、stars、评论数单独当付费证明；
- 竞品不存在必须独立验证，不能由“没搜到”推出；
- 冲突证据保留。

Pattern ID 不增加证据权重，只用于解释**为什么会想到这个候选**。

---

## 8. 2h Demo / 48h Validation

Builder-style discovery 应尽快从研究切到可证伪动作。

### 2h Demo Test

不是要求生产产品两小时做完，而是测试 value proposition 能否被压缩。

合格 demo 应有：

- 一个真实输入；
- 一个真实输出；
- 一个目标用户能立即理解的 before/after；
- 尽量不需要账户体系、复杂后台或完整 UI。

若 2h demo 只能做 landing page，而无法交付任何结果，说明 wedge 可能仍太大或太抽象。

### 48h Validation Test

优先验证行为而不是口头好感：

- 帮 2–5 个真实对象跑一次结果；
- 发布真实 benchmark / compatibility / migration artifact；
- 在痛点发生地展示，不做泛流量投放；
- 看是否有人给数据、给项目、问价格、要求再跑一次、主动转发或要求接入。

“Nice idea”不算通过。

---

## 9. 发现阶段常见失败模式

### Failure 1 — Keyword brainstorming

只列关键词和赛道，没有 Change/Job/Payer。

**修复**：强制填写 Candidate Card。

### Failure 2 — Clone reflex

看到头部产品贵/火就做 clone。

**修复**：先分类 pain，优先找 migration、platform gap、pricing-model、local/offline 等具体 wedge。

### Failure 3 — OSS hosted reflex

看到 GitHub stars 就“做 SaaS 版”。

**修复**：扫描 B1 的八个相邻商业层，并找 payer。

### Failure 4 — Trend worship

把 Google Trends 百分比或新词当需求。

**修复**：找到持久 job、第二类证据和 alternate explanation。

### Failure 5 — News bias

候选全来自最近 7 天。

**修复**：Stable Jobs track 至少贡献约 30% 候选。

### Failure 6 — User = Payer

只写谁使用，不写谁承担后果。

**修复**：显式列 owner：finance/security/ops/founder/client。

### Failure 7 — Big-suite fantasy

候选动辄“X for industry Y”。

**修复**：用 H6 强制写一个 2h proof artifact 和最小 wedge。

### Failure 8 — No competition = opportunity

没搜到同类就乐观。

**修复**：把“没有竞争”改写为待验证假设；检查替代流程、免费工具、agency/manual workaround 和上游原生能力。

---

## 10. 输出给后续评分流程的内容

进入现有 `scoring.md` 前，每个 finalist 应额外保留：

- `pattern_ids`
- `change`
- `payer`
- `friction_type`
- `proof_artifact`
- `alternate_explanation`
- `decay_risk`

这些字段不直接加分，但能让最终评分解释“这个机会是如何被发现的”，并帮助区分：

- 高分但纯热点；
- 低热度但 stable job 很强；
- OSS adoption 很强但 payer 不存在；
- 搜索增长很快但 alternate explanation 尚未排除。

最终仍由证据、反证、builder fit 和 kill criteria 决定 recommendation / NO-GO。