# AI News Digest Archive

> Daily-to-yearly AI intelligence reports with commentary, judgment, and long-term signal tracking.
> 从日报到年报的 AI 情报档案库，记录事实，也沉淀判断与长期信号。

一个持续更新的 AI 情报档案库，按日报、周报、月报、年报沉淀全球 AI 领域的重要动态与判断，重点关注中美大模型、AI 编程代理、官方博客 / 研究 / 发布，以及 GitHub 热门项目和开源基础设施。

## 谁适合用

如果你也想要一套能长期沉淀 AI 观察、并且能由 Codex 每天自动写日报的仓库，这个项目可以直接 fork 后拿来用。

它适合：

- 想每天跟踪全球 AI 热点的人
- 想重点看中美大模型、AI 编程代理、官方博客与 GitHub 开源动态的人
- 想把“事实 + 判断”一起长期积累下来的人
- 想在自己的电脑上恢复同一套 Codex 自动化流程的人

## 这是什么

这个仓库不是单纯的“新闻搬运”。

它更像一个长期维护的 AI 观察站：

- 记录每天最值得关注的 AI 更新
- 在事实之上补充评论、判断和趋势推演
- 通过周报、月报、年报沉淀长期信号
- 尽量优先引用官方一手来源，减少二手转述噪声

## 目标

- 每天上午 9 点生成一篇 AI 日报并提交到仓库
- 优先记录高信噪比信息，而不是堆砌链接
- 在事实之外沉淀评论、判断和趋势推演
- 长期形成可检索、可回看的个人情报档案

## 重点覆盖范围

- 中美大模型公司与模型更新
- AI 编程代理与编程工具
- OpenAI / Anthropic / Google / Meta / xAI / Microsoft 等官方博客、研究、发布
- DeepSeek / Qwen / 智谱 / Kimi / MiniMax / 百度 / 腾讯 / 字节等中国 AI 厂商动态
- GitHub 热门 AI 项目、重要开源仓库与基础设施进展
- 关键投融资、政策、算力、推理服务、Agent 产品趋势

更细的覆盖清单见 [docs/coverage-map.md](docs/coverage-map.md)。

## 日报原则

- 优先一手来源：官方博客、官方公告、研究页面、官方 GitHub、公司账号
- 媒体报道只做补充，不让二手转述盖过原始信息
- 事实和判断分开写，避免把观点伪装成事实
- 每篇报告都要有评论判断层，积累连续的认知与观点
- 每条信息都尽量回答两个问题：发生了什么、为什么值得关注
- 明确日期和时间窗，避免“今天”“昨天”这类模糊表述

具体写作规范见 [docs/editorial-guidelines.md](docs/editorial-guidelines.md)。

## 仓库结构

```text
daily/                  每日日报
weekly/                 每周周报
monthly/                每月月报
yearly/                 每年年报
docs/                   覆盖范围、写作规范、工作流说明
templates/              日报/周报模板
```

各类报告默认路径：

- 日报：`daily/YYYY/YYYY-MM/YYYY-MM-DD.md`
- 周报：`weekly/YYYY/YYYY-Www.md`
- 月报：`monthly/YYYY/YYYY-MM.md`
- 年报：`yearly/YYYY/YYYY.md`

## 推荐日报结构

- 今日主线判断
- 今日评论与判断
- 最重要的 3-5 条更新
- 中美大模型动态
- AI 编程代理与开发工具
- 官方博客 / 研究 / 发布
- GitHub 热门项目与开源基础设施
- 值得继续跟踪的话题
- 参考来源

参考模板见 [templates/daily-report-template.md](templates/daily-report-template.md)。

如果你希望把日报进一步沉淀成长期认知系统，可以继续看：

- 周报模板：[templates/weekly-report-template.md](templates/weekly-report-template.md)
- 月报模板：[templates/monthly-report-template.md](templates/monthly-report-template.md)
- 长期议题台账模板：[templates/trend-ledger-template.md](templates/trend-ledger-template.md)
- 长期议题台账说明：[docs/trend-ledger.md](docs/trend-ledger.md)

## 自动化计划

- 定时：每天 09:00，Asia/Shanghai
- 时间窗：前一日 09:00 到当日 09:00
- 输出：生成当天日报 Markdown 并直接提交到本仓库 `main`

当前已经具备：

- 日报自动生成
- 周报 / 月报 / 年报自动汇总框架
- 固定 watchlist 与动态流规则
- 评论 / 判断层沉淀机制
- 结构化元数据模板
- 长期议题台账模板与方法说明

## 跨电脑恢复

这套流程现在已经支持“仓库自带安装说明 + 本机一键恢复”：

1. fork 这个仓库到你自己的 GitHub 账号，或者直接克隆你自己的副本
2. 在本地克隆仓库
3. 确保 Codex 已登录，且当前仓库具备 `git push` 权限
4. 运行 `python3 scripts/install_codex_daily_digest.py`

详细步骤见 [docs/portable-setup.md](docs/portable-setup.md)。

后续可以继续扩展：

- 按主题生成专题索引，例如 Agent、开源模型、AI 编程、推理基础设施
- 增加跨周期趋势追踪和年度回顾
- 接入 RSS / Atom / 官方账号流
- 增加推送提醒与摘要分发
