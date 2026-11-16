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
.chips{display:flex;flex-wrap:wrap;gap:4px;margin:0 0 6px;align-items:center}.chip{background:var(--ink);color:var(--bg);border-radius:10px;padding:0 8px;cursor:pointer;font-size:11px}.clear{color:var(--mute);text-decoration:underline;cursor:pointer;font-size:11px}.mute{color:var(--mute);font-size:11px}
.gh{margin:10px 6px 2px;font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute)}.cl.zero{opacity:.4}
.hint{border:1px solid var(--line);border-left:3px solid #d9822b;border-radius:6px;padding:6px 8px;margin:8px 0;background:var(--bg)}
.tag.sug{border-style:dashed;color:var(--mute)}
.tl{display:grid;grid-template-columns:auto 1fr;gap:0 8px;border-left:2px solid var(--line);padding-left:8px;margin:2px 0}.tl .me{font-weight:600}.tl time{color:var(--mute);white-space:nowrap}.tl small{color:var(--mute)}
.tag{display:inline-block;border:1px solid var(--line);border-radius:10px;padding:0 7px;margin:0 4px 4px 0;font-size:11px}
pre{white-space:pre-wrap;word-break:break-word;font:12px/1.5 inherit;background:var(--bg);padding:8px;border-radius:6px}
a{color:inherit}.rel{display:block;padding:2px 0;cursor:pointer;text-decoration:underline dotted}
@media (max-width:900px){body{grid-template-columns:1fr;grid-template-rows:auto 40vh 1fr auto}#list{display:none}}
</style></head><body>
<header><b id="home" style="cursor:pointer" title="Overview">__REPO__</b><input id="q" type="search" placeholder="Search title / body…">
<label><input id="showE" type="checkbox" checked> links</label>
<label title="pairs that are among each other's 5 most similar items"><input id="showM" type="checkbox" checked> similar</label>
<label title="count suggested labels when filtering by label"><input id="showS" type="checkbox" checked> suggested</label>
<label><input id="showI" type="checkbox" checked> issues</label>
<label><input id="showP" type="checkbox" checked> PRs</label><span id="count" style="color:var(--mute)"></span><span id="frag" style="color:var(--mute);margin-left:auto"></span></header>
<div id="list"></div>
<div id="map"><canvas id="c"></canvas><div id="tip"></div></div>
<div id="detail"></div>
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
items.forEach(d=>{d.ls=d.l.split(',').filter(Boolean);d.sg=d.sg||[]});
const lsOf=d=>showS.checked?d.ls.concat(d.sg.map(x=>x[0])):d.ls;
const comps=[...new Set(items.flatMap(d=>d.ls.filter(l=>l.startsWith('component:'))))].sort();
const compOf=d=>lsOf(d).find(l=>l.startsWith('component:'));
const grey=matchMedia('(prefers-color-scheme:dark)').matches?'#666':'#aaa';
const colI=d=>{if(mode==='t')return col(d.c);const c=compOf(d);return c?col(comps.indexOf(c)):grey};
let W,H,s=1,tx=0,ty=0,sel=-1,hov=-1,cluster=null,term='',mode='t';
const chosen=new Set(),NONE='\0none',TYPE=/^(0[0-7]|17|23|33) - /;
const grp=l=>l===NONE?'none':l.startsWith('pr:')?'pr':l.startsWith('dup:')?'dup':l.startsWith('cmp:')?'cmp':l.startsWith('age:')?'age':l.startsWith('component:')?'component':TYPE.test(l)?'type':'other';
const YEAR=365.25*864e5,ageOf=d=>{const y=(new Date(D.now)-new Date(d.up))/YEAR;return y<1?'age:0':y<3?'age:1':y<5?'age:3':'age:5'};
const keysOf=d=>{const k=lsOf(d).slice();if(d.ps)k.push('pr:'+d.ps[0]);if(d.zb)k.push('pr:similar');if(d.du)k.push('dup:'+d.du[1][0][1]);if(d.cp)k.push('cmp:yes');k.push(ageOf(d));return k};
function passAll(d,skip){const k=keysOf(d),by={};for(const c of chosen){const g=grp(c);if(g!==skip)(by[g]=by[g]||[]).push(c)}
 for(const g in by){if(!by[g].some(c=>c===NONE?!lsOf(d).length:k.includes(c)))return false}return true}
function fit(){const r=cv.getBoundingClientRect(),dpr=devicePixelRatio;W=r.width;H=r.height;cv.width=W*dpr;cv.height=H*dpr;g.setTransform(dpr,0,0,dpr,0,0);
 s=Math.min(W/(x1-x0),H/(y1-y0))*.92;tx=(W-(x1-x0)*s)/2-x0*s;ty=(H-(y1-y0)*s)/2-y0*s;draw()}
const P=i=>[items[i].x*s+tx,items[i].y*s+ty];
const visible=i=>{const d=items[i];if(d.k==='pr'?!showP.checked:!showI.checked)return false;if(mode==='t'){if(cluster!==null&&d.c!==cluster)return false}else if(!passAll(d,null))return false;return !term||d.t.toLowerCase().includes(term)||d.s.toLowerCase().includes(term)};
function draw(){g.clearRect(0,0,W,H);const vis=items.map((_,i)=>visible(i));let n=0;vis.forEach(v=>n+=v);count.textContent=n+' / '+items.length;
 const hl=sel>=0?new Set([sel,...nb[sel].map(e=>e[0])]):null;
 {for(const [a,b,k] of edges){if(!vis[a]||!vis[b]||!(k==='similar'?showM:showE).checked)continue;const on=hl&&(a===sel||b===sel);if(hl&&!on)continue;
  const [ax,ay]=P(a),[bx,by]=P(b);g.beginPath();g.moveTo(ax,ay);g.lineTo(bx,by);g.setLineDash(k==='similar'?[3,3]:[]);g.strokeStyle=on?getComputedStyle(document.body).getPropertyValue('--sel'):k==='closes'||k==='duplicate_of'?'rgba(220,80,60,.45)':k==='similar'?'rgba(60,130,220,.45)':getComputedStyle(document.body).getPropertyValue('--edge');g.lineWidth=on?1.4:k==='closes'?1:.8;g.stroke()}g.setLineDash([])}
 const r=Math.max(2,Math.min(5,s*.6));
 for(let i=0;i<items.length;i++){if(!vis[i])continue;const [x,y]=P(i);if(x<-9||y<-9||x>W+9||y>H+9)continue;const dim=hl&&!hl.has(i);
  g.globalAlpha=dim?.15:.9;g.fillStyle=colI(items[i]);const q=i===sel?r*1.8:r;
  if(items[i].k==='pr')g.fillRect(x-q,y-q,2*q,2*q);else{g.beginPath();g.arc(x,y,q,0,7);g.fill()}
  if(i===sel||i===hov){g.globalAlpha=1;g.strokeStyle=getComputedStyle(document.body).getPropertyValue('--sel');g.lineWidth=1.5;g.strokeRect(x-q-2,y-q-2,2*q+4,2*q+4)}}
 g.globalAlpha=1}
function pick(mx,my){let b=-1,bd=100;for(let i=0;i<items.length;i++){if(!visible(i))continue;const [x,y]=P(i),d=(x-mx)**2+(y-my)**2;if(d<bd){bd=d;b=i}}return b}
function esc(t){return t.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
const ref=o=>{const j=byNum.get(o);return j!==undefined?`<span class="rel" style="display:inline" data-i="${j}">#${o}</span>`:`<a href="${D.repo}/issues/${o}" target="_blank">#${o}</a>`};
function show(i){sel=i;draw();const d=items[i];
 const row=([o,cr,st,t,r])=>{const j=byNum.get(o),lab=`#${o} [${st}] ${esc(t)} <small>${r}</small>`;return `<time>${cr}</time>`+(j!==undefined?`<span class="rel" data-i="${j}">${lab}</span>`:`<a class="rel" href="${D.repo}/issues/${o}" target="_blank">${lab}</a>`)};
 const me=`<time>${d.cr}</time><span class="me">#${d.n} this ${d.k==='pr'?'PR':'issue'}</span>`;
 const rel=d.tl?`<div class="tl">${d.tl.filter(e=>e[1]<d.cr).map(row).join('')}${me}${d.tl.filter(e=>e[1]>=d.cr).map(row).join('')}</div>`:'';
 detail.innerHTML=`<h2>${esc(d.t)}</h2><div class="meta">${d.k==='pr'?'PR':'Issue'} <a href="${d.u}" target="_blank">#${d.n}</a> · ${esc(d.a||'')} · ${d.cm} comments · updated ${d.up.slice(0,10)}</div>
 <div>${d.ls.map(l=>`<span class="tag">${esc(l)}</span>`).join('')}${d.sg.map(([l,p,src])=>`<span class="tag sug" title="suggested by ${src}${src==='vote'?' ('+p+' votes)':p?' ('+p.toFixed(2)+' kNN)':''}">${esc(l)} ?</span>`).join('')}<span class="tag" style="border-color:${col(d.c)}">${esc(D.names[d.c])}</span></div>
 ${d.ps&&d.ps[0]!=='none'?`<div class="hint"><b>${PS['pr:'+d.ps[0]]}</b> ${d.ps[1].map(([n,f])=>`<a href="${D.repo}/pull/${n}" target="_blank">#${n}</a> ${f}`).join(', ')}</div>`:''}${d.zb?`<div class="hint"><b>Later merged PR looks like the fix</b> ${ref(d.zb[0])} ${esc(d.zb[2])} <small style="color:var(--mute)">${Math.round(d.zb[1]*100)}% similar, no link</small></div>`:''}${d.cp?`<div class="hint"><b>Open PRs after the same thing</b><br>${d.cp.map(([o,r,t])=>`${ref(o)} ${esc(t)} <small style="color:var(--mute)">${r}</small>`).join('<br>')}</div>`:''}${d.du?`<div class="hint"><b>${DUP['dup:'+d.du[1][0][1]]}</b>${d.du[0]?` · keep ${ref(d.du[0])} (original or oldest)`:''}<br>${d.du[1].map(([o,lv,s,st,t])=>`${ref(o)} [${st}] ${esc(t)} <small style="color:var(--mute)">${lv} ${Math.round(s*100)}%</small>`).join('<br>')}</div>`:''}${d.si?`<h3 style="font-size:12px;color:var(--mute);margin:10px 0 2px">Similar</h3>`+d.si.map(([o,s,t,st])=>{const j=byNum.get(o),lab=`${Math.round(s*100)}% #${o} [${st}] ${esc(t)}`;return j!==undefined?`<span class="rel" data-i="${j}">${lab}</span>`:`<a class="rel" href="${D.repo}/issues/${o}" target="_blank">${lab}</a>`}).join(''):''}${rel?`<h3 style="font-size:12px;color:var(--mute);margin:10px 0 2px">Timeline (links and similar items)</h3>${rel}`:''}<pre>${esc(d.b)}</pre>`;
 detail.querySelectorAll('.rel[data-i]').forEach(e=>e.onclick=()=>{const j=+e.dataset.i;focus(j);show(j)})}
function focus(j){const [x,y]=[items[j].x,items[j].y];tx=W/2-x*s;ty=H/2-y*s;draw()}
cv.onmousemove=e=>{const r=cv.getBoundingClientRect();if(drag){tx+=e.movementX;ty+=e.movementY;draw();return}
 const i=pick(e.clientX-r.left,e.clientY-r.top);if(i!==hov){hov=i;draw()}
 tip.style.display=i>=0?'block':'none';if(i>=0){tip.textContent='#'+items[i].n+' '+items[i].t;tip.style.left=Math.min(e.clientX-r.left+12,W-330)+'px';tip.style.top=(e.clientY-r.top+12)+'px'}};
let drag=false,moved=0;cv.onmousedown=()=>{drag=true;moved=0;cv.style.cursor='grabbing'};
addEventListener('mouseup',e=>{if(!drag)return;drag=false;cv.style.cursor='grab'});
cv.onclick=e=>{const r=cv.getBoundingClientRect();const i=pick(e.clientX-r.left,e.clientY-r.top);if(i>=0)show(i);else{sel=-1;draw();overview()}};
const OV={close_duplicate_marked:'Marked duplicate on GitHub, still open',close_fixed_linked:'Closing PR merged, still open',close_duplicate_likely:'Likely duplicate of an older issue',close_fixed_similar:'Later merged PR looks like the fix',review_competing:'Open PRs after the same thing'};
function overview(){const iss=items.filter(d=>d.k==='issue'),n=k=>items.filter(d=>keysOf(d).includes(k)).length;
 const cat={};items.forEach(d=>{const c=cat[d.c]=cat[d.c]||[0,0];c[0]++;c[1]+=d.cm});
 const hot=Object.entries(cat).sort((a,b)=>b[1][1]-a[1][1]).slice(0,8);
 const talk=items.slice().sort((a,b)=>b.cm-a.cm).slice(0,8);
 const sec=(t,h)=>`<h3 style="font-size:12px;color:var(--mute);margin:12px 0 2px">${t}</h3>${h}`;
 detail.innerHTML=`<h2>Overview</h2><div class="meta">${iss.length} open issues, ${items.length-iss.length} open PRs. Click a point for details; circle = issue, square = PR.</div>`+
 sec('Last activity',Object.keys(AGE).map(k=>`${AGE[k]}: <b>${n(k)}</b>`).join('<br>'))+
 Object.keys(OV).filter(k=>D.over[k]).map(k=>sec(`${OV[k]} (${D.over[k].length})`,D.over[k].slice(0,8).map(([o,c,r])=>`${ref(o)} ${esc(items[byNum.get(o)]?.t||'')} <small style="color:var(--mute)">${Math.round(c*100)}% · ${esc(r)}</small>`).join('<br>')+(D.over[k].length>8?`<br><small style="color:var(--mute)">… ${D.over[k].length-8} more in report.md</small>`:''))).join('')+
 sec('Hot categories (comments on open items)',hot.map(([c,[m,cm]])=>`<span class="rel" data-c="${c}">${esc(D.names[c])}</span> <small style="color:var(--mute)">${m} open, ${cm} comments</small>`).join(''))+
 sec('Most discussed open items',talk.map(d=>`${ref(d.n)} ${esc(d.t)} <small style="color:var(--mute)">${d.cm} comments</small>`).join('<br>'));
 detail.querySelectorAll('.rel[data-i]').forEach(e=>e.onclick=()=>{const j=+e.dataset.i;focus(j);show(j)});
 detail.querySelectorAll('.rel[data-c]').forEach(e=>e.onclick=()=>{mode='t';cluster=+e.dataset.c;renderList();draw()})}
home.onclick=()=>{sel=-1;draw();overview()};
cv.onwheel=e=>{e.preventDefault();const r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top,f=Math.exp(-e.deltaY*.0015);tx=mx-(mx-tx)*f;ty=my-(my-ty)*f;s*=f;draw()};
const counts={};items.forEach(d=>counts[d.c]=(counts[d.c]||0)+1);
const order=Object.keys(counts).map(Number).sort((a,b)=>counts[b]-counts[a]);
const PS={'pr:merged':'Closing PR merged: still open?','pr:open':'Closing PR open','pr:abandoned':'Closing PR abandoned','pr:tracking':'Tracking issue (has sub-issues)','pr:none':'No closing PR'};
const DUP={'dup:github':'Marked duplicate on GitHub','dup:likely':'Likely duplicate (very similar)','dup:possible':'Possible duplicate (nearest of each other)'};
const AGE={'age:0':'Active in the last year','age:1':'Quiet for 1-3 years','age:3':'Quiet for 3-5 years','age:5':'Quiet for over 5 years'};
PS['pr:similar']='Later merged PR looks like the fix (no link)';
const HINT={...PS,...DUP,...AGE,'cmp:yes':'Open PRs after the same thing'};frag.textContent=D.frag||'';
const GN={cmp:'Competing PRs',age:'Last activity',dup:'Duplicates',pr:'Issues by closing PR',type:'Type',component:'Component',other:'Other'};
function renderList(){const tab=(m,t)=>`<span class="tab${mode===m?' on':''}" data-m="${m}">${t}</span>`;
 let h=`<div class="tabs">${tab('t','Categories')}${tab('l','Labels')}</div>`;
 if(mode==='t'){h+=`<div class="cl${cluster===null?' on':''}" data-c="">All categories <em>${items.length}</em></div>`+order.map(c=>`<div class="cl${cluster===c?' on':''}" data-c="${c}"><i style="background:${col(c)}"></i><span>${esc(D.names[c])}</span><em>${counts[c]}</em></div>`).join('');list.innerHTML=h;return}
 const gl={dup:{},pr:{},cmp:{},age:{},type:{},component:{},other:{}},tot={},cnt={};
 for(const d of items)for(const l of keysOf(d)){tot[l]=(tot[l]||0)+1;gl[grp(l)][l]=1}
 for(const g in gl)for(const l in gl[g])cnt[l]=0;
 for(const d of items){if(d.k==='pr'?!showP.checked:!showI.checked)continue;const k=new Set(keysOf(d));for(const g of Object.keys(gl)){if(!passAll(d,g))continue;for(const l of k)if(grp(l)===g)cnt[l]++}}
 const nl=items.filter(d=>(d.k==='pr'?showP.checked:showI.checked)&&!lsOf(d).length&&passAll(d,'none')).length;
 h+=`<div class="chips">${[...chosen].map(c=>`<span class="chip" data-l="${esc(c)}">${esc(c===NONE?'(no label)':HINT[c]||c)} ×</span>`).join('')}${chosen.size?'<span class="clear">clear all</span>':'<span class="mute">Pick labels: OR within a group, AND across groups</span>'}</div>`;
 h+=`<div class="cl${chosen.has(NONE)?' on':''}" data-l="${NONE}"><i style="background:${grey}"></i><span>(no label)</span><em>${nl}</em></div>`;
 for(const g of ['dup','pr','cmp','age','type','component','other']){const ls=Object.keys(gl[g]).sort((a,b)=>g==='age'?a.localeCompare(b):tot[b]-tot[a]);if(!ls.length)continue;
  h+=`<div class="gh">${GN[g]}</div>`+ls.map(l=>{const ci=comps.indexOf(l);return `<div class="cl${chosen.has(l)?' on':''}${cnt[l]?'':' zero'}" data-l="${esc(l)}"><i style="background:${ci>=0?col(ci):'transparent'};border:1px solid var(--line)"></i><span>${esc(HINT[l]||l)}</span><em>${cnt[l]}</em></div>`}).join('')}
 const top=list.scrollTop;list.innerHTML=h;list.scrollTop=top}
list.onclick=e=>{const t=e.target.closest('.tab');if(t){mode=t.dataset.m;renderList();draw();return}
 if(e.target.closest('.clear')){chosen.clear();renderList();draw();return}
 const el=e.target.closest('.cl,.chip');if(!el)return;
 if(el.dataset.c!==undefined){cluster=el.dataset.c===''?null:+el.dataset.c}
 else{const l=el.dataset.l;if(chosen.has(l))chosen.delete(l);else{if(l===NONE)chosen.clear();else chosen.delete(NONE);chosen.add(l)}}
 renderList();draw()};
renderList();
q.oninput=()=>{term=q.value.trim().toLowerCase();draw()};[showE,showM,showI,showP].forEach(x=>x.onchange=draw);showS.onchange=()=>{renderList();draw()};
addEventListener('resize',fit);fit();overview();
</script></body></html>"""


REL = {"closes": ("closes", "closed by"), "mentions": ("mentions", "mentioned by"),
       "duplicate_of": ("duplicate of", "has duplicate"), "sub_issue": ("sub-issue of", "has sub-issue")}


def main(path):
    db = sqlite3.connect(path, timeout=120)
    repo = db.execute("select v from meta where k='repo'").fetchone()[0]
    items = [dict(n=n, k=k, t=t, b=(b or "")[:2000], s=(b or "")[:600], a=a, l=l or "", cm=cm, up=up, cr=cr[:10], u=u, c=c, x=x, y=y)
             for n, k, t, b, a, l, cm, up, cr, u, c, x, y in db.execute(
                 "select i.number,kind,title,body,author,labels,comments,updated_at,created_at,url,cluster,x,y "
                 "from items i join topics t on t.number=i.number where i.state='open' and t.x is not null")]
    names = dict(db.execute("select id, name from categories")) | {-1: "Unsorted"}
    links = [list(r) for r in db.execute(
        "select distinct src, dst, replace(kind,'closes_official','closes') from links "
        "where src in (select number from items where state='open') and dst in (select number from items where state='open')")]
    has = lambda t: db.execute("select 1 from sqlite_master where name=?", (t,)).fetchone()
    is_open = {it["n"] for it in items}
    # timeline: everything tied to an open item by a link (either direction, any state) or a semantic link, oldest first
    info = {n: (cr[:10], f"{k} " + ("merged" if m else st), t[:100]) for n, cr, k, m, st, t in db.execute(
        "select number, created_at, kind, merged, state, title from items")}
    tl = {}
    for a, b, k in db.execute("select src, dst, kind from links"):
        k = "closes" if k.startswith("closes") else k
        for me, other, out in ((a, b, True), (b, a, False)):
            if me in is_open and other in info:
                rel = REL[k][not out]
                if k != "mentions" or other not in tl.get(me, {}):
                    tl.setdefault(me, {})[other] = rel
    if has("similar"):
        for a, b, rank in db.execute("select a, b, rank from similar"):
            if a in is_open and b in is_open:
                links.append([a, b, "similar"])
            for me, other in ((a, b), (b, a)):
                if me in is_open and other not in tl.get(me, {}):
                    tl.setdefault(me, {})[other] = "nearest match" if rank == 0 else "similar"
    ps = {n: [st, json.loads(prs)] for n, st, prs in db.execute("select number, status, prs from pr_status")} if has("pr_status") else {}
    du, frag = {}, ""
    if has("dup_pairs"):
        master = dict(db.execute("select number, master from dup_master where master != number"))
        best = {"github": 0, "likely": 1, "possible": 2}
        for a, b, s, lv in db.execute("select a, b, sim, level from dup_pairs"):
            for me, other in ((a, b), (b, a)):
                if me in is_open:
                    du.setdefault(me, [None, []])[1].append([other, lv, round(s, 2), *info[other][1:]])
        for n, d in du.items():
            d[1].sort(key=lambda e: (best[e[1]], -e[2]))
            d[0] = master.get(n)
        issues = sum(1 for it in items if it["k"] == "issue")
        extra = sum(1 for it in items if it["n"] in master)
        frag = f"{issues} open issues ≈ {issues - extra} distinct problems"
    zb = {n: [p, round(s, 2), info[p][2]] for n, p, s in db.execute("select number, pr, sim from zombie")} if has("zombie") else {}
    cp = {}
    if has("pr_compete"):
        for a, b, reason, issue, s in db.execute("select a, b, reason, issue, sim from pr_compete"):
            for me, other in ((a, b), (b, a)):
                cp.setdefault(me, []).append([other, f"both close #{issue}" if issue else f"{s:.0%} similar, different authors", info[other][2]])
    over = {}
    if has("actions"):
        for kind, n, target, conf, reason in db.execute("select kind, number, target, confidence, reason from actions where kind != 'add_label' order by confidence desc, number"):
            over.setdefault(kind, []).append([n, round(conf, 2), reason])
    sg = {}
    if has("suggested"):
        best = {}
        for n, ax, lab, sc, src in db.execute("select number,axis,label,score,source from suggested"):
            best[(n, ax, lab) if src == "vote" else (n, ax)] = [lab, round(sc or 0, 2), src]
        for key, v in best.items():
            sg.setdefault(key[0], []).append(v)
    si = {}
    if db.execute("select 1 from sqlite_master where name='neighbors'").fetchone():
        for n, o, sim, t, st, m, k in db.execute(
                "select n.number, n.other, n.sim, i.title, i.state, i.merged, i.kind from neighbors n join items i on i.number=n.other "
                "where n.number in (select number from items where state='open') order by n.number, n.rank"):
            si.setdefault(n, []).append([o, round(sim, 3), t[:100], f"{k} " + ("merged" if m else st)])
    for it in items:
        if it["n"] in tl:
            it["tl"] = sorted([o, *info[o], rel] for o, rel in tl[it["n"]].items())[:60]
            it["tl"].sort(key=lambda e: e[1])
        if it["n"] in ps:
            it["ps"] = ps[it["n"]]
        if it["n"] in du:
            it["du"] = du[it["n"]]
        if it["n"] in zb:
            it["zb"] = zb[it["n"]]
        if it["n"] in cp:
            it["cp"] = cp[it["n"]]
        if it["n"] in si:
            it["si"] = si[it["n"]]
        if it["n"] in sg:
            it["sg"] = sg[it["n"]]
    html = PAGE.replace("__REPO__", repo).replace("__DATA__", json.dumps(dict(items=items, names=names, links=links, frag=frag, over=over, now=max(it["up"] for it in items), repo=f"https://github.com/{repo}"), ensure_ascii=False).replace("</", "<\\/"))
    out = Path(path).with_name("graph.html")
    out.write_text(html, encoding="utf-8")
    print(f"{out}  {out.stat().st_size/1e6:.1f} MB")


if __name__ == "__main__":
    main(sys.argv[1])
