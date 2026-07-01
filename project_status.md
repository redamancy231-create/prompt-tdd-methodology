## 项目状态: prompt-tdd-methodology

- 当前阶段: v0.1-methodology（已发布，经 Qwen R1 + Codex R2 审查闭合）
- 本轮完成:
  1. 从 prompt-tdd 项目提取对照实验方法论为独立案例手册
  2. Qwen3-Max R1(Major,2CRITICAL+3MAJOR)→修复→Codex R2(FAIL_WITH_CAVEATS→M2残留修正→闭合)
  3. 三语言翻译（en + zh-Hant，Codex GPT-5.5）
  4. Mermaid 实验管线图 + 交叉链接三个仓库
- 发现的问题:
  - C2(PM 编号与源报告完全不同)暴露了精简复盘的忠实度风险

## Next Steps

- 英文/正体中文 README 也加 Mermaid 图 → P2 → 无依赖
- 写介绍文章 → P2 → 无依赖
- 补全缺失的数据文件（A2 prompt文件已纳入，A3 scoresheet 保留在源仓库） → P2 → 无依赖

## 会话备注（2026-07-01，DeepSeek-V4-Pro via Claude Code CLI）

定位为"方法论案例手册 v0.1-methodology"——不是工具包，是 SOP + 两个真实案例（含阴性结果）。审查链：Qwen R1 + Codex R2，6 项发现闭合。analyze_experiment.py 的 minimal CSV rater 名已对齐脚本默认值。
