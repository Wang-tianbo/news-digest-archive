# 长期议题台账 - China Open Agent Runtime

## 基本信息

```yaml
slug: china-open-agent-runtime
title: 中国公开 Agent Runtime
status: watch
created_on: 2026-06-01
last_updated: 2026-06-01
promoted_from:
  - weekly/2026/2026-W20.md
  - weekly/2026/2026-W21.md
promotion_reason: Qwen Code 连续出现高频工程更新，但中国侧整体公开节奏仍需验证
owners:
  companies:
    - Qwen
    - Z.ai
    - DeepSeek
  products:
    - Qwen Code
    - Z Code
themes:
  - china_open_agent_runtime
  - agent_runtime
  - open_source_surface
region_scope:
  - china
fact_confidence: high
signal_strength: medium
```

## 议题定义

- 这个议题追踪中国侧是否会形成公开、连续、可复现的 agent runtime 产品和工程节奏。
- 长期价值在于判断中国公司是否能在 coding agent runtime 层形成独立公开节奏，而不是只在基础模型或平台 API 上竞争。
- 不应把所有中国 AI 公司动态都纳入本议题；只有公开 agent runtime、CLI、IDE、MCP、worktree、session、permission 等相关信号才计入。

## 关键问题

- Qwen Code 是否会成为中国侧最稳定的公开 agent runtime 样本
- Z Code、DeepSeek 或其他中国厂商是否会给出同等级公开工程节奏
- 中国侧公开 runtime 能否从 release 流进入文档、案例和平台叙事

## 时间线

### 2026-06-01

- 新增事实：2026-W20 和 2026-W21 周报持续记录 Qwen Code 的 daemon、MCP、worktree、diagnostics、goal、auto approval、subagent 等工程更新。
- 当时判断：Qwen Code 已经是中国侧最值得跟踪的公开 agent runtime 线，但其他厂商公开节奏尚未形成同等级连续信号。
- 判断变化：该议题从周报观察项升格为长期观察议题，状态暂定 `watch`。
- 来源：
  - [2026-W20 周报](../weekly/2026/2026-W20.md)
  - [2026-W21 周报](../weekly/2026/2026-W21.md)

## 当前判断

- 基于截至目前样本的判断：Qwen Code 在公开工程节奏上已经有明显连续性，但“中国公开 agent runtime”作为赛道判断仍需要更多公司和更多文档/案例支撑。
- 当前最强信号：Qwen Code 高频 release 覆盖 daemon、MCP、worktree、goal、approval、diagnostics、subagent。
- 当前最大不确定性：中国侧其他公司是否会跟进，以及 Qwen Code 是否能把工程更新转化为开发者生态。

## 连续性信号

- 已连续出现的公司动作：Qwen Code 多日多版本推进 runtime 能力。
- 已连续出现的产品动作：worktree isolation、progressive MCP、goal continuation、auto approval、memory diagnostics、foreground subagent persistence。
- 已连续出现的方法论变化：观察中国侧竞争不能只看基础模型 headline，也要看公开工程节奏。

## 反证与修正条件

- 如果 Qwen Code 后续 release 明显放缓，且没有文档/案例/生态接续，需要降权。
- 如果只有 Qwen Code 一个样本，应避免过早上升为“中国侧整体趋势”。
- 如果 Z Code 或其他产品出现连续公开 runtime 更新，可以提升 signal_strength。

## 下次更新时重点看什么

- Qwen Code 是否把 preview 能力推到稳定版
- Qwen Code 是否出现更多官方文档、案例和平台接入说明
- Z Code、DeepSeek 或其他中国厂商是否出现可复现 release / docs / changelog

## 关联报告

- 日报：
- 周报：
  - [2026-W20](../weekly/2026/2026-W20.md)
  - [2026-W21](../weekly/2026/2026-W21.md)
- 月报：
- 年报：

## 退出条件

- 什么时候可以判定这个议题进入稳定现实：至少两个中国侧公开 agent runtime 产品形成连续 release、文档和开发者使用反馈。
- 什么时候应该降低权重：连续两个周报没有 Qwen Code 或其他中国侧 runtime 新增事实。
- 什么时候应该拆分或归档：Qwen Code 单独成为主线，而其他中国侧产品长期没有可比信号。
