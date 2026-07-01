# 启动前检查表 (Printable Pre-Flight Checklist)

> 打印或复制此清单。每次启动新实验前逐项确认。

---

## 实验前 (Pre-Experiment)

### 设计门

- [ ] CK1: H0/H1 已明确陈述，统计检验方法已指定
- [ ] CK2: DV 定义明确，评分 rubric 已冻结（git commit）
- [ ] CK3: 功效分析完成，min_n_per_arm ≥ 计算值

### 等价性门

- [ ] CK4: 双组 prompt 产出清单已逐项核对（INVENTORY 等价）
- [ ] CK4: inventory hash 已冻结

### 测试门

- [ ] CK5: test_set.json 已创建，train/test 分割明确
- [ ] CK5: test 集不会用于 prompt 选择或参数调整
- [ ] CK6: 如 DV 为 0/1 或比例 → 已嵌入天花板探测用例

### 预注册

- [ ] .lock 文件已创建（假设 + 分析计划 + 停止规则 + test_set_sha256）
- [ ] .lock 文件已 git commit（commit hash: ________）

---

## 实验中 (During Experiment)

### Tier 0

- [ ] 小样本（n=4-8/臂）收集完成，无异常
- [ ] 评分脚本运行正确，manifest 完整
- [ ] 描述性统计方向合理，效应量粗略估计
- [ ] **工程门判决**: PASS / FAIL → ________

### Tier 1（仅工程门 PASS 后执行）

- [ ] raw_outputs/ 只增不覆盖
- [ ] 双评分者 A（作者模型）执行完毕
- [ ] 双评分者 B（不同后端）在裸环境中执行完毕
- [ ] 评分前评分者不知分组
- [ ] analyze_experiment.py --tier 1 执行完毕

---

## 实验后 (Post-Experiment)

### 科学门

- [ ] 统计显著？ p < ________
- [ ] 效应量 ≥ 最小兴趣阈值？ Δ ≥ ________
- [ ] 方向一致？ 方向 = ________
- [ ] **科学门判决**: PASS / FAIL → ________

### 审查

- [ ] 异后端独立审查 ≥ 1 轮
- [ ] 审查者与实验执行者不同后端
- [ ] 审查者在裸环境中审阅
- [ ] 审查发现已修正或记录

### 闭合

- [ ] 成熟度已标注（[E] / [E-] / [F·1域]）
- [ ] 局限声明已写入报告
- [ ] 方法论片段已提取（如有）
- [ ] 阴性结果已诚实报告（如适用）

---

*检查清单来源：prompt-tdd A2+A3 实验的实战方法论*
