# 本机 ledger 与恢复

ledger.py 只管理本机 JSON：稳定问题 ID、修订、明确答案和逐目标回执。它不访问 Slack/docs、不证明权限，也不自动识别自然语言批准。先通过真实平台工具核实人、来源、范围、受众与远端结果，再把结构化证据交给脚本。

配置和 state 均保存在包/仓库外的私有目录；按 audience/执行身份分开，单写入者运行。脚本用独占锁和原子替换防止本机并发覆盖；已有锁不自动删除，先核实原进程和上次远端结果。它不提供跨机器锁或消息 exactly-once。

命令输入 JSON 从 stdin 读取，避免把内容放命令行：

```sh
python3 scripts/ledger.py --state /private/workflow/state.json register < issue.json
python3 scripts/ledger.py --state /private/workflow/state.json resolve < reply.json
python3 scripts/ledger.py --state /private/workflow/state.json prepare < delivery.json
python3 scripts/ledger.py --state /private/workflow/state.json verify < receipt.json
python3 scripts/ledger.py --state /private/workflow/state.json show
```

register 输入：key、question、audience、source_revision。相同 key/内容不新建；来源/问题或 audience 变化递增 revision、清空当前答案并保留历史。

resolve 输入：id、revision、actor、authorized_actors、action（approve/reject/defer）、evidence。authorized_actors 由调用方已核实的项目确认权限提供，不能从 Slack 回复者自行声明中读取；defer 保持 pending。解析或复读不足就不要调用 resolve。

prepare 输入：target、revision、hash。首次返回 write 并先保存 pending；相同 pending 再运行返回 reconcile。不同内容也不能覆盖未核实的旧尝试。verified 且同修订/hash 返回 skip。平台创建前后均需远端查重。

verify 输入：target、revision、hash、url、observed=true。只有实际读回一致后才能提交，版本/hash 不匹配会拒绝；更高修订不能凭低修订成功自动验证。docs、Decision thread、Slack 和任务分别使用不同 target key。

每轮的 Decision 读取、成员/权限检查、跨受众批准和 payload hash 校验由 workflow 在真正写入前完成。ledger 中的 approved 仅说明该问题已确认，不能作为向 Team 发布的批准。
