---
name: intgral-knowledge-workflow
description: Run the evidence-to-decision workflow for Wispr meetings, early ideas and docs updates. Reconcile Decision on every cycle, preserve audience permissions, write verified records and notify material changes. Use for meeting synchronization, pending questions, confirmed decisions and explicitly approved publication.
---

# Intgral Knowledge Workflow

连接来源、主题、Decision、有效文档、进展通知与执行反馈。每轮经过 Decision；没有待确认事项时也记录已核对，不能跳过。阶段与权限分别维护，确认决定不自动批准扩大受众。

## 接入

读取当前项目 AGENTS.md 和获授权的私有团队配置（项目指定路径，或 INTGRAL_TEAM_CONFIG，兼容 INTGRAL_TEAM_CONTEXT）。相对 workspace_root 从配置目录解析，local_indexes 从工作区根目录解析。只定位本次来源。配置与索引不授予额外权限。

使用 Wispr、docs 和 Slack 的实际工具；账号授权、文档目标、Decision 目的地及成员、批准权限、运行身份、状态和 outbox 路径留私有配置。主流程见 [workflow.mmd](references/workflow.mmd)。工具不可用时保存私有待处理记录并说明缺口，不把尝试说成写入或上线。

## 每轮执行

1. **先核对 Decision。** 在授权范围内读取已登记线程的新回复、确认、更正、未结事项及新的人工作业提交，分页读全；Team 运行器只读取经过授权的 Team 投影，不读取私密 founders 频道。记录实际读取范围、截止时间和不可读项。Decision 暂不可用时仍可保存同权限来源草稿；会改变承诺或扩大受众的发布保持 pending。
2. **读取增量来源。** 包括 Wispr meetings、My thoughts、scratchpad，以及已登记 docs 的人工或自动修订；按 [wispr.md](references/wispr.md) 分别完整读取。先核对来源权限和归属，再归档；未知或冲突保持个人私有。
3. **归档并更新主题。** 会议按场，想法按稳定主题；保留来源、人工内容和有效决定。来源修订只更新来源区、产生差异与待复核，不用自动 summary 覆盖人工确认。具体写回与失败续办见 [archive.md](references/archive.md)。
4. **提交全部待确认项。** 范围、取舍、负责人、日期、验收、证据、权限、发布批准及运行缺口都进入持久 Decision 记录；一个稳定问题一条线程，重跑更新原记录。有权限才向配置的 Decision 目的地提交最小必要内容；个人/未知权限内容留 owner 私有队列，必要时仅提交不含原文的分类请求。不得丢弃未发成功的问题。见 [decision.md](references/decision.md)。
5. **处理明确结论。** 核验确认者的实际批准范围、原话、问题修订、适用范围与来源；更新、拒绝、延期或补证据分别记录。无权确认、旧版本、含糊赞同、表情或沉默不解决问题。有关问题 pending 时继续独立且已授权的工作，不自行填上人名、预算或期限。
6. **写回并验证。** 在原权限范围更新来源、主题、提案和有效决定。产品/MVP/engineering 仅在已授权范围更新，参见 [topdown.md](references/topdown.md)。明确执行承诺还须满足项目 work_tracking 的门槛才修改正式任务。
7. **重大更新通知。** docs 写入并重新加载复核后，按受众通知；人工编辑也检查实质差异。普通改字无通知，已发即时更新在日报中链接而不重发。发前核对目标当前成员/权限，结果不明先查远端。见 [publication.md](references/publication.md)。
8. **保存回执与反馈。** 源、docs、Decision、通知和任务分别维护 verified revision；失败独立保留 pending。实际结果成为下轮证据或新问题，自动摘要和回声不算新确认。

## 阶段与权限

来源 → exploring → validating/提案 → decided → 执行关联 → 被替代。正式任务状态留在任务系统。

personal / founders / team 是独立可见性。衍生记录继承最严格来源权限；成员或阶段变化不自动扩大访问。私有 Decision 中的回复也不会因问题起源于 Team 而自动向员工公开。详见 [permissions.md](references/permissions.md)。

## 可重复运行

支持 dry-run（拟改与通知预览）、apply（已授权最小写入）、verify（读回复核）、reconcile（只补未验证目标）、publish-approved（精确获批版本）。

[ledger.py](scripts/ledger.py) 提供本机问题去重、修订确认和逐目标回执，不执行平台写入，也不能代替实际权限核验。命令和恢复约束见 [state.md](references/state.md)。分权限使用独立私有 ledger；未迁移验证前保留旧 state，不重置来源 checkpoint。多个运行器的本机 ledger 不提供分布式 exactly-once 保证。

交付报告列出实际来源覆盖、文档/线程/消息链接、待确认问题与失败阶段。区分 PR、合并、安装、授权和运行成功。权限漂移或同一操作重试一次仍失败时停止该目标，保留证据待续办。
