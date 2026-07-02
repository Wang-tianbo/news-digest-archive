# 固定追踪源

这是一份高优先级来源清单，用于保证日报长期保持高信噪比。总体原则是：

- 先扫官方发布、官方博客、官方文档、官方 changelog
- 再扫官方 GitHub 仓库、Release、产品动态页
- 最后再用媒体和社区热度补上下文

建议按下面三层执行，避免“源越来越多，但日报越来越散”：

- 日报必扫：核心公司官方博客、官方文档、官方 changelog、重点产品仓库 Release
- 静默日补位：第二梯队 AI 编程工具、云平台动态、开发者工具专题源
- 周报 / 月报专题：开源基础设施、模型服务框架、MCP 生态、云厂商系统层更新

## 一、海外核心官方源

- OpenAI News: [openai.com/news](https://openai.com/news/)
- OpenAI Codex: [openai.com/codex](https://openai.com/codex)
- OpenAI Codex 发布文: [Introducing Codex](https://openai.com/index/introducing-codex/)
- OpenAI Codex 更新文: [Introducing upgrades to Codex](https://openai.com/index/introducing-upgrades-to-codex/)
- OpenAI Codex Docs: [platform.openai.com/docs/codex/overview](https://platform.openai.com/docs/codex/overview)
- OpenAI API Changelog: [platform.openai.com/docs/changelog](https://platform.openai.com/docs/changelog)
- Anthropic News: [anthropic.com/news](https://www.anthropic.com/news)
- Claude Code 产品页: [anthropic.com/claude-code](https://www.anthropic.com/claude-code)
- Claude Code Docs: [docs.anthropic.com/en/docs/claude-code/overview](https://docs.anthropic.com/en/docs/claude-code/overview)
- Google AI Blog: [blog.google/technology/ai](https://blog.google/technology/ai/)
- Google DeepMind Blog: [deepmind.google/en/blog](https://deepmind.google/en/blog/)
- Gemini API Changelog: [ai.google.dev/gemini-api/docs/changelog](https://ai.google.dev/gemini-api/docs/changelog)
- Vertex AI Release Notes: [cloud.google.com/vertex-ai/generative-ai/docs/release-notes](https://cloud.google.com/vertex-ai/generative-ai/docs/release-notes)
- Meta AI Blog: [ai.meta.com/blog](https://ai.meta.com/blog/)
- xAI Docs: [docs.x.ai](https://docs.x.ai/overview)
- xAI Release Notes: [docs.x.ai/developers/release-notes](https://docs.x.ai/developers/release-notes)
- xAI Models: [docs.x.ai/developers/models](https://docs.x.ai/developers/models)
- Microsoft Blog: [blogs.microsoft.com](https://blogs.microsoft.com/)
- Azure OpenAI What's New: [learn.microsoft.com/azure/ai-foundry/openai/whats-new](https://learn.microsoft.com/en-us/azure/foundry-classic/openai/whats-new)
- Azure AI Foundry Agent Service What's New: [learn.microsoft.com/azure/ai-foundry/agents/whats-new](https://learn.microsoft.com/en-us/azure/foundry-classic/agents/whats-new?view=foundry)
- AWS Bedrock Doc History: [docs.aws.amazon.com/bedrock/latest/userguide/doc-history.html](https://docs.aws.amazon.com/bedrock/latest/userguide/doc-history.html)
- Mistral News: [mistral.ai/news](https://mistral.ai/news)
- Mistral Docs: [docs.mistral.ai](https://docs.mistral.ai/)
- Perplexity API Docs: [docs.perplexity.ai](https://docs.perplexity.ai/docs/getting-started/overview)
- Perplexity API Changelog: [docs.perplexity.ai/docs/resources/changelog](https://docs.perplexity.ai/docs/resources/changelog)
- GitHub Blog: [github.blog](https://github.blog/)
- GitHub Changelog: [github.blog/changelog](https://github.blog/changelog/)

## 二、AI 编程代理与开发工具专项源

### OpenAI / Codex

- 产品页: [openai.com/codex](https://openai.com/codex)
- 发布与升级: [Introducing Codex](https://openai.com/index/introducing-codex/), [Introducing upgrades to Codex](https://openai.com/index/introducing-upgrades-to-codex/)
- 开发文档: [platform.openai.com/docs/codex/overview](https://platform.openai.com/docs/codex/overview)
- 平台更新: [platform.openai.com/docs/changelog](https://platform.openai.com/docs/changelog)
- 官方仓库: [github.com/openai/codex](https://github.com/openai/codex)
- 版本发布: [openai/codex releases](https://github.com/openai/codex/releases)
- Agent SDK: [github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python)
- Agent SDK 发布: [openai-agents-python releases](https://github.com/openai/openai-agents-python/releases)

### Anthropic / Claude Code

- 产品页: [anthropic.com/claude-code](https://www.anthropic.com/claude-code)
- 文档: [Claude Code overview](https://docs.anthropic.com/en/docs/claude-code/overview)
- 官方仓库: [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code)
- 版本发布: [claude-code releases](https://github.com/anthropics/claude-code/releases)

### Cursor

- 官方博客: [cursor.com/blog](https://www.cursor.com/blog)
- 官方 Changelog: [cursor.com/changelog](https://cursor.com/changelog)
- 官方文档: [docs.cursor.com](https://docs.cursor.com/)
- Cursor CLI 文档: [docs.cursor.com/tools/cli](https://docs.cursor.com/tools/cli)

### GitHub Copilot

- Copilot 文档首页: [docs.github.com/en/copilot](https://docs.github.com/en/copilot)
- Copilot CLI 文档: [Using GitHub Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli/overview)
- Copilot Agent 文档: [Managing access to GitHub Copilot coding agent](https://docs.github.com/en/copilot/how-tos/agents/copilot-coding-agent/enabling-copilot-coding-agent)
- GitHub Changelog: [github.blog/changelog](https://github.blog/changelog/)
- Copilot 标签流: [github.blog/changelog/label/copilot](https://github.blog/changelog/label/copilot/)

### Gemini CLI

- 官方仓库: [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)
- 版本发布: [gemini-cli releases](https://github.com/google-gemini/gemini-cli/releases)
- Release Notes: [docs/changelogs/index.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/changelogs/index.md)
- Gemini API Changelog: [ai.google.dev/gemini-api/docs/changelog](https://ai.google.dev/gemini-api/docs/changelog)

### Devin / Cognition

- 官方首页与博客入口: [cognition.ai](https://cognition.ai/)
- Devin 知识库: [knowledge.cognition.ai](https://knowledge.cognition.ai/)
- 官方 GitHub 组织: [github.com/CognitionAI](https://github.com/CognitionAI)

### Qwen Code / Z Code

- Qwen Code Docs: [qwen-code-docs](https://qwenlm.github.io/qwen-code-docs/en/index)
- Qwen Code Blog: [qwen-code-docs blog](https://qwenlm.github.io/qwen-code-docs/en/blog/)
- Z Code Docs: [zcode.z.ai/docs](https://zcode.z.ai/docs)
- Z Code 产品页: [zcode.z.ai/en](https://zcode.z.ai/en)

### Windsurf

- 官方 Changelog: [windsurf.com/changelog](https://windsurf.com/changelog)

### Continue

- 官方博客: [blog.continue.dev](https://blog.continue.dev/)
- 官方文档: [docs.continue.dev](https://docs.continue.dev/)
- 官方仓库: [github.com/continuedev/continue](https://github.com/continuedev/continue)

### Cline

- 官方文档: [docs.cline.bot](https://docs.cline.bot/cline-overview)
- MCP 文档: [docs.cline.bot/mcp/mcp-overview](https://docs.cline.bot/mcp/mcp-overview)
- 官方仓库: [github.com/cline/cline](https://github.com/cline/cline)

### OpenHands

- 官方文档: [docs.openhands.dev](https://docs.openhands.dev/overview/introduction)
- 官方博客: [openhands.dev/blog](https://www.openhands.dev/blog)
- 官方仓库: [github.com/OpenHands/OpenHands](https://github.com/OpenHands/OpenHands)

### Sourcegraph / Cody

- 官方博客: [sourcegraph.com/blog](https://sourcegraph.com/blog)
- Cody Docs: [sourcegraph.com/docs/cody](https://sourcegraph.com/docs/cody)

### Augment

- 官方博客: [augmentcode.com/blog](https://www.augmentcode.com/blog)

### JetBrains Junie

- JetBrains AI Guide: [jetbrains.com/guide/ai](https://www.jetbrains.com/guide/ai/)
- Junie Docs: [jetbrains.com/help/ai-assistant/junie-agent.html](https://www.jetbrains.com/help/ai-assistant/junie-agent.html)

## 三、中国模型厂商专项源

### DeepSeek

- 官网: [deepseek.com](https://www.deepseek.com/)
- 透明度中心: [deepseek.com/en/transparency](https://www.deepseek.com/en/transparency/)
- 官方 GitHub: [github.com/deepseek-ai](https://github.com/deepseek-ai)

### Qwen

- 官方博客: [qwenlm.github.io/blog](https://qwenlm.github.io/blog/)
- 官方 GitHub: [github.com/QwenLM](https://github.com/QwenLM)
- Qwen Code Docs: [qwen-code-docs](https://qwenlm.github.io/qwen-code-docs/en/index)

### 智谱 / Z.ai

- 公司页: [z.ai/company](https://z.ai/company)
- 开放平台: [bigmodel.cn](https://bigmodel.cn/)
- 官方文档: [docs.bigmodel.cn](https://docs.bigmodel.cn/)
- Z Code 文档: [zcode.z.ai/docs](https://zcode.z.ai/docs)

### 月之暗面 / Kimi

- 公司页: [moonshot.cn/about](https://www.moonshot.cn/about)
- 官方博客: [platform.moonshot.cn/blog](https://platform.moonshot.cn/blog)

### MiniMax

- 官方 News: [minimax.io/news](https://www.minimax.io/news)
- 官网: [minimax.io](https://www.minimax.io/)

### 腾讯混元

- 产品页: [cloud.tencent.com/product/hunyuan](https://cloud.tencent.com/product/hunyuan)
- 文档首页: [cloud.tencent.com/document/product/1729/117864](https://cloud.tencent.com/document/product/1729/117864)
- 产品动态: [cloud.tencent.com/document/product/1729/97765](https://cloud.tencent.com/document/product/1729/97765)

### 百度文心 / 千帆

- 产品页: [cloud.baidu.com/product/wenxinworkshop.html](https://cloud.baidu.com/product/wenxinworkshop.html)
- 文档首页: [cloud.baidu.com/doc/WENXINWORKSHOP/index.html](https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html)

### 字节跳动 / 豆包 / 火山方舟

- 火山引擎首页: [volcengine.com](https://www.volcengine.com/)
- 豆包产品页: [volcengine.com/product/doubao](https://www.volcengine.com/product/doubao)
- 火山方舟文档首页: [volcengine.com/docs/82379/66619f91f281250274ef5000](https://www.volcengine.com/docs/82379/66619f91f281250274ef5000)
- 火山引擎开发者社区文章: [developer.volcengine.com/articles](https://developer.volcengine.com/articles/7462939272262189083)

### 01.AI / 零一万物

- 官网: [lingyiwanwu.com](https://www.lingyiwanwu.com/)
- 官方 GitHub: [github.com/01-ai](https://github.com/01-ai)

### 商汤 / SenseNova

- 官网: [sensenova.cn](https://www.sensenova.cn/)
- 平台首页: [platform.sensenova.cn](https://platform.sensenova.cn/)

### TRAE / MarsCode

- TRAE 首页: [trae.ai](https://www.trae.ai/)
- TRAE Blog: [trae.ai/blog](https://www.trae.ai/blog)
- TRAE Changelog: [trae.ai/changelog](https://www.trae.ai/changelog)
- MarsCode 首页: [marscode.com](https://www.marscode.com/)
- MarsCode Blog: [marscode.com/blog](https://www.marscode.com/blog)
- MarsCode Docs: [marscode.com/docs](https://www.marscode.com/docs)

## 四、开源与社区观察

- GitHub Trending: [github.com/trending](https://github.com/trending)
- Hugging Face: [huggingface.co](https://huggingface.co/)
- Hugging Face Blog: [huggingface.co/blog](https://huggingface.co/blog)
- Anthropic GitHub 组织: [github.com/anthropics](https://github.com/anthropics)
- QwenLM GitHub 组织: [github.com/QwenLM](https://github.com/QwenLM)
- DeepSeek GitHub 组织: [github.com/deepseek-ai](https://github.com/deepseek-ai)
- CognitionAI GitHub 组织: [github.com/CognitionAI](https://github.com/CognitionAI)
- vLLM Blog: [vllm.ai/blog](https://vllm.ai/blog)
- vLLM Releases: [github.com/vllm-project/vllm/releases](https://github.com/vllm-project/vllm/releases)
- SGLang Releases: [github.com/sgl-project/sglang/releases](https://github.com/sgl-project/sglang/releases)
- llama.cpp Releases: [github.com/ggml-org/llama.cpp/releases](https://github.com/ggml-org/llama.cpp/releases)
- Transformers Releases: [github.com/huggingface/transformers/releases](https://github.com/huggingface/transformers/releases)
- MCP Docs: [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/getting-started/intro)
- MCP Servers: [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
- MCP Registry: [github.com/modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry)
- NVIDIA Generative AI Blog: [developer.nvidia.com/blog/category/deep-learning/generative-ai](https://developer.nvidia.com/blog/category/deep-learning/generative-ai/)

## 五、AI 外围高相关情报

这些源不是为了把日报做成“泛科技新闻”，而是为了补足那些会反过来改变 AI 竞争格局的外围变量。

### 算力与半导体

- NVIDIA News: [nvidianews.nvidia.com/news](https://nvidianews.nvidia.com/news)
- NVIDIA Blog: [blogs.nvidia.com](https://blogs.nvidia.com/)
- NVIDIA Generative AI Blog: [developer.nvidia.com/blog/category/deep-learning/generative-ai](https://developer.nvidia.com/blog/category/deep-learning/generative-ai/)
- AMD IR Press Releases: [ir.amd.com/news-events/press-releases](https://ir.amd.com/news-events/press-releases)
- ASML News: [asml.com/en/news](https://www.asml.com/en/news)
- Micron Blog: [micron.com/about/blog](https://www.micron.com/about/blog)

### 云、数据中心与电力

- Vertex AI Release Notes: [cloud.google.com/vertex-ai/generative-ai/docs/release-notes](https://cloud.google.com/vertex-ai/generative-ai/docs/release-notes)
- Azure OpenAI What's New: [learn.microsoft.com/azure/ai-foundry/openai/whats-new](https://learn.microsoft.com/en-us/azure/foundry-classic/openai/whats-new)
- Azure AI Foundry Agent Service What's New: [learn.microsoft.com/azure/ai-foundry/agents/whats-new](https://learn.microsoft.com/en-us/azure/foundry-classic/agents/whats-new?view=foundry)
- AWS Bedrock Doc History: [docs.aws.amazon.com/bedrock/latest/userguide/doc-history.html](https://docs.aws.amazon.com/bedrock/latest/userguide/doc-history.html)
- OpenAI Global Affairs: [openai.com/global-affairs](https://openai.com/global-affairs/)
- OpenAI 基建文章: [Building the compute infrastructure for the intelligence age](https://openai.com/index/building-the-compute-infrastructure-for-the-intelligence-age/)

### 政策、监管与地缘政治

- BIS Press Releases: [bis.gov/press-release](https://www.bis.gov/press-release)
- BIS AI / 芯片规则样本页: [Department of Commerce announces rescission of the Biden-era AI diffusion rule](https://www.bis.gov/press-release/department-commerce-announces-rescission-biden-era-artificial-intelligence-diffusion-rule-strengthens)
- EU AI Act 官方页: [digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- NIST AI RMF: [nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework)
- 中国政府网“人工智能+”行动样本页: [关于深入实施“人工智能+”行动的意见](https://www.gov.cn/zhengce/202508/content_7037899.htm)

### 安全、滥用与治理

- OpenAI Security & Privacy: [openai.com/security-and-privacy](https://openai.com/security-and-privacy/)
- OpenAI Security News: [openai.com/news/security](https://openai.com/news/security/)
- Anthropic News: [anthropic.com/news](https://www.anthropic.com/news)
- CISA AI Cybersecurity Collaboration Playbook: [cisa.gov/resources-tools/resources/ai-cybersecurity-collaboration-playbook](https://www.cisa.gov/resources-tools/resources/ai-cybersecurity-collaboration-playbook)
- NIST AI RMF: [nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework)

### 企业采用、组织变革与劳动力

- Microsoft Work Trend Index: [microsoft.com/worklab/work-trend-index](https://www.microsoft.com/en-us/worklab/work-trend-index)
- Anthropic Economic Index: [anthropic.com/economic-index](https://www.anthropic.com/economic-index)
- Stanford AI Index: [hai.stanford.edu/ai-index](https://hai.stanford.edu/ai-index)
- 2025 AI Index Report: [hai.stanford.edu/ai-index/2025-ai-index-report](https://hai.stanford.edu/ai-index/2025-ai-index-report)
- UNESCO AI: [unesco.org/en/artificial-intelligence](https://www.unesco.org/en/artificial-intelligence)

### AI+ 行业落地

- Stanford AI Index 科学与医疗章节: [Science and medicine](https://hai.stanford.edu/ai-index/2025-ai-index-report/science-and-medicine)
- NVIDIA 企业 AI 新闻: [nvidianews.nvidia.com/news](https://nvidianews.nvidia.com/news)
- 中国政府网“人工智能+”行动样本页: [关于深入实施“人工智能+”行动的意见](https://www.gov.cn/zhengce/202508/content_7037899.htm)

## 六、AI 思想与观点观察源

这部分用于长期跟踪中文互联网与全球范围内的 AI 技术工作者、研究者、创业者及关键人物，在博客、X、公众号、长文中表达的判断、困惑、分歧与方法论。

使用原则：

- 这是观点源，不是事实源；不能用人物观点替代官方发布、文档、Release 或 changelog
- 优先使用博客、长文、技术文章、公开访谈和可复查文章；X / Twitter、微博、短帖只作为观点线索
- 只记录有长期复盘价值的判断、分歧、困惑与方法论；如果当天没有高信号观点，日报整段省略
- 观点进入日报时要写清楚 `观点摘要`、`为什么值得记录`、`我的判断` 和 `来源`

### 全球人物与长文源

- Andrej Karpathy Blog: [karpathy.ai](https://karpathy.ai/)
- Andrej Karpathy X: [x.com/karpathy](https://x.com/karpathy)
- Simon Willison Blog: [simonwillison.net](https://simonwillison.net/)
- Simon Willison X: [x.com/simonw](https://x.com/simonw)
- Ethan Mollick / One Useful Thing: [oneusefulthing.org](https://www.oneusefulthing.org/)
- Ethan Mollick X: [x.com/emollick](https://x.com/emollick)
- François Chollet Blog: [fchollet.com](https://fchollet.com/)
- François Chollet X: [x.com/fchollet](https://x.com/fchollet)
- Jim Fan X: [x.com/DrJimFan](https://x.com/DrJimFan)
- Sam Altman Blog: [blog.samaltman.com](https://blog.samaltman.com/)
- Sam Altman X: [x.com/sama](https://x.com/sama)
- Dario Amodei / Anthropic Essays: [anthropic.com/news](https://www.anthropic.com/news)
- Yann LeCun X: [x.com/ylecun](https://x.com/ylecun)
- Noam Brown X: [x.com/polynoamial](https://x.com/polynoamial)
- Latent Space / swyx: [latent.space](https://www.latent.space/)
- swyx X: [x.com/swyx](https://x.com/swyx)
- Andrew Ng / The Batch: [deeplearning.ai/the-batch](https://www.deeplearning.ai/the-batch/)

### 中文互联网人物与长文源

- 宝玉 Blog: [baoyu.io](https://baoyu.io/)
- 宝玉 X: [x.com/dotey](https://x.com/dotey)
- 李沐 / 动手学深度学习: [zh.d2l.ai](https://zh.d2l.ai/)
- DeepLearning.AI 中文相关内容可作为 Andrew Ng 观点的补充入口: [deeplearning.ai](https://www.deeplearning.ai/)

说明：中文个人观点源先保持保守。后续如果要加入公众号、知识星球、播客或中文长文平台，应优先选择公开可访问、能稳定引用、适合长期复查的入口。

## 七、动态流 / 可订阅流

这部分不是单个页面，而是每天应主动扫的“更新流”。

- 官方 changelog 流：
  - OpenAI API Changelog
  - xAI Release Notes
  - Cursor Changelog
  - Windsurf Changelog
  - GitHub Changelog
  - Gemini API Changelog
  - Gemini CLI Release Notes
  - Vertex AI Release Notes
  - Perplexity API Changelog
  - Qwen Code Weekly / Product Updates
  - 腾讯混元产品动态
  - 火山方舟产品动态
  - TRAE Changelog
- GitHub Release 流：
  - `openai/codex`
  - `openai/openai-agents-python`
  - `anthropics/claude-code`
  - `google-gemini/gemini-cli`
  - `vllm-project/vllm`
  - `sgl-project/sglang`
  - `ggml-org/llama.cpp`
  - `huggingface/transformers`
  - `modelcontextprotocol/servers`
  - `modelcontextprotocol/registry`
  - 重点模型与工具官方仓库
- GitHub 组织活跃流：
  - `openai`
  - `anthropics`
  - `QwenLM`
  - `deepseek-ai`
  - `CognitionAI`
  - `01-ai`
- 文档更新流：
  - Codex Docs
  - Claude Code Docs
  - Cursor Docs
  - Copilot Docs
  - xAI Docs
  - Gemini API Docs
  - Qwen Code Docs
  - BigModel Docs
  - Perplexity API Docs
  - Mistral Docs
  - 火山方舟 Docs

说明：

- GitHub Blog / Changelog 页面本身提供 RSS 能力，适合后续接入订阅。
- GitHub 仓库的 Releases、Tags、Commits 页面也适合后续接入 Atom 订阅。
- 个别官网入口对脚本访问不稳定，自动化优先选文档页、Release 页、changelog 页，官网首页作为人工补充。
- 这一步当前先作为“每日巡检规则”执行，等日报稳定后再进一步自动化订阅。

## 八、使用建议

- 每天先扫“日报必扫”源：Codex、Claude Code、Copilot、Cursor、Gemini CLI、Qwen Code，再扫中美重点模型厂商官方动态
- 如果当天出现重大模型发布，回到“发布文 + 文档 + changelog + GitHub 仓库”四件套核实
- 如果核心源当天信号偏弱，再启用“静默日补位”源，但不要为了凑篇幅重复前几日日报已经写过的内容
- 对 Codex、Claude Code、Copilot、Cursor、Gemini CLI、Devin、Qwen Code 这类产品，不只看博客，也要看文档和版本发布
- 对中国厂商，优先看产品页、文档页、官方博客、官方 GitHub，再看开发者社区和媒体报道
- 对 AI 思想与观点观察，优先记录能解释方法论变化、路线分歧、产品判断或组织采用困惑的观点；不要把人物动态做成每日签到
- 对外围情报，只选那些会真实改变 AI 主线的变量，例如算力、云平台接入、监管变化、安全治理、企业采用或关键行业落地；如果只是一般科技新闻，不进日报
- 日报里的外围情报建议控制在 1-3 条；如果当天没有高置信度外围信号，可以整段省略
- 日报里的观点观察建议控制在 1-3 条；如果当天没有高信号观点，可以整段省略
- 对 vLLM、SGLang、llama.cpp、Transformers、MCP 生态这类基础设施，更适合作为周报 / 月报中的“趋势层”素材
- 算力与半导体、政策与治理、企业采用这三类外围情报，更适合在周报 / 月报中沉淀连续判断，而不是每天机械签到
- 媒体报道只用于补充上下文，不作为最核心事实来源
