# AI News Digest Archive

> Daily-to-yearly AI intelligence archive with facts, judgment, and long-term signal tracking.  
> 一套围绕 AI 主线、同时吸收关键外围变量的长期情报档案库。

这不是一个“把新闻贴满仓库”的项目。

它更像一套可持续运行的 AI 情报工作流：每天生成高信噪比日报，在事实之外沉淀判断，再通过周报、月报、年报把短期热点变成长期认知资产。

项目主线始终围绕 AI 本身展开，重点关注：

- 中美大模型公司与模型节奏
- AI 编程代理、开发者工具、Agent 工作流
- 官方博客、研究、产品更新、changelog、release notes
- GitHub 热门项目与关键开源基础设施

同时，这套方法也允许有节制地向外扩一圈：

- 当算力、半导体、云平台、监管、安全治理、企业采用、重点行业落地对 AI 主线产生实质影响时，会作为 `AI 外围高相关情报` 纳入观察
- 如果这些外围变量当天没有高置信度新增，就不强行写入日报

这意味着它不是泛科技资讯仓库，而是一套“`AI 核心主线 + AI 外围关键变量`”的情报归档系统。

## 适合谁

这个仓库适合下面几类人：

- 想长期跟踪全球 AI 竞争，而不是只看零散新闻的人
- 想重点观察中美模型公司、AI 编程代理、官方发布和开源基础设施的人
- 想把“事实 + 判断 + 跟踪问题”一起沉淀下来的人
- 想要一套可以 fork、克隆、换电脑后仍然能恢复运行的 Codex 自动化流程的人

## 这个项目解决什么问题

很多 AI 资讯流有两个常见问题：

- 信息很多，但没有稳定主线
- 文章很多，但没有持续判断

这个仓库要解决的是另一类问题：

- 每天只记录最值得记住的高价值更新
- 尽量优先引用官方一手来源，减少二手噪声
- 把“事实”和“判断”明确分开
- 允许日报偏短，不为了凑数重复昨天已经写过的内容
- 通过周报、月报、年报不断修正和沉淀自己的长期判断

## 方法特点

这套流程的核心不是“搜更多”，而是“更稳定地选、写、存、复盘”。

它的工作方法大致是：

1. 先扫固定 watchlist 中最重要的一手源
2. 再看 changelog、release、文档更新等动态流
3. 只挑会改变格局、工作流、部署方式或开发者行为的高价值信息
4. 在事实层之后追加当日判断
5. 用结构化元数据为周报、月报、年报和长期议题台账做索引

你可以把它理解成一套带有编辑标准的 AI 情报生产线，而不是一份临时整理的链接清单。

## 当前覆盖范围

核心覆盖：

- OpenAI / Anthropic / Google / Meta / xAI / Microsoft / GitHub
- DeepSeek / Qwen / 智谱 / Kimi / MiniMax / 百度 / 腾讯 / 字节 / 01.AI / 商汤
- Codex / Claude Code / Cursor / GitHub Copilot / Gemini CLI / Devin / Qwen Code / Z Code
- GitHub 热门 AI 项目、MCP 生态、vLLM、SGLang、llama.cpp、Transformers 等关键基础设施

外围高相关覆盖：

- 算力与半导体
- 云平台、数据中心与推理容量
- 政策、监管与地缘政治
- 安全、滥用与治理
- 企业采用、组织变革与劳动力
- AI 在重点行业中的高价值落地

更细的对象和来源见：

- [docs/coverage-map.md](docs/coverage-map.md)
- [docs/source-watchlist.md](docs/source-watchlist.md)

## 日报长什么样

默认日报会包含这些模块：

- `结构化快照`
- `主线判断`
- `今日评论与判断`
- `今日最重要的 3-5 条更新`
- `中美大模型`
- `AI 编程代理`
- `官方博客 / 研究 / 发布`
- `AI 外围情报观察`
- `GitHub 热门项目`
- `值得继续跟踪`
- `结构化索引`
- `今日结构化结论`
- `参考来源`

其中有两个点是这个项目很看重的：

- 正文前部是给人看的 `结构化快照`
- 文末附近保留可折叠的 `结构化索引`，方便后续周报、月报、年报和机器聚合

参考模板见 [templates/daily-report-template.md](templates/daily-report-template.md)。

## 核心原则

- 优先使用官方一手来源
- 事实和判断分开写
- 不重复前几日日报已经写过的内容，除非有实质新角度
- 如果没有高置信度新增，允许日报更短
- 外围情报只有在能明确反作用于 AI 主线时才进入日报
- 评论必须建立在当天样本之上，而不是泛泛感想

详细规范见 [docs/editorial-guidelines.md](docs/editorial-guidelines.md) 和 [docs/automation-spec.md](docs/automation-spec.md)。

## 仓库结构

```text
daily/                  每日日报
weekly/                 每周周报
monthly/                每月月报
yearly/                 每年年报
docs/                   覆盖范围、写作规范、工作流说明
templates/              日报、周报、月报、年报模板
scripts/                安装与恢复脚本
ops/                    Codex 自动化模板
ledgers/                长期议题台账
```

默认路径约定：

- 日报：`daily/YYYY/YYYY-MM/YYYY-MM-DD.md`
- 周报：`weekly/YYYY/YYYY-Www.md`
- 月报：`monthly/YYYY/YYYY-MM.md`
- 年报：`yearly/YYYY/YYYY.md`

## 自动化能力

这个仓库当前已经具备：

- 每天 `09:05 Asia/Shanghai` 自动触发日报生成，业务口径仍固定为 `09:00` 桶
- 每天 `09:35 Asia/Shanghai` 自动巡检日报是否已生成；如主任务静默失败，由 watchdog 兜底补跑
- 每周 / 每月 / 每年自动生成高层总结
- 固定 watchlist 与动态流巡检规则
- 评论 / 判断层沉淀机制
- 结构化元数据模板
- 周报 / 月报 / 年报模板
- 长期议题台账模板与方法说明
- 跨电脑恢复安装方案
- 归档健康检查脚本，用于发现缺失日报、周报、月报和 Git 同步异常

日报自动化的业务时间固定为：

- 触发时间：每天 `09:05 Asia/Shanghai`
- 兜底巡检：每天 `09:35 Asia/Shanghai`
- 覆盖时间窗：前一日 `09:00` 到当日 `09:00`

如果严格时间窗内高价值更新太少，允许补充最近几天仍在发酵的一手信息，但不能和前几日日报简单重复。

说明：日报错峰到 `09:05` 是为了避开本机多个 Codex automation 同时在 `09:00` 抢启动造成的静默结束风险；`09:35` watchdog 用来检查主任务是否真的落盘，避免后台 automation 静默结束后无人发现。报告的业务时间窗不变，仍按 `09:00-09:00 Asia/Shanghai` 归档。

## 如何开始

如果你想直接复用这套方法，推荐这样开始：

1. fork 这个仓库到你自己的 GitHub 账号
2. 克隆你自己的仓库到本地
3. 确保 Codex 已登录，且当前仓库具备 `git push` 权限
4. 在仓库根目录运行 `python3 scripts/install_codex_daily_digest.py`
5. 安装器会一次性写入日报、日报 watchdog、周报、月报、年报这五个 Codex 自动化任务

详细说明见 [docs/portable-setup.md](docs/portable-setup.md)。

## 归档健康检查

如果你怀疑定时任务没有正常生成报告，可以在仓库根目录运行：

```bash
python3 scripts/check_archive_health.py
```

它会检查最近日报、已完成周报、已完成月报和 Git 同步状态。你也可以指定日期做复盘：

```bash
python3 scripts/check_archive_health.py --today 2026-06-01
```

## 如果你想继续扩展

这个仓库后续很适合继续往这些方向发展：

- 做专题索引，例如 Agent、开源模型、AI 编程、推理基础设施
- 增加跨周期趋势追踪和年度回顾
- 接入 RSS / Atom / 官方账号流
- 增加推送提醒与摘要分发
- 基于 `结构化索引` 做自动聚合、检索和可视化

## 相关文档

- [docs/coverage-map.md](docs/coverage-map.md)
- [docs/source-watchlist.md](docs/source-watchlist.md)
- [docs/editorial-guidelines.md](docs/editorial-guidelines.md)
- [docs/automation-spec.md](docs/automation-spec.md)
- [docs/portable-setup.md](docs/portable-setup.md)
- [docs/trend-ledger.md](docs/trend-ledger.md)
- [templates/daily-report-template.md](templates/daily-report-template.md)
- [templates/weekly-report-template.md](templates/weekly-report-template.md)
- [templates/monthly-report-template.md](templates/monthly-report-template.md)
- [templates/yearly-report-template.md](templates/yearly-report-template.md)
- [templates/trend-ledger-template.md](templates/trend-ledger-template.md)
