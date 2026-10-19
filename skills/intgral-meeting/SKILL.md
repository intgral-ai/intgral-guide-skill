---
name: intgral-meeting
description: Compatibility entry for the Intgral meeting workflow, now part of intgral-knowledge-workflow. Use existing meeting prompts to enter the complete source, Decision, document and update loop.
---

# Intgral Meeting — compatibility entry

完整流程已升级为 [intgral-knowledge-workflow](../intgral-knowledge-workflow/SKILL.md)。

“会前准备 / 刷新 meeting Draft”使用 [intgral-meeting-prepare](../intgral-meeting-prepare/SKILL.md)；会后归档与同步继续走下方流程。单独安装兼容入口时，按本次请求安装相应 skill。

先检查新 workflow skill 是否已安装/随包可读；可用时按其完整流程执行：先通过 Wispr 连接器、账号与实际读取的前置检查，每轮核对独立私密 Decision，再按登记受众分流：Team 纪要进全员 Meeting，Founders 会议进私有 Meeting，个人 thoughts 仅 owner 可见，未分类保持私有待确认。常设授权内的 Team 纪要可自动同步；写回和通知仍核对各自授权。保留用户原先指定的范围。

如果只安装了这个兼容入口而无法读取新 skill，说明缺少依赖并提供仓库中 skills/intgral-knowledge-workflow 的安装位置；可以读取已授权来源、准备私有草稿与待处理记录，但不要声称已过 Decision、已写回或已经部署。插件包同时提供会前准备、完整流程和兼容入口；独立使用归档兼容入口须同时安装 knowledge workflow。
