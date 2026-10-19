---
name: intgral-meeting-prepare
description: "Prepare an Intgral pre-meeting Draft from the latest authorized docs template and current work evidence. Use before a team or founders meeting to refresh progress, top-down discussion questions and the next checkpoint; meeting notes after the event use the knowledge workflow."
---

# Intgral Meeting Prepare

会前生成一份能直接开会使用的 Draft：先看方向与结果，再看成员和工作线进展，最后讨论问题、下个检查点与待确认项。采用最新授权模板的结构，事实每轮重新核验；会中决定留给实际会议确认。

## 定位本场和模板

读取项目 AGENTS.md、获授权私有配置及其 documentation / communication / work_tracking 索引。沿用 [intgral-knowledge-workflow](../intgral-knowledge-workflow/SKILL.md) 的 Decision、来源权限、写回与恢复规则；缺少依赖时可准备私有草稿，不能宣称已核验 Decision 或已发布。

从用户请求或已核验日历确定本场日期、主题、实际 occurrence、时区及 Team / Founders 受众。一次明确的近期会议可直接采用；多场候选或受众不明且影响落点时才询问，独立资料读取可继续。日期沿用本场时区，检查点保留原承诺的日期与时区。

优先读私有配置 `collaboration_policy.meeting_prepare.template_documents` 中对应受众的模板；没有登记时，按 docs 索引找到该类最新适用 Draft，核对集合、场次、更新时间和正文。已结束会议的 Draft 可提供排版结构，不能因最近被修改就成为本场目标。模板页若混有会后纪要，提取会前结构，保留模板与来源的 ID/revision 在私有运行记录中。内部正文、人员、客户、日期和链接不复制进共享 skill。

## 准备内容

1. **先核对 Decision。** 私有协调器按权限读取有关确认、更正和未结问题；受限 Team 身份仅读取获准的 Team 投影。Team Draft 只使用本来适合 Team 的证据及明确获准公开的结论，私密线程的原文、标题、链接和问题数量留在私有记录。缺少 Decision 覆盖时标缺口，保留有效决定，依赖新确认的内容继续待确认。
2. **核对当前证据。** 范围采用请求指定窗口，或上次同类会议至本次截止；周会可用本周，无法确定时说明采用的窗口。读取有关 Slack 讨论和线程回复、Linear 状态、GitHub PR/检查、docs 研究/商务记录及必要 Figma 产物。按当前获授权成员与工作线覆盖，未读到的标“待补更新”，不推断没有进展。引用 Wispr 时才执行连接器、账号和真实读取检查；逐字稿、会议摘要与个人 thoughts 按既有字段权限分别处理。
3. **按金字塔组织。** 用当前目标与实际结果开篇；每位有关成员/工作线用少量要点写进展、证据、阻塞和下一步，再列从客户价值、产品范围到交付依赖的讨论问题，最后说明下个检查点要看到什么。按最新模板调整顺序，详细证据用同受众链接承接；没有必要每次输出表格或长审计日志。
4. **保留状态差异。** 口头自述、已实现、PR 待合并、已合并、测试通过、演示成功、上线和客户验收分别标明。探索、AI 建议和候选截止日期保持提案；当前有权负责人原始明确确认才能形成承诺。来源冲突并列证据与日期，不能以新消息或自动摘要静默替代有效决定。
5. **提出可处理的问题。** 每个议题说明要解决的问题、证据/变化、建议或选项、会上需要谁确认及期望产物。下个检查点分开“既有承诺”和“建议确认”，负责人、期限、交付物、验收和依赖缺什么就标待确认。有关未决项复用稳定 Decision 记录及线程；权限不明或个人材料只留 owner-only 队列，分类请求不附私有内容。会前准备不直接创建或推进 Linear 任务。

采用 live 模板；模板暂不可读或没有可用模板时，用 [通用金字塔骨架](assets/meeting-draft.md) 先交私有草稿，明确最新模板未核验。既有图片、附件和成员补充保留；涉及图片证据须实际读取像素，无法读取则标覆盖缺口。装饰图不是必需输入。

## 写回与会后衔接

- 用户要求准备或刷新 Draft 时，在已授权且实时核验的目标写回；仅要求预览则交草稿。Team 进入全员 Meeting，Founders 进入私有 Meeting，个人 thoughts 保留 owner-only。实际目标和权限从私有路由核验，不因使用模板扩大受众。
- 按场次与受众查重：优先 calendar occurrence / 实际起止，尚无 ID 时私有登记主题、完整日期时间与受众组成的暂定身份。复用本场 `集合 / YYYY-MM-DD / 主题 Draft`；同题不同场次各自归档。远端查重后才创建，集合 ID 不当作父文档 ID。
- 私有配置提供 `collaboration_policy.meeting_prepare.state_path` 时，记录场次/受众、模板 revision、来源覆盖、上次生成片段及逐目标读回回执。重跑比较“上次生成 / 当前远端 / 本轮内容”，只更新本场会前准备区；成员改过的段落作为人工基线，保留会中记录、图片及已附会后纪要。没有生成基线时，先以当前远端为准做局部增补。
- 重新读取 revision 后做最小补丁；并发更改先重读合并，无法兼容的段落保留双方并标冲突。写入不明先查远端，一次重读后仍失败则保存 pending，返回已完成部分。
- 读回正文、来源链接、日期层级和权限后，返回 **Draft 标题、真实链接、主要变化、覆盖截止与仍待确认项**。仅在已获授权的对应 Slack 线程回告或通知，skill 本身不建立定时任务、发送会前群提醒或承诺已部署 Slack 触发器。
- 会中保留“确认决定 / 确认人”和“行动 / 负责人 / 日期 / 完成标准 / 缺什么”记录区。会后由 knowledge workflow 关联同一场次补纪要，保留会前基线与人工记录；准备 Draft 不标成会议已结束或问题已解决。
