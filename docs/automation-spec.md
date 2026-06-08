# 日报自动化规范

这份文档定义每天 09:05 触发 AI 日报自动化时应遵循的规则。日报业务时间窗仍固定为 09:00 到 09:00。

## 目标

- 生成一篇简洁、高信噪比、可回看的 AI 日报
- 聚焦全球 AI 热点，重点覆盖中美大模型与 AI 编程代理
- 在必要时补充能反作用于 AI 主线的外围高相关情报
- 将结果直接提交到本仓库，供后续查阅

## 时间口径

- 自动化触发时间：每天 09:05，Asia/Shanghai
- 兜底巡检时间：每天 09:35，Asia/Shanghai
- 报告时间窗：前一日 09:00 至当日 09:00
- 触发时间比业务窗口晚 5 分钟，是为了避开本机多个 Codex automation 同时抢启动导致的静默失败风险
- 安装器会同时写入本地时钟和 UTC 时钟候选触发点，兼容 Codex Desktop cron 在不同版本中的时区解释差异
- 日报主任务执行前必须再次检查真实 `Asia/Shanghai` 时间窗口和当天日报文件；如果不在窗口内或文件已存在，必须 no-op 且不改仓库
- watchdog 只检查当天日报是否已经落盘；如果已存在，不改仓库；如果缺失，按同一时间窗补写日报并推送
- 如果严格时间窗内高价值更新偏少，可以补入最近几天仍在持续发酵的高价值官方更新，但必须在正文中明确补充范围
- 补充内容必须避免与仓库中最近几日日报重复；如果没有新的高置信度信息，允许生成更短的简版日报

## 报告要求

- 输出文件路径：`daily/YYYY/YYYY-MM/YYYY-MM-DD.md`
- 标题格式：`# AI 日报 - YYYY-MM-DD`
- 必须包含可点击来源链接
- 必须优先使用官方来源
- 必须使用绝对日期，避免“今天”“昨天”
- 必须包含独立的评论 / 判断模块
- 建议包含一个简短的“结构化快照”，并在文末附近提供可折叠的完整 YAML 元数据，记录主题、公司、产品、信号、followups、fact_confidence 和 signal_strength，便于后续周报 / 月报聚合

其他周期报告路径约定：

- 周报：`weekly/YYYY/YYYY-Www.md`
- 月报：`monthly/YYYY/YYYY-MM.md`
- 年报：`yearly/YYYY/YYYY.md`

## 必查数据源

- 先查 [docs/source-watchlist.md](source-watchlist.md) 中的 AI 编程代理专项源
- 再查中国模型厂商专项源
- 如果核心主线之外出现高价值外围变量，再查 AI 外围高相关情报源
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

## 写作原则

- 少而精，宁可少写，也不要堆砌
- 每条重点信息回答：发生了什么、为什么重要
- 区分“事实”与“判断”
- 评论部分要形成自己的判断，而不是重复事实
- 评论段落要显式体现“基于本期样本的判断”口径
- 尽量复用稳定的主题标签、公司名和产品名，减少同义写法，便于长期索引
- 外围情报不是每期必写；如果当天没有高置信度外围变量，正文省略该模块，并在结构化索引里写 `peripheral_themes: []`
- 使用 `fact_confidence` 表示事实来源可靠性，使用 `signal_strength` 表示当天信号强弱，避免把“事实可靠”误读成“今天信号很强”
- 对 changelog、release、trending、stars、排名等易变化信息，优先引用具体条目，并尽量附带版本号、日期或快照时间
- 对不确定信息明确标注

## Git 要求

- 只提交本次生成或更新的日报文件
- commit message 使用：`docs: add ai digest for YYYY-MM-DD`
- 默认推送到 `main`

## 跨电脑安装

- 仓库内提供跨平台安装器 `scripts/install_codex_daily_digest.py`
- macOS / Linux 另外提供便捷包装脚本 `scripts/install_codex_daily_digest.sh`
- 脚本会一并安装日报、日报 watchdog、周报、月报、年报五个 Codex 自动化任务
- 脚本会把自动化配置写入 `${CODEX_HOME:-~/.codex}/automations/<automation-id>/automation.toml`
- 脚本会根据当前电脑的本地时区，计算日报、周报、月报、年报各自对应的 `Asia/Shanghai` 本地触发时间，并额外写入 UTC 时钟候选触发时间
- 如果仓库换了路径，或者系统时区发生变化，重跑一次安装脚本
- 详细说明见 [docs/portable-setup.md](portable-setup.md)

## 失败处理

- 如果当天高价值更新很少，仍生成简版日报
- 如果抓取过程受阻，保留已验证的重要信息，不用未经确认的内容凑数
- 如果自动化连续缺失日报，先运行 `python3 scripts/check_archive_health.py` 检查缺失日报、周报、月报和最近提交状态
- 如果 session 日志显示任务在 `17:xx Asia/Shanghai` 触发并因窗口校验 no-op，说明当前 Codex cron 正在按 UTC 时钟解释 `BYHOUR`；重跑 `python3 scripts/install_codex_daily_digest.py`，确认 RRULE 同时包含 `BYHOUR=1,9` 这类双候选小时
