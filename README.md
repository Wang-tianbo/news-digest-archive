# AI News Digest Archive

这是一个用于沉淀 AI 行业日报、周报和专题观察的私有仓库，重点关注全球 AI 热点，尤其是中美大模型、AI 编程代理，以及相关公司发布的官方文章、博客、研究和产品更新。

## 目标

- 每天上午 9 点生成一篇 AI 日报并提交到仓库
- 优先记录高信噪比信息，而不是堆砌链接
- 长期形成可检索、可回看的个人情报档案

## 重点覆盖范围

- 中美大模型公司与模型更新
- AI 编程代理与编程工具
- OpenAI / Anthropic / Google / Meta / xAI / Microsoft 等官方博客、研究、发布
- DeepSeek / Qwen / 智谱 / Kimi / MiniMax / 百度 / 腾讯 / 字节等中国 AI 厂商动态
- GitHub 热门 AI 项目、重要开源仓库与基础设施进展
- 关键投融资、政策、算力、推理服务、Agent 产品趋势

更细的覆盖清单见 [docs/coverage-map.md](/Users/tbw/Documents/Playground/news-digest-archive/docs/coverage-map.md)。

## 日报原则

- 优先一手来源：官方博客、官方公告、研究页面、官方 GitHub、公司账号
- 媒体报道只做补充，不让二手转述盖过原始信息
- 事实和判断分开写，避免把观点伪装成事实
- 每条信息都尽量回答两个问题：发生了什么、为什么值得关注
- 明确日期和时间窗，避免“今天”“昨天”这类模糊表述

具体写作规范见 [docs/editorial-guidelines.md](/Users/tbw/Documents/Playground/news-digest-archive/docs/editorial-guidelines.md)。

## 仓库结构

```text
daily/                  每日日报
weekly/                 每周周报
docs/                   覆盖范围、写作规范、工作流说明
templates/              日报/周报模板
```

日报默认放在 `daily/YYYY/YYYY-MM/YYYY-MM-DD.md`。

## 推荐日报结构

- 今日主线判断
- 最重要的 3-5 条更新
- 中美大模型动态
- AI 编程代理与开发工具
- 官方博客 / 研究 / 发布
- GitHub 热门项目与开源基础设施
- 值得继续跟踪的话题
- 参考来源

参考模板见 [templates/daily-report-template.md](/Users/tbw/Documents/Playground/news-digest-archive/templates/daily-report-template.md)。

## 自动化计划

- 定时：每天 09:00，Asia/Shanghai
- 时间窗：前一日 09:00 到当日 09:00
- 输出：生成当天日报 Markdown 并直接提交到本仓库 `main`

后续可以继续扩展：

- 每周自动汇总成周报
- 按主题生成专题索引，例如 Agent、开源模型、AI 编程、推理基础设施
- 增加年度回顾和趋势追踪
