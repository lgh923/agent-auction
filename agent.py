#!/usr/bin/env python3
"""Agent Auction: 一个"Agent服务市场"——多个Agent竞价同一任务, 匹配引擎按 价格×质量×速度 打分选赢家, 再走x402类微支付结算. 只读模型, 无真实下单."""
import json, datetime, os

# 任务描述
TASK = dict(id="T-2026-0918", title="抓取币安Agent OS最新动态并生成简报",
            budget_usd=25.0, deadline_min=30)

# 候选 Agent (能力: 单价, 质量分, 速度, 可靠度)
AGENTS = [
    dict(name="Sentinel-X",        price=8.0,  quality=92, speed=8.5, reliability=99),
    dict(name="DataPilot",         price=6.0,  quality=85, speed=9.2, reliability=97),
    dict(name="CircuitBreaker",    price=9.5,  quality=96, speed=7.0, reliability=99),
    dict(name="RayAgent",          price=5.0,  quality=78, speed=9.6, reliability=93),
    dict(name="Owl-Finance",       price=7.0,  quality=88, speed=8.0, reliability=98),
    dict(name="MicroSettle",       price=4.5,  quality=74, speed=8.8, reliability=95),
]

def score(a):
    # 综合分: 质量 / (价格×时间)/可靠度 归一; 越高越好
    value = (a["quality"]/100) * (a["speed"]/10) * (a["reliability"]/100)
    cost = a["price"] / TASK["budget_usd"]          # 越低越便宜
    eff = value / max(cost, 0.05)                    # 性价比
    return round(eff*10, 1)

rows=[]
for a in AGENTS:
    s=score(a)
    rows.append(dict(name=a["name"], price=a["price"], quality=a["quality"],
                     speed=a["speed"], reliability=a["reliability"], score=s))
rows.sort(key=lambda x:-x["score"])
winner=rows[0]; runner=rows[1]
# x402 结算: 给赢家按报价付款 + 服务费
settle_fee = round(winner["price"]*0.02, 2)
payout = round(winner["price"] - settle_fee, 2)

result=dict(ts=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
            task=TASK, bids=rows, winner=winner["name"], runner=runner["name"],
            settle=dict(gross=winner["price"], fee=settle_fee, payout=payout,
                        currency="USD", protocol="x402-micro-payment"))
os.makedirs("output",exist_ok=True)
open("output/result.json","w").write(json.dumps(result,indent=2,ensure_ascii=False))

L=["# Agent Auction · 竞价与结算\n",
   f"**任务**: {TASK['title']}  (预算 ${TASK['budget_usd']:.2f} / 时限 {TASK['deadline_min']}min)\n",
   "## 竞价排名\n",
   "| Agent | 报价 | 质量 | 速度 | 可靠 | 综合分 |",
   "|---|---|---|---|---|---|"]
for r in rows:
    L.append(f"| {r['name']} | ${r['price']:.2f} | {r['quality']} | {r['speed']} | {r['reliability']}% | **{r['score']}** |")
L.append(f"\n## 结果\n- **赢家**: {winner['name']} (综合分 {winner['score']})")
L.append(f"- **结算(x402)**: 毛额 ${winner['price']:.2f} - 服务费 ${settle_fee:.2f} = **实付 ${payout:.2f}**")
L.append("\n> 竞价模型: 质量×速度×可靠 / 性价比; 仅演示匹配与结算逻辑, 非真实交易.")
open("output/report.md","w").write("\n".join(L))
print("winner:",winner["name"],"score",winner["score"],"| payout",payout,"| runner:",runner["name"])
