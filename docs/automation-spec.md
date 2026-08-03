# 日报自动化规范

这份文档定义每天 09:05 触发 AI 日报自动化时应遵循的规则。日报业务时间窗仍固定为 09:00 到 09:00。

## 目标

- 生成一篇简洁、高信噪比、可回看的 AI 日报
- 聚焦全球 AI 热点，重点覆盖中美大模型与 AI 编程代理
- 在必要时补充能反作用于 AI 主线的外围高相关情报
- 稳定记录活跃 AI 博主、技术工作者、研究者、创业者和关键人物的信息线索、判断、困惑、分歧与方法论；入选门槛是可复查、AI 相关、有信息增量，而不要求每条都是强观点
- 在有高价值论文或研究动向时记录 AI 研究前沿，用来辅助技术路线和未来趋势判断
- 将结果直接提交到本仓库，供后续查阅

## 时间口径

- 候选收件箱预生成时间：每天 08:40，Asia/Shanghai
- 自动化触发时间：每天 09:05，Asia/Shanghai
- 兜底巡检时间：每天 09:35，Asia/Shanghai
- 报告时间窗：前一日 09:00 至当日 09:00
- 触发时间比业务窗口晚 5 分钟，是为了避开本机多个 Codex automation 同时抢启动导致的静默失败风险
- 安装器会同时写入本地时钟和 UTC 时钟候选触发点，兼容 Codex Desktop cron 在不同版本中的时区解释差异
- 日报主任务执行前必须再次检查真实 `Asia/Shanghai` 时间窗口和当天日报文件；如果不在窗口内或文件已存在，必须 no-op 且不改仓库
- 候选收件箱任务只写 `.codex-run/` 本地文件，不提交、不推送、不发通知；如果失败，不影响日报主任务和 watchdog
- watchdog 只检查当天日报是否已经落盘；如果已存在，不改仓库；如果缺失，按同一时间窗补写日报并推送
- 如果严格时间窗内高价值更新偏少，可以补入最近几天仍在持续发酵的高价值官方更新，但必须在正文中明确补充范围
- 补充内容必须避免与仓库中最近几日日报重复；如果没有新的高置信度信息，允许生成更短的简版日报

## 报告要求

- 输出文件路径：`daily/YYYY/YYYY-MM/YYYY-MM-DD.md`
- 元数据输出路径：`metadata/daily/YYYY/YYYY-MM/YYYY-MM-DD.yml`
- 标题格式：`# AI 日报 - YYYY-MM-DD`
- 必须包含可点击来源链接
- 必须优先使用官方来源
- 必须使用绝对日期，避免“今天”“昨天”
- 必须包含独立的 `我的判断` 模块
- 必须包含一个简短的 `30 秒摘要`
- 完整 YAML 元数据默认写入 sidecar 文件，记录主题、公司、产品、信号、opinion_sources、viewpoint_themes、research_sources、research_themes、research_artifacts、research_interpretations、candidate_usage、source_checks、evidence_items、followups、fact_confidence 和 signal_strength，便于后续周报 / 月报聚合
- 正文 `结构化索引` 只保留 sidecar 路径和轻量说明；只有 sidecar 无法生成时，才临时退回可折叠 YAML

## AI 信号候选收件箱

- 候选收件箱是日报前置辅助层，不替代日报自动化和人工判断
- 日报消费的稳定候选结构称为 `SignalCandidate`，信源基础画像称为 `SourceProfile`
- 公开候选源登记在 `config/signal-sources.yml`；只有 `source_tier: public`、`run_mode: auto`、`health_status: active` 的来源允许进入自动采集
- 本地 SQLite、候选 JSONL、review Markdown 和手工导入 JSONL 必须写入 `.codex-run/`，不得提交到仓库
- 可用 `python3 scripts/collect_signal_candidates.py --date YYYY-MM-DD` 采集公开源，用 `python3 scripts/render_signal_review.py --date YYYY-MM-DD` 生成 `.codex-run/signal-reviews/YYYY-MM-DD.md`
- 日报任务如果发现 `.codex-run/signal-reviews/YYYY-MM-DD.md` 存在，可以读取其中 `已采用`、`观察中`、`补证据` 或仍为 `待审` 但分数较高的候选作为辅助线索；如果候选池不存在、为空或脚本失败，日报仍按既有规则继续生成
- 候选信号只能作为线索入口，写入日报前仍需检查原始链接、官方来源、论文原文、release、changelog 或原始项目链接
- review 中的 `adoption_reason`、`rejection_reason`、`retrospective_status` 用于周报、月报、年报复盘；未采用理由也应被视为长期认知资产
- X、公众号、小红书、付费墙、私域社群、浏览器 Cookie 和登录态来源不进入 v1 自动链路；未来如需接入，只能放在独立实验区，人工触发、人工确认、只输出候选信号

其他周期报告路径约定：

- 周报：`weekly/YYYY/YYYY-Www.md`
- 月报：`monthly/YYYY/YYYY-MM.md`
- 年报：`yearly/YYYY/YYYY.md`

## 企业微信提醒

- 企业微信提醒使用群机器人 webhook，默认只发送报告摘要和 GitHub 链接，不发送完整报告正文
- 日报不发送企业微信群消息；日报只负责生成、提交并推送到 GitHub
- 周报提醒时间：周报生成任务成功 `push origin main` 后立即发送；每周一 `10:15 Asia/Shanghai` 的独立通知任务作为兜底检查，发送刚完成的上一个完整周报
- 月报提醒时间：每月 1 日 `10:20 Asia/Shanghai`，发送刚完成的上一个自然月月报
- 年报提醒时间：每年 1 月 1 日 `10:25 Asia/Shanghai`，发送刚完成的上一年年报
- 提醒任务必须在发送前确认对应报告已经存在于 `origin/main`
- 同一报告同一远端 commit 只能发送一次，除非手动使用 `--force`
- 周报生成任务在推送成功后必须调用 `python3 scripts/send_wecom_report.py --kind weekly --date YYYY-MM-DD`
- 企业微信发送失败不能回滚或修改已经推送到 GitHub 的报告，只能作为通知失败单独报告
- webhook 只能来自环境变量 `WECOM_WEBHOOK_URL` 或本机忽略文件 `.codex-run/wecom-notify.env`，不得提交到仓库或打印到日志
- 如果 webhook 未配置，提醒任务必须安全跳过，不影响日报、周报、月报、年报生成

## 必查数据源

- 如果本地存在 `.codex-run/signal-reviews/YYYY-MM-DD.md`，先把它作为候选线索清单读取；不存在时不要报错，也不要为了生成候选池而阻塞日报
- 先查 [docs/source-watchlist.md](source-watchlist.md) 中的 AI 编程代理专项源
- 再查中国模型厂商专项源
- 如果核心主线之外出现高价值外围变量，再查 AI 外围高相关情报源
- 优先扫描 AI 圈博主源中的核心日常雷达和 `AI 圈观点与社区信号源池`；低频关键人物候选只在出现长文、公开演讲、重大短帖或关键线索时使用
- 对中英文扩展源，优先使用 RSS / Atom、GitHub Releases、GitHub org activity、changelog 和公开长文；网页型来源可作为常规巡检或低频候选，不要求每日命中
- `AI 圈博主` 每天至少巡检三个桶：中文公开源、英文个人 / newsletter 源、工程社区源；正文要求固定 5 条，其中中文来源 2 条、英文来源 3 条
- 如果主窗口内 `AI 圈博主` 命中不足 5 条，扩大到最近 7 天未写入过的公开输出；补入时必须标明发布日期或观察日期，并避免重复近期日报
- AI 圈博主暂不纳入 X-only 来源；优先使用博客、RSS / Atom、Substack、GitHub、公众号公开页和公开长文。如果账号只有 X 入口，在 `source_checks` 中标记为 `blocked` 或 `partial`
- 扫描 AI 研究前沿源，优先挑选有原文链接且可能影响技术路线判断的论文、研究博客、benchmark、eval、开源实现或实验室动向
- 对 Codex、Claude Code、Copilot、Cursor、Gemini CLI、Devin、Qwen Code 相关动态，优先查产品页、官方文档、changelog、官方仓库和 release
- 对 DeepSeek、Qwen、智谱、Kimi、MiniMax、腾讯混元、百度文心、豆包 / 火山方舟，优先查官方博客、产品页、文档页、产品动态和官方 GitHub

## 动态流规则

- 每日巡检时，不只看官网首页，也要看 changelog、release notes、产品动态页
- 重点仓库要看 release / tags / 最近活跃情况
- 重点文档要看最近更新痕迹，例如 last updated、release notes、weekly update
- 如果固定 watchlist 没有足够信息，再补高质量媒体与社区信号

## 选题优先级

1. OpenAI、Anthropic、Google、Meta、Microsoft、GitHub 的官方更新
2. DeepSeek、Qwen、智谱、Kimi、MiniMax 等中国模型公司的重要进展
3. Codex、Claude Code、Copilot、Cursor、Devin、Gemini CLI 等 AI 编程工具动态
4. GitHub 热门 AI 项目和关键开源基础设施
5. 投融资、监管、合作、算力和推理服务等会改变格局的事件
6. 只有当它们明显反作用于 AI 主线时，才纳入算力、政策、安全、企业采用和行业落地等外围情报
7. 对 AI 圈博主，优先纳入可复查、AI 相关、有信息增量的线索、观点、方法论或实践复盘；不要求每条都直接改变主线判断
8. 只有当论文或研究动向能帮助判断未来技术路线时，才纳入 AI 研究前沿

## 写作原则

- 少而精，宁可少写，也不要堆砌
- 每条重点信息回答：发生了什么、为什么重要
- 区分“事实”与“判断”
- 评论部分要形成自己的判断，而不是重复事实
- 评论段落要显式体现“基于本期样本的判断”口径
- 尽量复用稳定的主题标签、公司名和产品名，减少同义写法，便于长期索引
- 观点 / 线索源只作为信息线索、思想信号和判断样本，不能替代官方发布、文档、changelog、Release 或原始项目链接等事实来源
- AI 圈博主条目必须标明 `类型：信息线索 / 观点判断 / 方法论 / 实践复盘`
- 媒体、资讯整理、GitHub 项目动态和社区资源进入 AI 圈博主时默认标为 `信息线索`，涉及事实时尽量补官方发布、论文原文、release 或原始项目链接
- 中英文扩展源每天合计要求选 5 条社区 / 观点信号：中文来源 2 条、英文来源 3 条；无足够可复查信息增量时可少于 5 条，但必须在 `source_checks` 说明缺口，不机械凑数
- 同一来源可以连续入选；判断依据是是否有新的、可复查的信息增量，而不是人为轮换来源
- AI 圈博主默认每天写 5 条，中文来源 2 条、英文来源 3 条，并在正文中按 `中文来源` / `英文来源` 分组；只有在完成核心雷达、中文公开源、英文个人 / newsletter 源和工程社区源巡检后仍无足够可复查信息增量时，正文才可少于 5 条或省略该模块，并在元数据 sidecar 的 `source_checks` 里写明缺口
- AI 研究前沿条目必须标明 `类型：论文 / 研究博客 / benchmark / eval / 开源实现 / 实验室动向`，并保留原文链接
- 权威解读只能作为辅助理解材料，不能替代论文或研究原文
- AI 研究前沿不是每期必写；如果当天没有高价值论文或研究动向，正文省略该模块，并在元数据 sidecar 里写 `research_sources: []`、`research_themes: []`、`research_artifacts: []` 和 `research_interpretations: []`
- 外围情报不是每期必写；如果当天没有高置信度外围变量，正文省略该模块，并在元数据 sidecar 里写 `peripheral_themes: []`
- 使用 `fact_confidence` 表示事实来源可靠性，使用 `signal_strength` 表示当天信号强弱，避免把“事实可靠”误读成“今天信号很强”
- 对 changelog、release、trending、stars、排名等易变化信息，优先引用具体条目，并尽量附带版本号、日期或快照时间
- `GitHub 热门项目` 用来发现主线之外的新兴 AI 开源项目和关键基础设施，默认排除 OpenAI、Anthropic Claude Code、GitHub Copilot 及其官方仓库、SDK、CLI、文档仓库；这些官方主线项目的重要更新应写入 `AI 新闻` 或 `AI 编程代理`
- `GitHub 热门项目` 尽量不要重复最近 7 天已经写过的项目；只有出现新的 release、架构变化、生态采用、star / trending 明显跃迁或生产使用证据时，才允许重复并写明新增信息
- 如果当天没有足够新鲜且有信息增量的热门项目，可以省略 `GitHub 热门项目`，不要用 OpenAI、Claude Code、Copilot 等主线官方项目占位
- 对主要来源组，必须在 `source_checks` 中记录是否巡检、巡检时间和 `hit` / `miss` / `blocked` / `partial` 结果；推荐分组包括 `ai_blogger_core_radar`、`ai_blogger_free_opinion_pool`、`china_ai_media_signals`、`china_ai_engineering_radar`、`china_research_community`、`english_ai_engineering_radar`、`english_agent_infra_radar`、`english_inference_platforms`、`english_research_blogs`、`english_industry_analysis`、`english_safety_governance`
- 对核心条目，建议在 `evidence_items` 中记录来源角色、证据类型、条目日期、快照时间、一手链接和置信理由
- 对不确定信息明确标注

## Git 要求

- 只提交本次生成或更新的日报文件和对应元数据 sidecar
- commit message 使用：`docs: add ai digest for YYYY-MM-DD`
- 默认推送到 `main`

## 跨电脑安装

- 仓库内提供跨平台安装器 `scripts/install_codex_daily_digest.py`
- macOS / Linux 另外提供便捷包装脚本 `scripts/install_codex_daily_digest.sh`
- 脚本会一并安装候选收件箱、日报、日报 watchdog、周报、月报、年报和企业微信提醒九个 Codex 自动化任务
- 脚本会把自动化配置写入 `${CODEX_HOME:-~/.codex}/automations/<automation-id>/automation.toml`
- 脚本会根据当前电脑的本地时区，计算日报、周报、月报、年报和企业微信提醒各自对应的 `Asia/Shanghai` 本地触发时间，并额外写入 UTC 时钟候选触发时间
- 如果仓库换了路径，或者系统时区发生变化，重跑一次安装脚本
- 详细说明见 [docs/portable-setup.md](portable-setup.md)

## 失败处理

- 如果当天高价值更新很少，仍生成简版日报
- 如果抓取过程受阻，保留已验证的重要信息，不用未经确认的内容凑数
- 如果候选收件箱采集失败、review 缺失或为空，记录为辅助线索缺失，不影响日报、周报、月报、年报主链路
- 如果企业微信发送失败，只记录通知失败，不回滚或修改已经生成的报告
- 如果企业微信 webhook 未配置，通知任务安全跳过
- 如果自动化连续缺失日报，先运行 `python3 scripts/check_archive_health.py --fetch` 检查缺失日报、周报、月报、本机 automation、远端同步和最近提交状态
- 如果 session 日志显示任务在 `17:xx Asia/Shanghai` 触发并因窗口校验 no-op，说明当前 Codex cron 正在按 UTC 时钟解释 `BYHOUR`；重跑 `python3 scripts/install_codex_daily_digest.py`，确认 RRULE 同时包含 `BYHOUR=1,9` 这类双候选小时
