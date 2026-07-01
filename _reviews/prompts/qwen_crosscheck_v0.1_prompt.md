你是独立审查者，对一个新发布的开源项目进行交叉审查。

## 审查对象

仓库：E:/workspace/projects/prompt-tdd-methodology/
版本：v0.1-methodology（首次发布，未经独立审查）
定位：Prompt 对照实验方法论案例手册——不是工具包，是"如何做 prompt 对照实验"的 SOP + 两个真实案例

文件清单：
- README.md / sop.md / analyze_experiment.py
- methodology/lessons-learned.md / glossary.md / checklists.md
- examples/a2-prep-exec-post/ (README + prompt_A/B + test_set.json + scoresheet.csv)
- examples/a3-action-routing/ (README only)
- examples/minimal/scoresheet.csv
- appendix/a1-summary.md
- schema/README.md

源材料对照（原始 prompt-tdd 项目）：
- E:/workspace/projects/prompt-tdd/README.md
- E:/workspace/projects/prompt-tdd/methodology_extraction/retrospect_a2_a3_combined.md（60KB 深度复盘）
- E:/workspace/projects/prompt-tdd/methodology_extraction/autopsy_a3.md（A3 尸检报告）
- E:/workspace/projects/prompt-tdd/tests/pocketflow_assets/a2_prep_exec_post/experiment_report_tier1.md（A2 Tier 1 报告）
- E:/workspace/projects/prompt-tdd/project_status.md

## 审查维度

### D1: SOP 方法论提取忠实度
- sop.md 是否准确提炼了源项目 A2+A3 的实验方法论？
- CK1-CK6 检查清单是否覆盖了源项目中实际使用的所有关键检查？
- 有没有遗漏源项目中重要的方法论元素？

### D2: 案例叙事准确性
- A2 案例 README 是否准确反映了原始 experiment_report_tier1.md 的数据和结论？
- A3 案例 README 的口径是否统一（"实验设计未能检验假设" vs "假设被证伪"）？
- A3 作为反例案例的叙事是否诚实地反映了 autopsy_a3.md 的结论？

### D3: 复盘精简忠实度
- methodology/lessons-learned.md（~5KB）是否准确提炼了 retrospect_a2_a3_combined.md（60KB）的核心内容？
- 三个跨实验模式（P1-P3）和六个缺失模式（PM1-PM6）的数据是否与源报告一致？
- 精简过程中是否有重要的 nuance 被丢失？

### D4: README 定位诚实度
- README 明确标注"v0.1-methodology"和"不是 pip install 的工具库"——这一定位是否诚实？
- "快速开始"是否真的可执行（pip install + python analyze_experiment.py + minimal CSV）？
- Mermaid 流程图是否准确反映了 SOP 的实验管线？

### D5: 整体判断
- 这个仓库的第一印象是什么？定位是否与内容匹配？
- 作为独立 GitHub 仓库，它是否有独立存在价值（vs 保持为框架附属资产）？
- 当前状态下是否可以推荐给他人使用？如果不行，缺什么？

## 输出格式

对每个维度：
1. 整体评价
2. 具体发现（标注严重度 + 文件名+段落）
3. 改进建议

最后给出总体终判（Keep / Minor / Major / Discard）和理由。

请先读取仓库全部文件，再对照源材料进行审查。独立审查者后端：请自报模型名称。
