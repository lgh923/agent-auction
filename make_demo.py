#!/usr/bin/env python3
"""Agent Auction demo: 真实浏览器里的"Agent服务市场"页 — 竞价榜+获胜高亮+点击"运行竞价"->结算."""
import json, os
d = json.load(open("output/result.json"))
task=d["task"]; bids=d["bids"]; settle=d["settle"]
def pctq(q): return f"{q}"

rows=[]
medals=["🥇","🥈","🥉","","",""]
for i,b in enumerate(bids):
    winner="win" if b["name"]==d["winner"] else ""
    rows.append(f'''<tr class="row {winner}" data-i="{i}" style="animation-delay:{i*0.09}s">
<td class="rank">{medals[i]}<b>{i+1}</b></td><td class="nm">{b["name"]}{' <span class=tag>WIN</span>' if winner else ''}</td>
<td>${b["price"]:.2f}</td><td>{pctq(b["quality"])}</td><td>{b["speed"]}</td><td>{b["reliability"]}%</td>
<td><span class="sc">{b["score"]}</span></td></tr>''')
rows="".join(rows)

TEMPLATE="""<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:Inter,-apple-system,'PingFang SC',sans-serif}
body{background:#f4f5fb;color:#14162b}
.top{background:#14162b;color:#fff;padding:0 32px;height:56px;display:flex;align-items:center;gap:24px}
.tlogo{font-weight:800;font-size:17px;display:flex;align-items:center;gap:9px}
.tlogo .cube{width:20px;height:20px;border-radius:6px;background:linear-gradient(135deg,#7c5cff,#b388ff);display:inline-block}
.top nav{display:flex;gap:18px;font-size:13px;color:#a0a3c0}.top nav b{color:#fff;border-bottom:2px solid #7c5cff;padding-bottom:4px}
.top .bal{margin-left:auto;background:#262a4a;border:1px solid #373b63;border-radius:10px;padding:7px 14px;font-size:12px;color:#cdd0ec}
.top .bal b{color:#fff}
.wrap{max-width:1020px;margin:0 auto;padding:30px 24px}
.task{background:linear-gradient(120deg,#1a1d3a,#2b2f5e);color:#fff;border-radius:18px;padding:22px 26px;display:flex;justify-content:space-between;align-items:center}
.task .tl{font-size:12px;color:#9aa0cf;letter-spacing:.5px}
.task .tt{font-size:21px;font-weight:800;margin:6px 0}
.task .meta{display:flex;gap:22px;margin-top:8px;font-size:13px;color:#c3c7ee}
.task .meta b{color:#fff;font-size:15px}
.task .run{background:#7c5cff;border:none;color:#fff;font-weight:800;font-size:15px;padding:14px 24px;border-radius:12px;cursor:pointer;box-shadow:0 8px 22px rgba(124,92,255,.35)}
.task .run:active{transform:scale(.97)}
.panel{background:#fff;border-radius:16px;margin-top:18px;box-shadow:0 4px 20px rgba(40,40,80,.06);overflow:hidden}
.phead{display:grid;grid-template-columns:.8fr 1.7fr .9fr .7fr .7fr .9fr 1fr;padding:12px 22px;font-size:12px;color:#8a8db0;font-weight:600;background:#fafbff;border-bottom:1px solid #eceef8}
table{width:100%;border-collapse:collapse}
td{padding:12px 22px;font-size:13.5px;border-bottom:1px solid #f1f2fb;text-align:left}
tr.row{opacity:0;animation:in .5s forwards;cursor:pointer}
tr.row:hover{background:#f9f9ff}
tr.win{background:#f2efff;border-left:3px solid #7c5cff}
tr.win td{font-weight:700}
td.rank{color:#8a8db0;font-weight:700}.tag{background:#7c5cff;color:#fff;font-size:10px;padding:2px 7px;border-radius:8px;margin-left:7px}
td.nm{font-weight:700}.sc{font-weight:800;font-size:15px;color:#5b3df5}
.settle{display:none;background:#f2efff;border-top:2px solid #7c5cff;padding:18px 24px;font-size:13px}
.settle .h{font-weight:800;color:#4a2fd1;margin-bottom:8px}
.settle .ln{display:flex;gap:26px;color:#4a4f74}.settle .ln b{color:#14162b;font-size:16px}
.pick{display:none;background:#f8f8ff;border:1px solid #ece8ff;border-radius:12px;margin:0 22px 16px;padding:14px 18px;font-size:13px}
.pick .h{font-weight:800;color:#14162b;margin-bottom:6px}
.pick .row2{display:flex;gap:20px;color:#4a4f74}.pick .row2 b{color:#14162b}
@keyframes in{to{opacity:1}}
</style></head><body>
<div class="top"><div class="tlogo"><span class="cube"></span>Agent Auction</div>
<nav><b>市场</b><span>任务</span><span>结算</span><span>历史</span></nav><div class="bal">余额 <b>$1,240.00</b></div></div>
<div class="wrap">
 <div class="task">
  <div><div class="tl">任务 #{task["id"]}</div><div class="tt">{task["title"]}</div>
  <div class="meta"><span>预算 <b>${task["budget_usd"]:.2f}</b></span><span>时限 <b>{task["deadline_min"]} min</b></span><span>竞标 <b>{len(bids)}</b></span></div></div>
  <button class="run" id="run">▶ 运行竞价</button>
 </div>
 <div class="panel">
  <div class="phead"><span>#</span><span>Agent</span><span>报价</span><span>质量</span><span>速度</span><span>可靠度</span><span>综合分</span></div>
  <table>@@ROWS@@</table>
  <div class="pick" id="pick"><div class="h" id="pickh"></div><div class="row2" id="pickr"></div></div>
  <div class="settle" id="settle"><div class="h">⚡ 结算 · x402 微支付</div>
  <div class="ln"><span>赢家 <b>@@WINNER@@</b></span><span>毛额 <b>$@@GROSS@@</b></span><span>服务费 <b>-$@@FEE@@</b></span><span>实付 <b>$@@PAYOUT@@</b></span></div></div>
 </div>
 <p style="color:#9aa0c0;font-size:11px;margin-top:14px">Agent 竞价匹配引擎 (质量×速度×可靠)/性价比 · 只读演示 · 非真实交易</p>
</div>
<script>
var run=document.getElementById('run'),started=false;
run.onclick=function(){if(started)return;started=true;
 document.getElementById('settle').style.display='block';run.textContent='竞价完成 ✓';run.style.background='#16a06a';};
// 点竞价行 -> 高亮 + 显示该Agent投标详情
var info=@@INFO@@;
document.querySelectorAll('tr.row').forEach(function(tr){
 tr.onclick=function(){var b=info[tr.getAttribute('data-i')];
  document.querySelectorAll('tr.row').forEach(function(x){x.classList.remove('win');});
  tr.classList.add('win');
  document.getElementById('pickh').textContent='◂ 候选 Agent · '+b.nm;
  document.getElementById('pickr').innerHTML='<span>报价 <b>$'+b.pr.toFixed(2)+'</b></span><span>质量 <b>'+b.q+'</b></span><span>速度 <b>'+b.sp+'</b></span><span>可靠 <b>'+b.r+'%</b></span><span>综合分 <b>'+b.sc+'</b></span>';
  document.getElementById('pick').style.display='block';};
});
</script>
</body></html>"""

def _rep(s):
    s=s.replace("@@ROWS@@",rows).replace("@@WINNER@@",d["winner"])
    s=s.replace("@@GROSS@@",f"{settle['gross']:.2f}").replace("@@FEE@@",f"{settle['fee']:.2f}").replace("@@PAYOUT@@",f"{settle['payout']:.2f}")
    # 任务卡片字段
    s=s.replace('{task["id"]}',task["id"]).replace('{task["title"]}',task["title"])
    s=s.replace('${task["budget_usd"]:.2f}',f"${task['budget_usd']:.2f}")
    s=s.replace('{task["deadline_min"]} min',f"{task['deadline_min']} min")
    s=s.replace('{len(bids)}',str(len(bids)))
    return s
infojs=json.dumps([{"nm":b["name"],"pr":b["price"],"q":b["quality"],"sp":b["speed"],"r":b["reliability"],"sc":b["score"]} for b in bids],ensure_ascii=False)
html=_rep(TEMPLATE).replace("@@INFO@@",infojs)
os.makedirs("output",exist_ok=True)
open("output/demo.html","w").write(html)
print("demo.html 已生成 (Agent Auction 市场页, 靛紫)")
