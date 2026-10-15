# Intgral Management Skill

供员工交给语言模型使用的团队协作指南。描述要推进的工作，模型会帮助定位目标、责任角色、依赖、资料、下一步行动与完成标准。

本公开仓库保存可复用的方法、通用角色和空配置示例。实际成员、项目目标、内部来源与审批规则在团队私有系统中维护。

## 使用

将整个目录安装或复制到模型客户端支持的 skills 目录，保留 `SKILL.md`、`references/` 和 `assets/` 的相对结构；也可以把 [SKILL.md](SKILL.md) 和所需的引用文件一起交给模型。

例如：

> 使用 intgral-management-skill：我收到一项客户反馈，需要判断下一步应该补什么信息、与哪些角色协作，以及产物放在哪里。

需要实际团队信息时，按 [配置示例](assets/team-context.example.json) 在**仓库外的私有位置**建立配置，并让当前模型读取该文件；项目也可以在 `AGENTS.md` 声明配置位置。支持本地文件的环境可设置 `INTGRAL_TEAM_CONFIG` 指向它，已有的 `INTGRAL_TEAM_CONTEXT` 入口继续兼容。没有配置或工具权限时，模型仍能给出角色级指导，并说明关键缺口。配置中使用现有系统的访问控制，不存放访问令牌。

模型先读取工作区根目录的 `AGENTS.md`，再通过私有配置的 `local_indexes` 按需读取文档、设计、沟通、研究、代码或环境入口，并到源站核实实时状态。相对 `workspace_root` 从配置文件所在目录解析，`local_indexes` 的相对路径从工作区根目录解析。实际路径和索引内容留在私有工作区；资料索引与具体代码仓库的知识图分别维护。

## 平台分工

| 平台 | 负责什么 |
|---|---|
| Figma | 设计系统、UI/UX、组件与交互，实施和评审对齐适用版本 |
| [docs.intgral.ai](https://docs.intgral.ai) | 商务、研究、会议、团队流程等文档 |
| Drive | 需要在 Drive 保存的文件和附件，由相关文档链接过去 |
| Slack | 讨论、协调、决策来源和交接 |
| Linear | 正式任务、负责人、依赖和计划状态 |
| GitHub | 代码、PR、测试、实现与发布证据 |

工作方法与平台关系见 [gear map](references/gear-map.md)，管理场景分支见 [workflows](references/workflows.md)。Skill 的指导本身不扩大员工或模型的操作权限。

## 贡献与检查

公开 issue 和 PR 使用虚构示例与通用角色。内部资料、链接、设计截图、客户记录和私有配置留在私有系统中。提交前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

仅需 Python 3.11 或更高版本，无第三方运行依赖：

```sh
python3 scripts/validate.py --history
python3 -m unittest discover -s tests -v
```

检查涵盖包结构、相对链接、配置示例、当前文件及 Git 历史中的常见敏感信息模式。还需要人工确认内容适合公开；自动检查不等于完整的安全审计。

采用 [MIT License](LICENSE)。
