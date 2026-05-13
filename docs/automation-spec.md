# 日报自动化规范

这份文档定义每天 09:00 自动生成 AI 日报时应遵循的规则。

## 目标

- 生成一篇简洁、高信噪比、可回看的 AI 日报
- 聚焦全球 AI 热点，重点覆盖中美大模型与 AI 编程代理
- 将结果直接提交到本仓库，供后续查阅

## 时间口径

- 执行时间：每天 09:00，Asia/Shanghai
- 报告时间窗：前一日 09:00 至当日 09:00

## 报告要求

- 输出文件路径：`daily/YYYY/YYYY-MM/YYYY-MM-DD.md`
- 标题格式：`# AI 日报 - YYYY-MM-DD`
- 必须包含可点击来源链接
- 必须优先使用官方来源
- 必须使用绝对日期，避免“今天”“昨天”

## 选题优先级

1. OpenAI、Anthropic、Google、Meta、Microsoft、GitHub 的官方更新
2. DeepSeek、Qwen、智谱、Kimi、MiniMax 等中国模型公司的重要进展
3. Codex、Claude Code、Copilot、Cursor、Devin、Gemini CLI 等 AI 编程工具动态
4. GitHub 热门 AI 项目和关键开源基础设施
5. 投融资、监管、合作、算力和推理服务等会改变格局的事件

## 写作原则

- 少而精，宁可少写，也不要堆砌
- 每条重点信息回答：发生了什么、为什么重要
- 区分“事实”与“判断”
- 对不确定信息明确标注

## Git 要求

- 只提交本次生成或更新的日报文件
- commit message 使用：`docs: add ai digest for YYYY-MM-DD`
- 默认推送到 `main`

## 失败处理

- 如果当天高价值更新很少，仍生成简版日报
- 如果抓取过程受阻，保留已验证的重要信息，不用未经确认的内容凑数
