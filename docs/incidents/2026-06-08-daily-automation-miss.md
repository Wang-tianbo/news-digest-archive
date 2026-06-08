# 2026-06-08 日报自动化缺失复盘

- 复盘时间：2026-06-08 10:00 Asia/Shanghai
- 影响范围：`2026-06-07` 和 `2026-06-08` 日报未在预期 09 点档生成
- 修复状态：已修复本机 automation 配置和仓库安装器；缺失日报已补写

## 现象

- `python3 scripts/check_archive_health.py --today 2026-06-08` 显示缺失 `daily/2026/2026-06/2026-06-07.md` 和 `daily/2026/2026-06/2026-06-08.md`
- 仓库本身干净，`main` 与 `origin/main` 同步
- `2026-06-08 09:38 Asia/Shanghai` 前只看到周报 session 成功运行，没有看到日报主任务或 watchdog 在 09 点档运行

## 关键证据

- `2026-06-06 09:06 Asia/Shanghai`：日报主任务成功生成 `2026-06-06` 日报
- `2026-06-06 09:35 Asia/Shanghai`：watchdog 成功验证当日日报存在
- `2026-06-06 17:06 / 17:35 Asia/Shanghai`：日报主任务和 watchdog 又各触发一次，但因真实上海时间不在 09 点窗口而 no-op
- `2026-06-07 17:07 / 17:36 Asia/Shanghai`：日报主任务和 watchdog 只在 17 点档触发，并因不在 09 点窗口 no-op
- `2026-06-08 09:11 Asia/Shanghai`：周报任务成功运行并提交，说明 Codex automation 整体未完全停摆

`2026-06-07` 日报 session 的内部时间戳为 `2026-06-07T09:07:16Z`，换算为 `2026-06-07 17:07 Asia/Shanghai`。任务随后执行 `TZ=Asia/Shanghai date` 得到 `2026-06-07T17:07:34+0800`，并按提示词窗口规则安全退出。

## 根因判断

最可能根因是 Codex Desktop cron 对 `BYHOUR` 的解释在当前版本 / 调度状态中出现了本地时钟与 UTC 时钟混用或切换。

旧配置写入的是：

```text
BYHOUR=9;BYMINUTE=5
BYHOUR=9;BYMINUTE=35
```

当 Codex 按本地时钟解释时，任务会在 `09:05 / 09:35 Asia/Shanghai` 运行；当 Codex 按 UTC 时钟解释时，同一配置会在 `17:05 / 17:35 Asia/Shanghai` 运行。由于日报提示词正确地拒绝 09 点窗口外执行，所以 17 点档触发只会 no-op，最终造成日报缺失。

## 修复

- 安装器改为同时写入本地时钟和 UTC 时钟候选触发点
- 中国时区机器上的日报主任务变为 `BYHOUR=1,9;BYMINUTE=5`
- 中国时区机器上的 watchdog 变为 `BYHOUR=1,9;BYMINUTE=35`
- 日报主任务新增文件存在检查：如果当天日报已存在，直接 no-op，不改仓库
- 文档补充双时钟候选的原因、验证方式和故障判断方法

## 验证

本机已重新运行：

```bash
python3 scripts/install_codex_daily_digest.py
python3 -m py_compile scripts/install_codex_daily_digest.py scripts/check_archive_health.py
```

本机 automation 当前确认：

```text
daily-ai-digest-archive: BYHOUR=1,9;BYMINUTE=5
daily-ai-digest-watchdog: BYHOUR=1,9;BYMINUTE=35
weekly-ai-digest-summary: BYHOUR=1,9;BYMINUTE=10
monthly-ai-digest-summary: BYHOUR=1,9;BYMINUTE=15
yearly-ai-digest-summary: BYHOUR=1,9;BYMINUTE=20
```

## 后续观察

- `2026-06-09 09:05 Asia/Shanghai` 应至少有一个候选触发进入真实 09 点窗口并生成日报
- 如果同一天另一个候选触发进入 17 点档，应只记录 no-op，不应修改仓库
- `2026-06-09 09:35 Asia/Shanghai` watchdog 应验证当天日报存在；如果主任务仍未落盘，应补写
