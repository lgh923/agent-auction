# Agent Auction

一个跑在 Binance Agent OS 上的**只读 Agent 市场**：把"让哪个 Agent 干这个活"变成一个**竞价+结算**的流程——多家 Agent 竞价同一任务，一个匹配引擎打分选赢家，再用 **x402 类微支付**结清报酬。

## 它解决什么
AI Agent 越来越多，但你**该信任谁、该付多少**？Agent Auction 把这件"选人+付钱"的事透明化：**按 性价比 打分选赢家 + 让赢家拿到报酬**。只演示匹配与结算逻辑，不下真实单。

## 竞价怎么打
```
综合分 = (质量/100 × 速度/10 × 可靠度/100) / (报价/预算)  ×10
```
- 报价越便宜、质量越高、速度越快、越可靠 → 分越高
- 所有 Agent 按分排名，**第一名胜出**
- 结算：毛额 - 服务费(2%) = **实付**，走 **x402 micro-payment**

## 怎么用
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # 核心仅标准库
python3 agent.py                       # -> output/report.md + output/result.json
python3 make_demo.py                   # 生成市场页 HTML
python3 make_video.py                  # 真实 Chrome 桌面录屏
```

## 采样结果
```
任务 #T-2026-0918 · 抓取币安Agent OS动态并生成简报 (预算 $25 / 时限30min / 竞标6)
🏆 赢家 RayAgent  综合分 34.8 (报价$5 · 质量78 · 速度9.6 · 可靠93%)
⚡ 结算(x402): 毛额 $5.00 - 服务费 $0.10 = 实付 $4.90
```

> 竞价模型为演示逻辑；真实结算需走 Agent OS 的支付原语。仅供研究，非投资建议。
