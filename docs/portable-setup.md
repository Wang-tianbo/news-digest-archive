# 跨电脑恢复指南

这份指南的目标很简单：不论你是换一台电脑，还是第一次 fork 这个项目，只要把仓库拉下来，再执行一次安装脚本，就能把这套 `候选收件箱 + 日报 + 日报 watchdog + 周报 + 月报 + 年报 + 企业微信提醒` 自动化恢复到可运行状态。

## 最推荐的使用方式

如果你是第一次使用，推荐按下面顺序来：

1. 在 GitHub 上 fork 这个仓库到你自己的账号
2. 把你自己的 fork 克隆到本地
3. 登录 Codex
4. 运行安装脚本
5. 可选配置企业微信群机器人 webhook
6. 等待每天 / 每周 / 每月 / 每年自动生成报告并推送到你自己的仓库

这样做的好处是：

- 各周期报告会提交到你自己的仓库，而不是别人的仓库
- 你可以自由改写 watchlist、模板和评论风格
- 后续换电脑时，只需要重新克隆你的 fork 再安装一次

## 前置条件

- 新电脑已经安装并登录 Codex
- 你使用的是自己的仓库副本，或者至少当前仓库对你可写
- `git push` 到当前仓库已经可用
- 系统里有 Python 3

## 一键安装

推荐在仓库根目录运行：

```bash
python3 scripts/install_codex_daily_digest.py
```

Windows 也可以使用：

```powershell
py -3 scripts\install_codex_daily_digest.py
```

如果你在 macOS / Linux 上更习惯 shell，也可以运行：

```bash
bash scripts/install_codex_daily_digest.sh
```

安装脚本会自动完成这几件事：

- 检查当前目录是否像一个可用的 Git 仓库
- 检查仓库里是否存在自动化模板文件
- 计算当前电脑本地时间里，对应 `Asia/Shanghai 08:40` 候选收件箱和 `09:05` 日报的触发时间
- 额外写入 UTC 时钟候选触发时间，用来兼容不同 Codex Desktop 版本对 cron `BYHOUR` 的解释差异
- 生成本机可用的 Codex 自动化配置
- 把仓库当前绝对路径写入自动化的 `cwds`
- 写入候选收件箱、日报、日报 watchdog、周报、月报、年报和企业微信提醒九个 automation 目录下的 `automation.toml`

安装器不会替你登录 Codex，也不会替你自动创建 GitHub fork；它负责的是把“这台电脑上的 Codex 自动化配置”恢复好。

## 为什么这样做

原来的自动化文件只存在于本机 `~/.codex/automations/` 下，而且写死了本机绝对路径。换电脑之后，这两个条件都会失效：

- 新电脑没有现成的自动化文件
- 原来的仓库路径通常也不一样

现在这两个问题都由仓库内脚本统一处理，仓库本身才是“真配置源”。

如果你是第一次 fork 这个项目，还要多注意一点：

- 各周期报告默认都会 `push origin main`
- 所以 `origin` 最好指向你自己的 GitHub 仓库
- 如果 `origin` 还是别人的仓库，而你又没有写权限，日报生成后会在 push 这一步失败

## 时区处理

日报的业务时间仍然固定为 `Asia/Shanghai 09:00`，自动化实际触发时间为 `Asia/Shanghai 09:05`。

同时，安装器也会一并安装：

- 候选收件箱：每天 `08:40 Asia/Shanghai`
- 日报 watchdog：每天 `09:35 Asia/Shanghai`
- 周报：每周一 `09:10 Asia/Shanghai`
- 月报：每月 `1` 日 `09:15 Asia/Shanghai`
- 年报：每年 `1` 月 `1` 日 `09:20 Asia/Shanghai`
- 日报企业微信提醒：不发送；日报只归档到 GitHub
- 周报企业微信提醒：周报 push 成功后立即发送，另有每周一 `10:15 Asia/Shanghai` 兜底检查
- 月报企业微信提醒：每月 `1` 日 `10:20 Asia/Shanghai`
- 年报企业微信提醒：每年 `1` 月 `1` 日 `10:25 Asia/Shanghai`

日报晚 5 分钟触发，是为了避开本机多个 Codex automation 同时在 `09:00` 启动时可能出现的后台静默结束。报告归档仍按 `09:00-09:00 Asia/Shanghai` 计算，不会改变日报内容口径。

日报 watchdog 是一层保险丝：它每天 `09:35` 检查当天日报文件是否已经存在。如果主日报任务正常完成，watchdog 不会修改仓库；如果主任务触发后静默失败或没有落盘，watchdog 会按同一日报规则补写并推送。

候选收件箱任务每天 `08:40` 只生成 `.codex-run/signal-reviews/YYYY-MM-DD.md`，供 `09:05` 日报读取。它不修改 Git、不提交、不推送、不发通知；如果失败，日报仍会按原有 watchlist 规则生成。

安装脚本不会直接假设“每台电脑都在中国时区”，而是会优先使用当前电脑的 IANA 本地时区规则，把日报、周报、月报、年报各自对应的 `Asia/Shanghai` 触发时刻换算成本地触发时间，再写入自动化配置。这样你在另一台电脑上恢复时，不需要手工改时间。

同时，安装脚本也会额外写入 UTC 时钟候选触发点。这样做是因为 Codex Desktop 的 cron 在不同版本中可能把 `BYHOUR` 当作本地时钟，也可能当作 UTC 时钟；双候选能避免任务被推迟到 `17:xx Asia/Shanghai` 才触发。真正执行前，自动化提示词会再次校验当前是否处于正确的 `Asia/Shanghai` 业务窗口，并检查当天日报是否已经存在，所以多出来的候选触发只会 no-op，不会重复生成报告。

对于存在夏令时的时区，安装器会写入覆盖冬令时与夏令时的本地触发候选时刻；真正执行前，自动化提示词还会再次检查当前是否处于对应的 `Asia/Shanghai` 业务窗口，不在窗口内就直接 no-op，因此不会误生成重复报告。

说明：

- 如果系统时区之后发生变化，建议重跑一次安装脚本
- 如果你把仓库移动到了新的绝对路径，也建议重跑一次安装脚本
- 如果你在多台电脑上安装同一仓库的 automation，建议只保留一台机器作为主动写入端，其余机器暂停日报类 automation，避免多端同时生成同一天报告

## 验证方法

安装完成后，可以检查下面这些文件是否已生成：

- `${CODEX_HOME:-~/.codex}/automations/daily-ai-digest-archive/automation.toml`
- `${CODEX_HOME:-~/.codex}/automations/daily-ai-signal-inbox/automation.toml`
- `${CODEX_HOME:-~/.codex}/automations/daily-ai-digest-watchdog/automation.toml`
- `${CODEX_HOME:-~/.codex}/automations/weekly-ai-digest-summary/automation.toml`
- `${CODEX_HOME:-~/.codex}/automations/monthly-ai-digest-summary/automation.toml`
- `${CODEX_HOME:-~/.codex}/automations/yearly-ai-digest-summary/automation.toml`
- `${CODEX_HOME:-~/.codex}/automations/weekly-ai-digest-notify/automation.toml`
- `${CODEX_HOME:-~/.codex}/automations/monthly-ai-digest-notify/automation.toml`
- `${CODEX_HOME:-~/.codex}/automations/yearly-ai-digest-notify/automation.toml`

也可以按下面的清单自检：

1. 重新打开 Codex，确认自动化已经出现在本机配置里
2. 运行 `git remote -v`，确认 `origin` 指向你自己的仓库
3. 确认每天 09:05 Asia/Shanghai 之后，日报会写入 `daily/YYYY/YYYY-MM/YYYY-MM-DD.md`
4. 确认每天 08:40 Asia/Shanghai 的候选收件箱 automation 文件已经生成
5. 确认每天 09:35 Asia/Shanghai 的 watchdog automation 文件已经生成
6. 确认周报 / 月报 / 年报和企业微信提醒的 automation 文件也已经生成
7. 运行 `python3 scripts/check_archive_health.py --fetch`，确认最近日报、已完成周报、已完成月报、本机 automation 和 Git 远端同步状态正常

如果你只是想先验证安装器是否工作，不想等到第二天，也可以先检查自动化文件是否已经生成，再手动阅读里面的 `cwds` 和 `rrule` 是否符合预期。

在中国时区机器上，候选收件箱的 `rrule` 通常应同时包含 `BYHOUR=0,8;BYMINUTE=40`，日报主任务应同时包含 `BYHOUR=1,9;BYMINUTE=5`，watchdog 应同时包含 `BYHOUR=1,9;BYMINUTE=35`。其中本地小时覆盖本地时钟解释，UTC 小时覆盖 UTC 时钟解释；真正写报告的仍只有上海时间业务窗口。

## 企业微信提醒配置

企业微信提醒默认使用群机器人 webhook。它只发送报告摘要和 GitHub 链接，不会把完整报告刷进群里。

在仓库根目录创建本机私有配置：

```bash
mkdir -p .codex-run
cat > .codex-run/wecom-notify.env <<'EOF'
WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY
EOF
```

注意：

- `.codex-run/` 已被 Git 忽略，适合放本机密钥和通知状态
- 不要把 webhook 写进 README、自动化模板或任何会提交的文件
- 如果不配置 `WECOM_WEBHOOK_URL`，通知任务会安全跳过，不影响报告生成

配置后可以先预览摘要，不发送真实消息：

```bash
python3 scripts/send_wecom_report.py --kind weekly --dry-run
```

如果需要手动补发，可以使用：

```bash
python3 scripts/send_wecom_report.py --kind weekly --force
```

## 常见问题

### 1. 安装脚本提示当前目录不是有效仓库

通常是因为你没有在仓库根目录执行脚本，或者仓库没有完整克隆下来。回到项目根目录后重新运行即可。

### 2. 报告生成了，但 push 失败

最常见原因有两个：

- Codex 没有可用的 GitHub 凭据
- `origin` 不是你自己的可写仓库

先运行 `git remote -v` 检查远端，再确认你能手动 `git push`。

### 3. 我换了电脑或者换了仓库路径

直接重新运行一次安装脚本即可。

### 4. 我改了系统时区

也建议重跑一次安装脚本，让本地触发时间重新按当前时区计算。

## 当前边界

- 这套方案解决的是“换电脑后如何恢复同一套多周期自动化”
- 它不代替 Codex 登录，也不代替 GitHub 凭据配置
- 如果你未来还要加季度报、专题报，也可以沿用同样的模板和安装方式继续扩展
