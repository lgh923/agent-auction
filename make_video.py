#!/usr/bin/env python3
"""Agent Auction: 真实桌面录屏 — 真实Chrome窗口(macOS菜单栏+标题栏+地址栏)被使用, 真实点击'运行竞价'->结算面板."""
import json, base64, time, urllib.request, websocket, subprocess, os

# CDP 连接
targets=json.load(urllib.request.urlopen("http://127.0.0.1:9222/json",timeout=5))
page=[t for t in targets if t.get("type")=="page"][0]
ws=websocket.create_connection(page["webSocketDebuggerUrl"],timeout=90,proxy_type="http",http_proxy_host="127.0.0.1",http_proxy_port=7890)
_id=[0]
def cmd(m,p=None,to=90):
    _id[0]+=1;mid=_id[0];ws.settimeout(to);ws.send(json.dumps({"id":mid,"method":m,"params":p or {}}))
    while True:
        x=json.loads(ws.recv())
        if x.get("id")==mid:return x.get("result",{})
def js(e,to=60):
    r=cmd("Runtime.evaluate",{"expression":e,"returnByValue":True},to);return r.get("result",{}).get("value")
cmd("Page.enable");cmd("Runtime.enable")

# 导航到 demo, 先滚动让页面完整渲染
cmd("Page.navigate",{"url":"http://127.0.0.1:8081/output/demo.html"});time.sleep(2.2)
cmd("Runtime.evaluate",{"expression":"window.scrollTo(0,120)"});time.sleep(0.6)
cmd("Runtime.evaluate",{"expression":"window.scrollTo(0,0)"});time.sleep(0.4)

# 激活 Chrome 到前台
subprocess.run(["osascript","-e",'tell application "Google Chrome" to activate'],capture_output=True)
time.sleep(1.0)

os.makedirs("/tmp/aa_frames",exist_ok=True)
[os.remove("/tmp/aa_frames/"+f) for f in os.listdir("/tmp/aa_frames")]
REG="22,47,1338,777"
def snap(n):
    subprocess.run(["screencapture","-x","-R",REG,f"/tmp/aa_frames/f{n:03d}.png"],capture_output=True)
n=0;t0=time.time()
# 阶段1: 初始市场页(真实chrome窗口) ~2.6s
while time.time()-t0<2.6:
    snap(n);n+=1;time.sleep(0.22)

def click_el(sel):
    r=cmd("Runtime.evaluate",{"expression":"(function(){var el="+sel+";var b=el.getBoundingClientRect();return JSON.stringify({x:b.left+b.width/2,y:b.top+b.height/2});})()","returnByValue":True})
    c=json.loads(r.get("result",{}).get("value","{\"x\":640,\"y\":400}"))
    x,y=int(c["x"]),int(c["y"])
    cmd("Input.dispatchMouseEvent",{"type":"mouseMoved","x":x,"y":y})
    cmd("Input.dispatchMouseEvent",{"type":"mousePressed","x":x,"y":y,"button":"left","clickCount":1})
    cmd("Input.dispatchMouseEvent",{"type":"mouseReleased","x":x,"y":y,"button":"left","clickCount":1})

# 阶段2: 真实滚动到表格 + 点第3行(MicroSettle)看详情 ~1.7s
cmd("Runtime.evaluate",{"expression":"window.scrollTo(0,240)"});time.sleep(0.5)
click_el("document.querySelectorAll('tr.row')[2]")
t0=time.time()
while time.time()-t0<1.7:
    snap(n);n+=1;time.sleep(0.22)

# 阶段3: 点第1行(RayAgent)看详情(高亮候选) ~1.7s
click_el("document.querySelectorAll('tr.row')[0]")
t0=time.time()
while time.time()-t0<1.7:
    snap(n);n+=1;time.sleep(0.22)

# 阶段4: 点"运行竞价" -> 结算面板 ~2.6s
click_el("document.getElementById('run')")
t0=time.time()
while time.time()-t0<2.6:
    snap(n);n+=1;time.sleep(0.22)
print("real-desktop frames:",n)
ws.close()
