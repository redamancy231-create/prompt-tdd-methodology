# Prompt-TDD · Prompt 對照實驗方法論案例手冊

> **English**: A methodology casebook for controlled prompt engineering experiments. Two real experiments with complete data, both yielding negative results honestly reported. Includes experiment design SOP, analysis toolkit, and lessons from 17+ rounds of multi-model review. **CC BY 4.0**.

**語言**：簡體中文（原文）  
**定位**：方法論案例手冊 (methodology casebook) — **v0.1-methodology**  
**來源**：提煉自 prompt-tdd 專案（2026-06-17 ~ 2026-06-22）

> **這**不是 pip install 的工具庫。這是一本**如何做 prompt 對照實驗**的操作手冊，附帶兩個真實案例的完整資料、程式碼和失敗分析。

---

## 核心理念

Amanda Askell（Anthropic）："一個好的 system prompt 背後，那個無聊但關鍵的秘密是測試驅動開發。"

```
不是:  写 prompt → 发现失败 → 加规则 → 规则打架 → 再加...
而是:  写测试 → 找能通过的 prompt → 发现新失败 → 加入测试集 → 重复
```

---

## 這本手冊解決什麼問題

| 問題 | 本手冊的答案 |
|------|------------|
| 怎麼知道改 prompt 真的變好了？ | 對照實驗 + 預註冊 + 工程門/科學門拆分 |
| 怎麼避免"感覺更好了"的錯覺？ | 雙 LLM 異後端盲評 + 效應量閾值 |
| 怎麼防止事後調整假設？ | 預註冊鎖 (.lock) + train/test 分離 |
| 陰性結果怎麼辦？ | **公開發布**——A2 和 A3 都是陰性 |
| 天花板效應怎麼處理？ | 實驗前做 ceiling probe（反編造測試用例） |

---

## 實驗管線

```mermaid
flowchart LR
    subgraph PREP["准备阶段"]
        D1["实验设计<br/>CK1-CK6"] --> D2["测试用例<br/>train/test"] --> D3["预注册<br/>.lock 冻结"]
    end
    subgraph EXEC["执行阶段"]
        C1["Tier 0<br/>小样本验证"] -->|工程门 PASS| C2["Tier 1<br/>推断统计"]
    end
    PREP --> EXEC --> REVIEW["审查闭合"] --> GRADE["成熟度标注<br/>[Sp]→[E]→[F]"]
```

### 兩個真實案例

| | A2: prep/exec/post 分段 | A3: 宣告式 vs NL 路由 |
|------|------|------|
| **角色** | **主案例**——完整管線 | **反例**——如何閉合無訊號實驗 |
| 任務域 | 程式碼審查 | Agent 路由決策 |
| 樣本量 | n=24/臂 + Qwen 復現 | Pilot: 15 cases |
| 結論 | 陰性 [E-] | 陰性 [E-] |
| 審查 | 6+ 輪 / 3 後端 | 10 輪 / 2 後端 |
| 資料 | [→ A2](examples/a2-prep-exec-post/) | [→ A3](examples/a3-action-routing/) |

---

## 快速開始

```bash
pip install -r requirements.txt
python analyze_experiment.py examples/minimal/scoresheet.csv --tier 0
```

跑通後讀 [SOP](sop.md) + [檢查清單](methodology/checklists.md)。

---

## 目錄結構

```
prompt-tdd-methodology/
├── README.md              ← 你在这里
├── sop.md                 ← 对照实验设计 SOP（CK1-CK6 + Tier 0→1）
├── analyze_experiment.py  ← 分析脚本（CSV→统计→报告）
├── schema/                ← 数据契约
├── examples/
│   ├── minimal/           ←   4-case 玩具（30秒跑通）
│   ├── a2-prep-exec-post/ ←   主案例
│   └── a3-action-routing/ ←   反例案例
├── methodology/
│   ├── lessons-learned.md ←   核心教训（~5KB）
│   ├── glossary.md        ←   术语表
│   └── checklists.md      ←   启动前检查表
└── appendix/
    └── a1-summary.md      ←   A1 为什么没纳入
```

---

## 實證基礎

| 指標 | 資料 |
|------|------|
| 完成實驗 | A2 + A3 |
| 跨模型復現 | A2: GPT-5.5→Qwen3.7-Max（Δ=−0.014 方向一致） |
| 審查輪次 | 17+（Codex + Qwen + Kimi + ZCode） |
| 方法論產出 | 21 個方法論片段 |

---

## 相關專案

| 專案 | 關係 |
|------|------|
| [**AI協作專案全生命週期框架**](https://github.com/redamancy231-create/ai-collaboration-framework) | **上游整合層**——A2/A3 實驗結論已寫回 §4.1.1 + §6.3.1-6.3.2；框架 CK1-CK6 檢查清單提煉自本手冊 |
| [**Independent Review Toolkit**](https://github.com/redamancy231-create/independent-review-toolkit) | **同級工具**——本手冊的兩個案例實驗均使用獨立審查 SOP 完成 17+ 輪異後端審查閉合 |

---

## 許可與引用

CC BY 4.0。v0.1-methodology。

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-01*
