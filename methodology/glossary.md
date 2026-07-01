# 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| **Tier 0** | Tier 0 | 小样本描述性统计阶段——验证工具链可行，不升级成熟度 |
| **Tier 1** | Tier 1 | 大样本推断统计阶段——假设检验 + 成熟度升级 |
| **工程门** | Engineering Gate | 判工具链可用：数据收集/评分脚本/manifest 完整性 |
| **科学门** | Science Gate | 判假设被支持：统计显著 + 效应量 ≥ 阈值 + 方向一致（三项全 PASS） |
| **预注册锁** | Pre-registration Lock | .lock 文件——冻结假设/分析计划/停止规则，git commit 后不可修改 |
| **INVENTORY 等价** | INVENTORY Equivalence | 逐项核对两组 prompt 产出清单 + hash 冻结，防 IV 污染 |
| **CK1-CK6** | Checklist 1-6 | 实验前检查清单：CK1-CK3 Tier 1 硬门，CK4-CK6 条件触发 |
| **[Sp]** | Specification | 成熟度——设计草案（初始状态） |
| **[E]** | Experiment | 成熟度——Tier 1 + 科学门 PASS + 审查闭合 |
| **[E-]** | Experiment (ceiling-limited) | 成熟度——Tier 1 完成 + 科学门 FAIL（阴性/天花板） |
| **[F·1域]** | Framework (single-domain) | 成熟度——写回框架，标注任务域限制 |
| **DV** | Dependent Variable | 因变量——实验测量的输出指标 |
| **IV** | Independent Variable | 自变量——实验操作的输入变量（如 prompt 格式） |
| **盲评** | Blind Scoring | 评分者不知道样本属于 A 组还是 B 组 |
| **双 LLM 异后端** | Dual-LLM Cross-Backend | 评分者 A（作者模型）+ 评分者 B（不同后端模型）独立评分 |
| **HARKing** | Hypothesizing After Results are Known | 看到结果后调整假设——预注册锁的对立面 |
| **Cohen's κ** | Cohen's Kappa | 评分者间一致性指标——用于检测 LLM-LLM 评分分歧 |
| **ceiling probe** | Ceiling Probe | 实验前探测天花板——嵌入反编造/极端测试用例评估检测空间 |
