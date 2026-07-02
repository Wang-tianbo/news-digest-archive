# 固定追踪源

这是一份高优先级来源清单，用于保证日报长期保持高信噪比。总体原则是：

- 先扫官方发布、官方博客、官方文档、官方 changelog
- 再扫官方 GitHub 仓库、Release、产品动态页
- 最后再用媒体和社区热度补上下文

建议按下面三层执行，避免“源越来越多，但日报越来越散”：

- 日报必扫：核心公司官方博客、官方文档、官方 changelog、重点产品仓库 Release
- 静默日补位：第二梯队 AI 编程工具、云平台动态、开发者工具专题源
- 研究前沿巡检：高价值论文、研究博客、benchmark / eval、开源实现和权威解读
- 周报 / 月报专题：开源基础设施、模型服务框架、MCP 生态、云厂商系统层更新和阶段性研究路线变化

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

## 五、AI 研究前沿源

这部分用于捕捉能帮助判断未来技术路线的论文、研究博客、benchmark、eval、开源实现和实验室动向。

使用原则：

- 研究条目必须优先保留论文或研究动向原文链接
- 权威解读只作为辅助材料，不能替代原文
- 日报建议控制在 1-3 条，不做论文列表
- 每条研究前沿都要回答“为什么可能影响未来”和“局限 / 待验证点”
- 如果研究信号来自论文实现或热门仓库，应同时保留论文原文和代码仓库链接

### 论文与聚合源

- arXiv cs.CL recent: [arxiv.org/list/cs.CL/recent](https://arxiv.org/list/cs.CL/recent)
- arXiv cs.LG recent: [arxiv.org/list/cs.LG/recent](https://arxiv.org/list/cs.LG/recent)
- arXiv cs.AI recent: [arxiv.org/list/cs.AI/recent](https://arxiv.org/list/cs.AI/recent)
- arXiv cs.CV recent: [arxiv.org/list/cs.CV/recent](https://arxiv.org/list/cs.CV/recent)
- arXiv cs.RO recent: [arxiv.org/list/cs.RO/recent](https://arxiv.org/list/cs.RO/recent)
- Hugging Face Papers: [huggingface.co/papers](https://huggingface.co/papers)
- Hugging Face Trending Papers: [huggingface.co/papers/trending](https://huggingface.co/papers/trending)
- Papers with Code: [paperswithcode.com](https://paperswithcode.com/)
- alphaXiv: [alphaxiv.org](https://www.alphaxiv.org/)

### 研究博客与实验室动向

- OpenAI Research: [openai.com/research](https://openai.com/research/)
- Anthropic Research: [anthropic.com/research](https://www.anthropic.com/research)
- Google DeepMind Blog: [deepmind.google/en/blog](https://deepmind.google/en/blog/)
- Meta AI Blog: [ai.meta.com/blog](https://ai.meta.com/blog/)
- Microsoft Research AI: [microsoft.com/research/research-area/artificial-intelligence](https://www.microsoft.com/en-us/research/research-area/artificial-intelligence/)
- Stanford HAI: [hai.stanford.edu](https://hai.stanford.edu/)
- Berkeley BAIR Blog: [bair.berkeley.edu/blog](https://bair.berkeley.edu/blog/)
- Qwen Blog: [qwenlm.github.io/blog](https://qwenlm.github.io/blog/)
- DeepSeek GitHub: [github.com/deepseek-ai](https://github.com/deepseek-ai)

### Benchmark / Eval / 开源实现

- SWE-bench: [swebench.com](https://www.swebench.com/)
- Chatbot Arena / LMSYS: [lmarena.ai](https://lmarena.ai/)
- HELM: [crfm.stanford.edu/helm](https://crfm.stanford.edu/helm/latest/)
- OpenCompass: [github.com/open-compass/opencompass](https://github.com/open-compass/opencompass)
- Hugging Face Models: [huggingface.co/models](https://huggingface.co/models)
- Hugging Face Spaces: [huggingface.co/spaces](https://huggingface.co/spaces)
- GitHub Trending AI: [github.com/trending](https://github.com/trending)

### 权威解读辅助源

- 论文作者、实验室官方博客、项目核心维护者的一手解读
- Simon Willison、Nathan Lambert / Interconnects、Sebastian Raschka、Chip Huyen、Hamel Husain、Eugene Yan、Jason Liu、Jack Clark / Import AI 等高质量技术长文
- 宝玉、李继刚、歸藏、WaytoAGI、响马等中文技术工作者或 AI 博主的公开解读

## 六、AI 外围高相关情报

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

## 七、AI 圈博主源

这部分用于长期跟踪中文互联网与全球范围内活跃且核心的 AI 博主、技术工作者、研究者、创业者及关键人物，在博客、X、公众号、长文中表达的高价值线索、判断、困惑、分歧与方法论。

使用原则：

- 这是观点 / 线索源，不是事实源；不能用个人观点或资讯整理替代官方发布、文档、Release、changelog 或原始项目链接
- 核心日常雷达里的资讯整理型博主可以提供高价值 AI 线索、工具发现、社区信号或产品动态，但进入日报时必须标明 `类型：信息线索`
- 观点、方法论或实践复盘进入日报时，建议标明 `类型：观点判断`、`类型：方法论` 或 `类型：实践复盘`
- 优先使用博客、长文、技术文章、公开访谈、公众号原文和可复查文章；X / Twitter、微博、短帖可以作为线索源，但重要事实应尽量补官方或原始来源
- 核心池不是每日必写池；如果当天没有高价值线索或观点样本，日报整段省略
- 条目进入日报时要写清楚 `类型`、`摘要`、`为什么值得记录`、`我的判断` 和 `来源`

### 核心日常雷达

#### 中文核心

| 人物 / 账号 | 重点观察方向 | 日报口径 | 首选入口 |
| --- | --- | --- | --- |
| 宝玉 / dotey | AI Agent、AI 编程、Prompt、软件工程实践 | 可写观点、方法论、实践复盘、重要线索 | [Blog](https://baoyu.io/), [X](https://x.com/dotey) |
| 歸藏 / op7418 | AI 工具、设计工作流、多模态、产品实践 | 可写产品发现、工具体验、观点判断 | [Website](https://www.guizang.ai/), [X](https://x.com/op7418) |
| Gorden_Sun | AI 新产品、新模型、热点变化 | 可写高价值资讯线索和社区信号 | [X](https://x.com/Gorden_Sun) |
| 小互 / XiaoHu | AI 日报、工具、产品体验、趋势解读 | 可写高价值资讯线索和社区信号 | 公开 X / 公众号入口，日报引用时补原始链接 |
| shao__meng | Agent、MCP、AI 创业、工作流实践 | 可写观点、实践复盘、重要线索 | [X](https://x.com/shao__meng) |
| goocarlos | Dify、AI 应用搭建、Agent 产品化 | 可写实践复盘、工具动态、重要线索 | [X](https://x.com/goocarlos) |
| Tumeng05 | LLM、RAG、Agent、AI 创业落地 | 可写实践复盘、产品判断、重要线索 | [X](https://x.com/Tumeng05) |
| Axton Liu | Prompt、AI 自动化、Agent 工作流 | 可写方法论、实践复盘、重要线索 | 公开 X / 公众号入口，日报引用时补原始链接 |
| 向阳乔木 / vista8 | AI 产品、工作流、Vibe Coding、趋势判断 | 可写工具体验、趋势判断、重要线索 | [X](https://x.com/vista8) |
| 李继刚 / lijigang | Prompt 方法论、AI 写作、认知工具 | 可写方法论和观点判断 | [GitHub](https://github.com/lijigang/write-prompt), 公众号 `Write Prompt` |
| WaytoAGI | AI 知识整理、前沿资源、学习路径 | 可写高价值资源线索和方法论总结 | [GitHub](https://github.com/waytoagi), 公众号 / 社群公开入口 |
| 响马 / xicilion | AI 编程、开发者工作流、工程实践 | 可写工程实践、工具判断、重要线索 | [X](https://x.com/xicilion) |
| Orange AI / oran_ge | AI 创业、产品、国内模型与应用生态 | 可写产品动态、创业观察、重要线索 | [Blog](https://blog.orangesai.com/) |
| AI进化论 花生 / AlchainHust | AI Native 产品、AI 编程、工具实践 | 可写产品发现、实践复盘、重要线索 | [X](https://x.com/AlchainHust) |

#### 全球核心

| 人物 / 账号 | 重点观察方向 | 日报口径 | 首选入口 |
| --- | --- | --- | --- |
| Simon Willison | LLM 工程、AI 编程、开源工具 | 可写工程实践、工具发现、观点判断 | [Blog](https://simonwillison.net/), [X](https://x.com/simonw) |
| Nathan Lambert / Interconnects | 开源模型、训练范式、产业判断 | 可写观点判断、研究线索、路线分歧 | [Interconnects](https://www.interconnects.ai/) |
| swyx / Latent Space | AI Engineer、Agent 工程、开发者生态 | 可写社区信号、工程趋势、观点判断 | [Latent Space](https://www.latent.space/), [swyx.io](https://www.swyx.io/) |
| Sebastian Raschka | LLM 研究、模型机制、技术教育 | 可写研究解读、技术线索、方法论 | [Ahead of AI](https://magazine.sebastianraschka.com/), [Blog](https://sebastianraschka.com/blog/) |
| Chip Huyen | AI Engineering、评估、生产化 | 可写工程方法论、实践复盘 | [Blog](https://huyenchip.com/) |
| Hamel Husain | evals、LLM 产品改进、工程实践 | 可写评估方法、实践复盘、工具线索 | [Blog](https://hamel.dev/) |
| Eugene Yan | AI 产品、推荐系统、LLM 工程 | 可写工程实践、产品判断 | [Blog](https://eugeneyan.com/) |
| Jason Liu | RAG、结构化输出、AI 工程落地 | 可写工具实践、工程方法、重要线索 | [Blog](https://jxnl.co/) |
| Jack Clark / Import AI | AI 研究、产业、安全与社会影响 | 可写研究线索、产业判断、风险观察 | [Import AI](https://importai.substack.com/) |
| Andrew Ng / The Batch | AI 应用、创业、教育、产业落地 | 可写产业信号、创业判断、应用案例 | [The Batch](https://www.deeplearning.ai/the-batch/) |
| Ethan Mollick | AI 组织采用、教育、工作方式变化 | 可写组织采用、实践观察、观点判断 | [One Useful Thing](https://www.oneusefulthing.org/) |
| Arvind Narayanan / Sayash Kapoor | AI 泡沫、风险、社会影响、反 hype | 可写风险判断、反共识观点 | [AI Snake Oil](https://www.aisnakeoil.com/) |
| Jim Fan | Agent、机器人、具身智能、Physical AI | 可写研究线索、路线判断 | [Website](https://jimfan.me/), [X](https://x.com/DrJimFan) |
| Riley Goodside | Prompt、模型行为、AI 交互边界 | 可写模型行为线索、Prompt 实验 | [X](https://x.com/goodside) |

### 低频关键人物候选

这些人不进入日常强制巡检，但出现公开长文、长访谈、演讲、一手文章，或重大短帖判断时可进入日报。

| 区域 | 人物 | 触发条件 |
| --- | --- | --- |
| 全球 | Andrej Karpathy、Lilian Weng、François Chollet、Yann LeCun、Dario Amodei、Sam Altman、Demis Hassabis、Jensen Huang | 长文、公开演讲、重大短帖、路线争议或战略判断 |
| 中文 | 梁文锋、李沐、苏剑林、张俊林、刘知远、唐杰、朱松纯、王小川、杨植麟、李开复、周鸿祎 | 长访谈、公开演讲、一手文章、重大短帖或关键行业判断 |

## 八、动态流 / 可订阅流

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

## 九、使用建议

- 每天先扫“日报必扫”源：Codex、Claude Code、Copilot、Cursor、Gemini CLI、Qwen Code，再扫中美重点模型厂商官方动态
- 如果当天出现重大模型发布，回到“发布文 + 文档 + changelog + GitHub 仓库”四件套核实
- 如果核心源当天信号偏弱，再启用“静默日补位”源，但不要为了凑篇幅重复前几日日报已经写过的内容
- 对 Codex、Claude Code、Copilot、Cursor、Gemini CLI、Devin、Qwen Code 这类产品，不只看博客，也要看文档和版本发布
- 对中国厂商，优先看产品页、文档页、官方博客、官方 GitHub，再看开发者社区和媒体报道
- 对 AI 圈博主，优先扫描核心日常雷达；资讯整理型博主可以提供高价值线索，但必须标注为 `信息线索`，不要把人物动态做成每日签到
- 对 AI 研究前沿，优先保留原文链接；有作者、研究员、核心开发者或可信技术博主的权威解读时，可以作为辅助阅读材料，但不能替代原文
- 对外围情报，只选那些会真实改变 AI 主线的变量，例如算力、云平台接入、监管变化、安全治理、企业采用或关键行业落地；如果只是一般科技新闻，不进日报
- 日报里的外围情报建议控制在 1-3 条；如果当天没有高置信度外围信号，可以整段省略
- 日报里的观点观察建议控制在 1-3 条；如果当天没有高价值线索或观点样本，可以整段省略
- 日报里的研究前沿建议控制在 1-3 条；如果当天没有高价值论文或研究动向，可以整段省略
- 对 vLLM、SGLang、llama.cpp、Transformers、MCP 生态这类基础设施，更适合作为周报 / 月报中的“趋势层”素材
- 算力与半导体、政策与治理、企业采用这三类外围情报，更适合在周报 / 月报中沉淀连续判断，而不是每天机械签到
- 媒体报道只用于补充上下文，不作为最核心事实来源
