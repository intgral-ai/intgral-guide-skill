---
name: intgral-meeting
description: Compatibility entry for the Intgral meeting workflow, now part of intgral-knowledge-workflow. Use existing meeting prompts to enter the complete source, Decision, document and update loop.
---

# Intgral Meeting — compatibility entry

完整流程已升级为 [intgral-knowledge-workflow](../intgral-knowledge-workflow/SKILL.md)。

先检查新 workflow skill 是否已安装/随包可读；可用时按其完整流程执行：先通过 Wispr 连接器、账号与实际读取的前置检查，每轮核对独立私密 Decision，再归档来源、提交全部待确认项、按权限写回和通知。保留用户原先指定的范围与授权。

如果只安装了这个兼容入口而无法读取新 skill，说明缺少依赖并提供仓库中 skills/intgral-knowledge-workflow 的安装位置；可以读取已授权来源、准备私有草稿与待处理记录，但不要声称已过 Decision、已写回或已经部署。插件包同时包含两个入口；独立安装须同时安装两者。
