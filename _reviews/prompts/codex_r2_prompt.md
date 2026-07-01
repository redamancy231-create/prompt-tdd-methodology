你是独立审查者，对以下修复进行 R2 重审。

## R1 回顾

Qwen3-Max 审查 prompt-tdd-methodology v0.1-methodology。终判 Major。发现 5 项（CRITICAL×2, MAJOR×3）。

## R2 任务

验证以下 5 项是否已修复。每项只判：已修复/未修复/部分修复。给具体证据。

CRITICAL:
- C1: `python analyze_experiment.py examples/minimal/scoresheet.csv --tier 0` 是否不再崩溃？minimal CSV 的 rater 名是否匹配脚本默认值（rater_human/rater_codex）？
- C2: methodology/lessons-learned.md 的 PM-1~PM-6 是否与源报告 retrospect_a2_a3_combined.md §4.3 一致（不再是用错的编号定义）？

MAJOR:
- M1: A2 案例 README 结果数字是否标注了 test-set-only scope？
- M2: sop.md 科学门是否从"三项"改为"四项"（加了 κ）？是否新增了 A3v2 四门禁（§8.5）？
- M3: requirements.txt 是否只声明实际使用的依赖（scipy）？A3 README 是否不再声称有 scoresheet.csv？

## 输出

```
C1: [已修复/未修复] 证据: ...
C2: ...
M1: ...
M2: ...
M3: ...

R2 终判: [PASS / FAIL_WITH_CAVEATS / FAIL]
```

请先读取当前版本的以下文件：
- examples/minimal/scoresheet.csv
- methodology/lessons-learned.md
- examples/a2-prep-exec-post/README.md
- sop.md
- requirements.txt
- examples/a3-action-routing/README.md

独立审查者后端：请自报模型名称。
