# 长期议题台账 - Agent Runtime Governance

## 基本信息

```yaml
slug: agent-runtime-governance
title: Agent 运行时治理
status: rising
created_on: 2026-06-01
last_updated: 2026-06-01
promoted_from:
  - weekly/2026/2026-W20.md
  - weekly/2026/2026-W21.md
promotion_reason: 连续两周出现运行时、权限、会话、后台任务和团队治理信号
owners:
  companies:
    - OpenAI
    - Anthropic
    - GitHub
    - Google
    - Qwen
  products:
    - Codex
    - Claude Code
    - GitHub Copilot
    - Gemini CLI
    - Qwen Code
themes:
  - agent_runtime
  - runtime_governance
  - session_orchestration
region_scope:
  - us
  - china
fact_confidence: high
signal_strength: high
```

## 议题定义

- 这个议题追踪 AI 编程代理从单次交互工具演进为可长期运行、可审计、可调度、可治理的软件运行时。
- 长期价值在于判断哪些公司能把 agent 做进真实团队流程，而不是停留在演示能力。
- 不应与单个模型能力提升混淆；这里关注的是权限、会话、后台任务、工作区隔离、审计、成本和团队管理。

## 关键问题

- 编程代理的主要竞争点是否正在从模型能力转向运行时治理能力
- 哪些产品率先把权限、会话、后台任务和团队策略做成默认能力
- 哪些信号说明该议题已经从趋势进入稳定现实

## 时间线

### 2026-06-01

- 新增事实：2026-W20 和 2026-W21 周报都把 agent runtime、session、permission、background task、team metrics 作为主线。
- 当时判断：运行时治理已经是 AI 编程代理竞争的核心层。
- 判断变化：该议题从周度重复信号升格为长期议题。
- 来源：
  - [2026-W20 周报](../weekly/2026/2026-W20.md)
  - [2026-W21 周报](../weekly/2026/2026-W21.md)

## 当前判断

- 基于截至目前样本的判断：Agent 运行时治理正在成为 AI 编程代理产品化的关键分水岭。
- 当前最强信号：OpenAI、Anthropic、GitHub、Google、Qwen 都在围绕会话、权限、后台任务、工作区隔离和团队可管理性持续迭代。
- 当前最大不确定性：这些能力是否会成为企业采购和团队迁移的决定因素，仍需要更多落地样本验证。

## 连续性信号

- 已连续出现的公司动作：OpenAI Codex、Anthropic Claude Code、GitHub Copilot、Gemini CLI、Qwen Code 都出现运行时层更新。
- 已连续出现的产品动作：permission profile、background session、agent task API、session protocol、worktree isolation、diagnostics。
- 已连续出现的方法论变化：观察重点从“模型是否更强”转向“agent 是否能长期、安全、可治理地运行”。

## 反证与修正条件

- 如果后续几周主要更新重新回到单点模型 headline，而运行时能力不再推进，需要下调该议题权重。
- 如果运行时治理能力分化成企业治理、个人长任务、云端调度三条不同主线，需要拆分议题。

## 下次更新时重点看什么

- GitHub Copilot agent task API 是否形成闭环
- Claude Code background sessions 是否继续加强团队治理
- Codex permission / goal / remote-control 是否进入更明确的企业叙事
- Qwen Code 是否把 preview 运行时能力稳定化

## 关联报告

- 日报：
- 周报：
  - [2026-W20](../weekly/2026/2026-W20.md)
  - [2026-W21](../weekly/2026/2026-W21.md)
- 月报：
- 年报：

## 退出条件

- 什么时候可以判定这个议题进入稳定现实：主要 AI 编程代理产品都默认提供会话治理、权限策略、后台任务和团队审计能力。
- 什么时候应该降低权重：连续两个周报没有新增运行时治理事实或判断变化。
- 什么时候应该拆分或归档：议题过大，且企业治理、个人长任务、云端调度出现清晰不同演进路径。
