# intgral-guide-skill

供成员交给语言模型使用的团队工作指南。描述要推进的工作，模型会先找到相关资料，再厘清目标、责任角色、依赖、下一步行动与完成标准。

本公开仓库保存可复用的方法、通用角色和空配置示例。实际成员、项目目标、内部来源与审批规则在团队私有系统中维护。

调用名：`intgral-guide-skill`。仓库：https://github.com/intgral-ai/intgral-guide-skill。

仓库另含完整的 [intgral-knowledge-workflow](skills/intgral-knowledge-workflow/SKILL.md)，连接 Wispr 会议、早期想法、Decision、docs、更新通知与执行反馈；[intgral-meeting-prepare](skills/intgral-meeting-prepare/SKILL.md) 负责会前 Draft。原 `$intgral-meeting` 保留为兼容入口。

## 会前准备

开会前运行 `$intgral-meeting-prepare`。它会读取 docs 中最新适用模板与本轮工作证据，按“先看结论 → 成员/工作线进展 → 顶层讨论问题 → 下个检查点 → 会中记录”生成或刷新本场 Draft，保留成员编辑、图片和既有记录，并返回实际文档链接。

> 使用 $intgral-meeting-prepare 准备下一次团队会议：按最新模板核对上次会议后的进展，整理要讨论的问题和下个检查点；未确认的范围、负责人、日期和验收标待确认，写入本场 Draft 后给我链接。

私有配置可通过 `collaboration_policy.meeting_prepare.template_documents` 按 Team / Founders 登记实际模板；每次仍读取 live 正文与 revision。模板与草稿的内部链接、客户资料和访问权限留私有系统，公开包只包含通用骨架。此入口按需运行，不创建会前自动化或群发提醒。会后由 knowledge workflow 关联同场纪要。

## Knowledge workflow 与接入

新入口：`$intgral-knowledge-workflow`，每轮先检查 Wispr 连接器、账号与实际读取能力，再核对 Decision、处理新来源和所有待确认项，按权限更新文档与通知。连接失败保留 pending 与 checkpoint。阶段升级不扩大受众；私密内容向团队发布需要单独批准。完整流程见 [Mermaid 图](skills/intgral-knowledge-workflow/references/workflow.mmd)。

Slack 是成员的日常工作入口：召唤已接入的 agent 完成查询、讨论、小改动与确认，在原线程交付；需留存的决定更新已有记录，复杂研究/方案/长任务才在 docs 维护工作稿，指令与进度仍留 Slack。明确决定与写入授权可同条完成；实际召唤入口须单独绑定与验收，插件安装不等于已部署监听。交互、权限、回执与恢复见 [Slack 操作规范](skills/intgral-knowledge-workflow/references/slack-interface.md)。纯 Slack/docs 请求只检查所需能力，引用 Wispr 时再核验 Wispr。

普通 skill 安装：使用 skill-installer 从本仓库已合并的 main 安装 `skills/intgral-knowledge-workflow`；会前准备同时安装 `skills/intgral-meeting-prepare`，需要原提示词兼容时同时安装 `skills/intgral-meeting`。插件包包含这三个入口，并声明官方 Wispr Flow 与 Slack 为必需 app；成员仍须使用自己的账号授权。插件名为 intgral-knowledge-workflow，既有插件安装不等于新版已安装。

调用示例：

> 使用 $intgral-knowledge-workflow 执行一轮同步：先检查 Wispr 连接与读取能力，再读取 Decision 回复、归档会议与 thoughts，更新同权限主题，把全部待确认项提交到配置的决策队列；仅在明确批准范围写回并推送重大更新。

私有配置需提供 docs 目标与权限、来源范围/时区、独立私密 Decision 频道与完整成员白名单、公司/团队通知目的地、实际批准权限、隔离运行身份、私有状态/outbox 路径。一个问题一条稳定线程，无变化不重复提醒。会议按[来源分类与常设授权](skills/intgral-knowledge-workflow/references/meeting-routing.md)分流：Team 纪要进配置的全员 Meeting，Founders 会议进私有集合，个人 thoughts 仅 owner 可见；未分类先私有暂存。独立 Team 运行器只读获准投影，不能读取私密频道。没有有效 Decision 读取仍可保存私有草稿，但依赖确认的承诺和跨受众发布保持 pending。

运行模式包括 dry-run、apply、verify、reconcile 与 publish-approved。这些是 skill 的工作模式，平台写入通过获授权的真实工具完成；[ledger helper](skills/intgral-knowledge-workflow/references/state.md) 只提供本机去重、修订与回执，不是已部署的同步服务。运行前核对实际平台能力与权限，不能凭本地 ledger 宣称远端已写入或隔离成功。

文档与消息需要实际读回验证。已有待发送记录结果不明时先核对远端，再续办；跨机器仍需共享去重与协调。真实白名单、内部地址、会议内容、账号信息和私有队列不进入本仓库。升级先保留旧 state 与 checkpoint，验证迁移后再切换已安装副本；正式安装使用合并后的 main，未合并分支只供评审。

## 使用

将整个目录安装或复制到模型客户端支持的 skills 目录，保留 `SKILL.md`、`references/` 和 `assets/` 的相对结构；也可以把 [SKILL.md](SKILL.md) 和所需的引用文件一起交给模型。

例如：

> 使用 intgral-guide-skill：我收到一项客户反馈，需要判断下一步应该补什么信息、与哪些角色协作，以及产物放在哪里。

需要实际团队信息时，按 [配置示例](assets/team-context.example.json) 在**仓库外的私有位置**建立配置，并让当前模型读取该文件；项目也可在 `AGENTS.md` 声明配置位置。支持本地文件的环境可设置 `INTGRAL_TEAM_CONFIG` 指向它，已有 `INTGRAL_TEAM_CONTEXT` 入口继续兼容；没有配置或工具权限时，模型仍能给出角色级指导，并说明关键缺口。配置中使用现有系统的访问控制，不存放访问令牌。

提供 `workspace_root` 后，模型先读取该根目录下的 `AGENTS.md`，再由 skill 按项目配置中的 `local_indexes` 加载任务相关资料，并到源站核实实时状态。相对的 `workspace_root` 从配置文件所在目录解析，索引路径从工作区根目录解析。实际根路径和索引内容留在私有工作区；资料索引与具体代码仓库的知识图分别维护。

团队目标、成员分工、会议安排和任务状态在私有来源中维护。只有查找资料、协作或记录流程改变时，才需要更新本 skill。

研究或会后继续讨论时，可以明确约定：

> 使用 $intgral-guide-skill。在这次 Intgral 讨论中，有依据的新发现先记为探索，写入已配置的 docs 研究主题；只有我在职责范围内明确确认后才记为决定。按私有配置将增量交给每日总结并同步团队更新频道。保存失败时保留待同步记录，告诉我实际完成到哪里。

也可以随时说“记一下这个方向”“先验证这个假设”或“确认在这个范围采用”。每位成员使用自己的授权账号；每日自动化补办的是共同入口和本机可访问的待同步记录，并不自动读取所有人的本地对话。

## 工作流程

1. 明确这次要达成的结果和当前卡点。
2. 读取项目 `AGENTS.md` 和获授权的私有配置，通过 `local_indexes` 只定位本次所需来源。
3. 回到来源核实适用版本与当前状态，连接目标、任务、角色、依赖和产物。
4. 给出下一步行动：谁参与、需要什么输入、产物放哪、怎样算完成；按请求和既有授权执行。
5. 将已确认的结果链接回相关文档和任务，交接待核验事项。

## 平台分工

| 平台 | 负责什么 |
|---|---|
| Figma | 设计系统、UI/UX、组件与交互，实施和评审对齐适用版本 |
| [docs.intgral.ai](https://docs.intgral.ai) | 商务、研究、会议、团队流程等文档 |
| Drive | 需要在 Drive 保存的文件和附件，由相关文档链接过去 |
| Slack | 讨论、协调、决策来源和交接 |
| Linear | 正式任务、负责人、依赖和计划状态 |
| GitHub | 代码、PR、测试、实现与发布证据 |

工作方法与平台关系见 [gear map](references/gear-map.md)，工作场景分支见 [workflows](references/workflows.md)。Skill 的指导本身不扩大成员或模型的操作权限。

## 贡献与检查

公开 issue 和 PR 使用虚构示例与通用角色。内部资料、链接、设计截图、客户记录和私有配置留在私有系统中。提交前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

仅需 Python 3.11 或更高版本，无第三方运行依赖：

```sh
python3 scripts/validate.py --history
python3 -m unittest discover -s tests -v
```

检查涵盖包结构、相对链接、配置示例、当前文件及 Git 历史中的常见敏感信息模式。还需要人工确认内容适合公开；自动检查不等于完整的安全审计。

采用 [MIT License](LICENSE)。
