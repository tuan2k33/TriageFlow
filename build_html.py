"""Build a self-contained graph.html (topic map + links) next to the repo db.

usage: python build_html.py data/<owner>__<name>/repo.db
"""
import json, sqlite3, sys
from pathlib import Path

PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__REPO__ map</title>
<style>
:root{--bg:#fafaf8;--panel:#fff;--ink:#1c1c1a;--mute:#6b6b66;--line:#e2e2dc;--edge:rgba(60,60,60,.35);--sel:#111}
@media (prefers-color-scheme:dark){:root{--bg:#141414;--panel:#1c1c1c;--ink:#e8e8e3;--mute:#9a9a94;--line:#2c2c2a;--edge:rgba(200,200,200,.3);--sel:#fff}}
*{box-sizing:border-box}html,body{height:100%;margin:0}
body{background:var(--bg);color:var(--ink);font:13px/1.45 system-ui,sans-serif;display:grid;grid-template-columns:260px 1fr 380px;grid-template-rows:auto 1fr;overflow:hidden}
header{grid-column:1/-1;display:flex;gap:12px;align-items:center;padding:8px 12px;border-bottom:1px solid var(--line);background:var(--panel)}
header b{font-size:14px}header input[type=search]{flex:1;max-width:420px;padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink)}
header label{color:var(--mute);white-space:nowrap}
#list,#detail{background:var(--panel);overflow:auto;padding:8px}
#list{border-right:1px solid var(--line)}#detail{border-left:1px solid var(--line)}
.tabs{display:flex;gap:4px;margin-bottom:6px}.tab{flex:1;text-align:center;padding:4px;border:1px solid var(--line);border-radius:6px;cursor:pointer;color:var(--mute)}.tab.on{background:var(--bg);color:var(--ink);font-weight:600}
.cl{display:flex;gap:8px;align-items:center;padding:4px 6px;border-radius:5px;cursor:pointer}
.cl:hover,.cl.on{background:var(--bg)}.cl i{width:10px;height:10px;border-radius:50%;flex:none}
.cl span{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.cl em{color:var(--mute);font-style:normal}
#map{position:relative;min-width:0}canvas{width:100%;height:100%;display:block;cursor:grab}
#tip{position:absolute;pointer-events:none;background:var(--panel);border:1px solid var(--line);padding:3px 7px;border-radius:5px;max-width:320px;display:none}
h2{font-size:15px;margin:2px 0 6px}.meta{color:var(--mute);margin-bottom:8px}
.tag{display:inline-block;border:1px solid var(--line);border-radius:10px;padding:0 7px;margin:0 4px 4px 0;font-size:11px}
pre{white-space:pre-wrap;word-break:break-word;font:12px/1.5 inherit;background:var(--bg);padding:8px;border-radius:6px}
a{color:inherit}.rel{display:block;padding:2px 0;cursor:pointer;text-decoration:underline dotted}
@media (max-width:900px){body{grid-template-columns:1fr;grid-template-rows:auto 40vh 1fr auto}#list{display:none}}
</style></head><body>
<header><b>__REPO__</b><input id="q" type="search" placeholder="Search title / body…">
<label><input id="showE" type="checkbox" checked> links</label>
<label><input id="showI" type="checkbox" checked> issues</label>
<label><input id="showP" type="checkbox" checked> PRs</label><span id="count" style="color:var(--mute)"></span></header>
<div id="list"></div>
<div id="map"><canvas id="c"></canvas><div id="tip"></div></div>
<div id="detail"><div class="meta">Click a point. Circle = issue, square = PR. Scroll to zoom, drag to pan.</div></div>
<script>
const D=__DATA__;
const items=D.items,byNum=new Map(items.map((d,i)=>[d.n,i]));
const nb=items.map(()=>[]);
for(const [a,b,k] of D.links){const i=byNum.get(a),j=byNum.get(b);if(i===undefined||j===undefined)continue;nb[i].push([j,k,1]);nb[j].push([i,k,0])}
const edges=D.links.map(([a,b,k])=>[byNum.get(a),byNum.get(b),k]).filter(e=>e[0]!==undefined&&e[1]!==undefined);
const hue=c=>(c*137.508)%360,col=c=>`hsl(${hue(c)} 65% ${matchMedia('(prefers-color-scheme:dark)').matches?62:45}%)`;
let xs=items.map(d=>d.x),ys=items.map(d=>d.y);
const x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);
const cv=document.getElementById('c'),g=cv.getContext('2d');
items.forEach(d=>d.ls=d.l.split(',').filter(Boolean));
const comps=[...new Set(items.flatMap(d=>d.ls.filter(l=>l.startsWith('component:'))))].sort();
const compOf=d=>d.ls.find(l=>l.startsWith('component:'));
const grey=matchMedia('(prefers-color-scheme:dark)').matches?'#666':'#aaa';
const colI=d=>{if(mode==='t')return col(d.c);const c=compOf(d);return c?col(comps.indexOf(c)):grey};
let W,H,s=1,tx=0,ty=0,sel=-1,hov=-1,cluster=null,term='',mode='t',lab=null;
function fit(){const r=cv.getBoundingClientRect(),dpr=devicePixelRatio;W=r.width;H=r.height;cv.width=W*dpr;cv.height=H*dpr;g.setTransform(dpr,0,0,dpr,0,0);
 s=Math.min(W/(x1-x0),H/(y1-y0))*.92;tx=(W-(x1-x0)*s)/2-x0*s;ty=(H-(y1-y0)*s)/2-y0*s;draw()}
const P=i=>[items[i].x*s+tx,items[i].y*s+ty];
const visible=i=>{const d=items[i];if(d.k==='pr'?!showP.checked:!showI.checked)return false;if(mode==='t'){if(cluster!==null&&d.c!==cluster)return false}else if(lab!==null&&(lab===''?d.ls.length:!d.ls.includes(lab)))return false;return !term||d.t.toLowerCase().includes(term)||d.s.toLowerCase().includes(term)};
function draw(){g.clearRect(0,0,W,H);const vis=items.map((_,i)=>visible(i));let n=0;vis.forEach(v=>n+=v);count.textContent=n+' / '+items.length;
 const hl=sel>=0?new Set([sel,...nb[sel].map(e=>e[0])]):null;
 if(showE.checked){for(const [a,b,k] of edges){if(!vis[a]||!vis[b])continue;const on=hl&&(a===sel||b===sel);if(hl&&!on)continue;
  const [ax,ay]=P(a),[bx,by]=P(b);g.beginPath();g.moveTo(ax,ay);g.lineTo(bx,by);g.strokeStyle=on?getComputedStyle(document.body).getPropertyValue('--sel'):k==='closes'?'rgba(220,80,60,.45)':getComputedStyle(document.body).getPropertyValue('--edge');g.lineWidth=on?1.4:k==='closes'?1:.8;g.stroke()}}
 const r=Math.max(2,Math.min(5,s*.6));
 for(let i=0;i<items.length;i++){if(!vis[i])continue;const [x,y]=P(i);if(x<-9||y<-9||x>W+9||y>H+9)continue;const dim=hl&&!hl.has(i);
  g.globalAlpha=dim?.15:.9;g.fillStyle=colI(items[i]);const q=i===sel?r*1.8:r;
  if(items[i].k==='pr')g.fillRect(x-q,y-q,2*q,2*q);else{g.beginPath();g.arc(x,y,q,0,7);g.fill()}
  if(i===sel||i===hov){g.globalAlpha=1;g.strokeStyle=getComputedStyle(document.body).getPropertyValue('--sel');g.lineWidth=1.5;g.strokeRect(x-q-2,y-q-2,2*q+4,2*q+4)}}
 g.globalAlpha=1}
function pick(mx,my){let b=-1,bd=100;for(let i=0;i<items.length;i++){if(!visible(i))continue;const [x,y]=P(i),d=(x-mx)**2+(y-my)**2;if(d<bd){bd=d;b=i}}return b}
function esc(t){return t.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function show(i){sel=i;draw();const d=items[i];const rel=nb[i].map(([j,k,out])=>`<span class="rel" data-i="${j}">${out?'':'← '}${k==='closes'?(out?'closes':'closed by'):(out?'mentions':'mentioned by')} #${items[j].n} ${esc(items[j].t)}</span>`).join('');
 detail.innerHTML=`<h2>${esc(d.t)}</h2><div class="meta">${d.k==='pr'?'PR':'Issue'} <a href="${d.u}" target="_blank">#${d.n}</a> · ${esc(d.a||'')} · ${d.cm} comments · updated ${d.up.slice(0,10)}</div>
 <div>${d.l.split(',').filter(Boolean).map(l=>`<span class="tag">${esc(l)}</span>`).join('')}<span class="tag" style="border-color:${col(d.c)}">${esc(D.names[d.c])}</span></div>
 ${rel?`<h3 style="font-size:12px;color:var(--mute);margin:10px 0 2px">Links</h3>${rel}`:''}<pre>${esc(d.b)}</pre>`;
 detail.querySelectorAll('.rel').forEach(e=>e.onclick=()=>{const j=+e.dataset.i;focus(j);show(j)})}
function focus(j){const [x,y]=[items[j].x,items[j].y];tx=W/2-x*s;ty=H/2-y*s;draw()}
cv.onmousemove=e=>{const r=cv.getBoundingClientRect();if(drag){tx+=e.movementX;ty+=e.movementY;draw();return}
 const i=pick(e.clientX-r.left,e.clientY-r.top);if(i!==hov){hov=i;draw()}
 tip.style.display=i>=0?'block':'none';if(i>=0){tip.textContent='#'+items[i].n+' '+items[i].t;tip.style.left=Math.min(e.clientX-r.left+12,W-330)+'px';tip.style.top=(e.clientY-r.top+12)+'px'}};
let drag=false,moved=0;cv.onmousedown=()=>{drag=true;moved=0;cv.style.cursor='grabbing'};
addEventListener('mouseup',e=>{if(!drag)return;drag=false;cv.style.cursor='grab'});
cv.onclick=e=>{const r=cv.getBoundingClientRect();const i=pick(e.clientX-r.left,e.clientY-r.top);if(i>=0)show(i);else{sel=-1;draw()}};
cv.onwheel=e=>{e.preventDefault();const r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top,f=Math.exp(-e.deltaY*.0015);tx=mx-(mx-tx)*f;ty=my-(my-ty)*f;s*=f;draw()};
const counts={};items.forEach(d=>counts[d.c]=(counts[d.c]||0)+1);
const order=Object.keys(counts).map(Number).sort((a,b)=>counts[b]-counts[a]);
const lc={};items.forEach(d=>d.ls.forEach(l=>lc[l]=(lc[l]||0)+1));
const unl=items.filter(d=>!d.ls.length).length;
const lorder=Object.keys(lc).sort((a,b)=>lc[b]-lc[a]);
function renderList(){const tab=(m,t)=>`<span class="tab${mode===m?' on':''}" data-m="${m}">${t}</span>`;
 let h=`<div class="tabs">${tab('t','Topics (auto)')}${tab('l','Labels')}</div>`;
 if(mode==='t')h+=`<div class="cl${cluster===null?' on':''}" data-c="">All topics <em>${items.length}</em></div>`+order.map(c=>`<div class="cl${cluster===c?' on':''}" data-c="${c}"><i style="background:${col(c)}"></i><span>${esc(D.names[c])}</span><em>${counts[c]}</em></div>`).join('');
 else h+=`<div class="cl${lab===null?' on':''}" data-l="*">All labels <em>${items.length}</em></div><div class="cl${lab===''?' on':''}" data-l=""><i style="background:${grey}"></i><span>(no label)</span><em>${unl}</em></div>`+lorder.map(l=>{const ci=comps.indexOf(l);return `<div class="cl${lab===l?' on':''}" data-l="${esc(l)}"><i style="background:${ci>=0?col(ci):'transparent'};border:1px solid var(--line)"></i><span>${esc(l)}</span><em>${lc[l]}</em></div>`}).join('');
 list.innerHTML=h}
list.onclick=e=>{const t=e.target.closest('.tab');if(t){mode=t.dataset.m;renderList();draw();return}
 const el=e.target.closest('.cl');if(!el)return;
 if('c' in el.dataset)cluster=el.dataset.c===''?null:+el.dataset.c;else lab=el.dataset.l==='*'?null:el.dataset.l;renderList();draw()};
renderList();
q.oninput=()=>{term=q.value.trim().toLowerCase();draw()};[showE,showI,showP].forEach(x=>x.onchange=draw);
addEventListener('resize',fit);fit();
</script></body></html>"""


def main(path):
    db = sqlite3.connect(path)
    repo = db.execute("select v from meta where k='repo'").fetchone()[0]
    items = [dict(n=n, k=k, t=t, b=(b or "")[:2000], s=(b or "")[:600], a=a, l=l or "", cm=cm, up=up, u=u, c=c, x=x, y=y)
             for n, k, t, b, a, l, cm, up, u, c, x, y in db.execute(
                 "select i.number,kind,title,body,author,labels,comments,updated_at,url,cluster,x,y "
                 "from items i join topics t on t.number=i.number")]
    names = {c: lab for c, lab in db.execute("select distinct cluster, label from topics")}
    links = [list(r) for r in db.execute("select src,dst,kind from links")]
    html = PAGE.replace("__REPO__", repo).replace("__DATA__", json.dumps(dict(items=items, names=names, links=links), ensure_ascii=False).replace("</", "<\\/"))
    out = Path(path).with_name("graph.html")
    out.write_text(html, encoding="utf-8")
    print(f"{out}  {out.stat().st_size/1e6:.1f} MB")


if __name__ == "__main__":
    main(sys.argv[1])
