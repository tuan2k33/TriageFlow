"""Build a self-contained browse.html next to the repo db: filters, the list of open items, details with a timeline.

usage: python build_html.py data/<owner>__<name>/repo.db
"""
import json, sqlite3, sys
from pathlib import Path

import axes

PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__REPO__ triage</title>
<style>
:root{--bg:#fafaf8;--panel:#fff;--ink:#1c1c1a;--mute:#6b6b66;--line:#e2e2dc}
@media (prefers-color-scheme:dark){:root{--bg:#141414;--panel:#1c1c1c;--ink:#e8e8e3;--mute:#9a9a94;--line:#2c2c2a}}
*{box-sizing:border-box}html,body{height:100%;margin:0}
body{background:var(--bg);color:var(--ink);font:13px/1.45 system-ui,sans-serif;display:grid;grid-template-columns:270px 1fr 440px;grid-template-rows:auto 1fr;overflow:hidden}
header{grid-column:1/-1;display:flex;gap:12px;align-items:center;padding:8px 12px;border-bottom:1px solid var(--line);background:var(--panel)}
header b{font-size:14px}header input[type=search]{flex:1;max-width:420px;padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink)}
header label,header select{color:var(--mute);white-space:nowrap}
#list,#detail,#rows{overflow:auto;padding:8px}#list,#detail{background:var(--panel)}
#list{border-right:1px solid var(--line)}#detail{border-left:1px solid var(--line)}
.cl{display:flex;gap:8px;align-items:center;padding:3px 6px;border-radius:5px;cursor:pointer}
.cl:hover,.cl.on{background:var(--bg)}.cl.on{font-weight:600}.cl.zero{opacity:.4}
.cl span{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.cl em{color:var(--mute);font-style:normal}
.gh{margin:10px 6px 2px;font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute)}
.chips{display:flex;flex-wrap:wrap;gap:4px;margin:0 0 6px;align-items:center}.chip{background:var(--ink);color:var(--bg);border-radius:10px;padding:0 8px;cursor:pointer;font-size:11px}.clear{color:var(--mute);text-decoration:underline;cursor:pointer;font-size:11px}
.row{padding:6px 8px;border-bottom:1px solid var(--line);cursor:pointer}.row:hover,.row.on{background:var(--panel)}.row small,.mute{color:var(--mute)}
h2{font-size:15px;margin:2px 0 6px}h3{font-size:12px;color:var(--mute);margin:12px 0 2px}.meta{color:var(--mute);margin-bottom:8px}
.hint{border:1px solid var(--line);border-left:3px solid #d9822b;border-radius:6px;padding:6px 8px;margin:8px 0;background:var(--bg)}
.tag{display:inline-block;border:1px solid var(--line);border-radius:10px;padding:0 7px;margin:0 4px 2px 0;font-size:11px}.tag.sug{border-style:dashed;color:var(--mute)}
.tl{display:grid;grid-template-columns:auto 1fr;gap:0 8px;border-left:2px solid var(--line);padding-left:8px;margin:2px 0}.tl .me{font-weight:600}.tl time{color:var(--mute);white-space:nowrap}
pre{white-space:pre-wrap;word-break:break-word;font:12px/1.5 inherit;background:var(--bg);padding:8px;border-radius:6px}
a{color:inherit}.rel{display:block;padding:2px 0;cursor:pointer;text-decoration:underline dotted}
#mx{padding:3px 10px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink);cursor:pointer}#mx.on{background:var(--ink);color:var(--bg)}
table.mx{border-collapse:collapse;font-size:11px}table.mx th{font-weight:500;color:var(--mute);padding:2px 4px}table.mx thead th{writing-mode:vertical-rl;transform:rotate(180deg);text-align:left;height:120px;vertical-align:bottom}
table.mx tbody th{text-align:right;white-space:nowrap;position:sticky;left:0;background:var(--bg)}table.mx td{width:42px;height:42px;text-align:center;vertical-align:middle;border:1px solid var(--line);cursor:pointer;padding:0}
table.mx td:hover{outline:2px solid var(--ink)}.bub{margin:auto;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px}.bub.sg{border:1.5px dashed var(--mute)}table.mx td.tot,table.mx th.tot{color:var(--mute);cursor:default}
@media (max-width:900px){body{grid-template-columns:1fr;grid-template-rows:auto 45vh 1fr}#list{display:none}}
</style></head><body>
<header><b id="home" style="cursor:pointer" title="Overview">__REPO__</b><input id="q" type="search" placeholder="Search title / body…">
<select id="sort"><option value="up">recently active</option><option value="old">longest quiet</option><option value="cm">most comments</option><option value="n">newest</option></select>
<label title="count suggested labels when filtering by label"><input id="showS" type="checkbox" checked> suggested</label>
<label><input id="showI" type="checkbox" checked> issues</label>
<label><input id="showP" type="checkbox" checked> PRs</label><button id="mx" title="open items by type and component">Matrix</button><span id="count" class="mute"></span><span id="frag" class="mute" style="margin-left:auto"></span></header>
<div id="list"></div><div id="rows"></div><div id="detail"></div>
<script>
const D=__DATA__;
const items=D.items,byNum=new Map(items.map((d,i)=>[d.n,i]));
items.forEach(d=>{d.ls=d.l;d.sg=d.sg||[]});
let sel=-1,term='',shown=200,view='list',cellF=null;
const chosen=new Set(),NONE='\0none',TYPES=new Set(D.types),COMP=D.comp?D.comp.toLowerCase()+':':null;
const PS={'pr:merged':'Closing PR merged: still open?','pr:similar':'Later merged PR looks like the fix (no link)','pr:open':'Closing PR open','pr:abandoned':'Closing PR abandoned','pr:tracking':'Tracking issue (has sub-issues)','pr:none':'No closing PR'};
const DUP={'dup:github':'Marked duplicate on GitHub','dup:likely':'Likely duplicate (very similar)','dup:possible':'Possible duplicate (nearest of each other)'};
const AGE={'age:0':'Active in the last year','age:1':'Quiet for 1-3 years','age:3':'Quiet for 3-5 years','age:5':'Quiet for over 5 years'};
const NAME={...PS,...DUP,...AGE,'cmp:yes':'Open PRs after the same thing'};for(const c in D.names)NAME['cat:'+c]=D.names[c];
const GN={dup:'Duplicates',pr:'Issues by closing PR',cmp:'Competing PRs',age:'Last activity',type:'Type',component:'Component',other:'Other labels',cat:'Category (by content)'};
const grp=l=>l===NONE?'none':/^(pr|dup|cmp|age|cat):/.test(l)?l.split(':')[0]:COMP&&l.toLowerCase().startsWith(COMP)?'component':TYPES.has(l)?'type':'other';
const lsOf=d=>showS.checked?d.ls.concat(d.sg.map(x=>x[0])):d.ls;
const YEAR=365.25*864e5,ageOf=d=>{const y=(new Date(D.now)-new Date(d.up))/YEAR;return y<1?'age:0':y<3?'age:1':y<5?'age:3':'age:5'};
const keysOf=d=>{const k=lsOf(d).slice();if(d.ps)k.push('pr:'+d.ps[0]);if(d.zb)k.push('pr:similar');if(d.du)k.push('dup:'+d.du[1][0][1]);if(d.cp)k.push('cmp:yes');k.push(ageOf(d),'cat:'+d.c);return k};
function passAll(d,skip){const k=keysOf(d),by={};for(const c of chosen){const g=grp(c);if(g!==skip)(by[g]=by[g]||[]).push(c)}
 for(const g in by){if(!by[g].some(c=>c===NONE?!lsOf(d).length:k.includes(c)))return false}return true}
const kindOk=d=>d.k==='pr'?showP.checked:showI.checked;
const short=l=>l==='(none)'||!COMP?l.replace(/^\d+ - /,''):(l.toLowerCase().startsWith(COMP)?l.slice(COMP.length).trim():l).replace(/^numpy\./,'').replace(/^\d+ - /,'');
// a repo without type or component labels gets pseudo labels: last activity for rows, the content category for columns
const real=g=>g==='type'?D.ax.type:D.ax.component;
const axOf=(d,g)=>{if(!real(g))return[g==='type'?AGE[ageOf(d)]:D.names[d.c]];const r=lsOf(d).filter(l=>grp(l)===g);return r.length?r:['(none)']};
const inCell=d=>!cellF||axOf(d,'type').includes(cellF[0])&&axOf(d,'component').includes(cellF[1]);
const base=d=>kindOk(d)&&passAll(d,null)&&(!term||d.t.toLowerCase().includes(term)||d.s.toLowerCase().includes(term));
const visible=d=>base(d)&&inCell(d);
const SORT={up:(a,b)=>b.up.localeCompare(a.up),old:(a,b)=>a.up.localeCompare(b.up),cm:(a,b)=>b.cm-a.cm,n:(a,b)=>b.n-a.n};
function esc(t){return t.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
const tags=d=>d.ls.map(l=>`<span class="tag">${esc(l)}</span>`).join('')+d.sg.map(([l,p,src])=>`<span class="tag sug" title="suggested: ${src==='vote'?p+' votes':'kNN score '+p}">${esc(l)} ?</span>`).join('');
function matrix(){const vis=items.filter(base),M={},T={},C={};mx.classList.add('on');
 for(const d of vis){const ts=axOf(d,'type'),cs=axOf(d,'component'),st=['age:3','age:5'].includes(ageOf(d));
  const sg=(real('type')&&ts[0]!=='(none)'&&!d.ls.some(l=>grp(l)==='type'))||(real('component')&&cs[0]!=='(none)'&&!d.ls.some(l=>grp(l)==='component'));
  for(const a of ts)for(const b of cs){const m=M[a+'\u0001'+b]=M[a+'\u0001'+b]||{n:0,s:0,g:0};m.n++;m.s+=st;m.g+=sg;T[a]=(T[a]||0)+1;C[b]=(C[b]||0)+1}}
 const ord=o=>Object.keys(o).sort((a,b)=>(a==='(none)')-(b==='(none)')||o[b]-o[a]),R=real('type')?ord(T):Object.values(AGE).filter(a=>T[a]),K=ord(C),mx_=Math.max(1,...Object.values(M).map(m=>m.n));
 count.textContent=vis.length+' / '+items.length;matrix.R=R;matrix.K=K;
 rows.innerHTML=`<div class="meta">Open items by ${D.ax.type?'type':'last activity (the repo has no type labels)'} (rows) and ${D.ax.component?'component':'content category (the repo has no component labels)'} (columns), with the filters on the left. Size = number of items; color = share quiet for 3+ years (pale: active, dark: forgotten); dashed = some items are here only through a suggested label (toggle “suggested”). An item with two labels counts in both cells. Click a cell to list its items.</div>
 <table class="mx"><thead><tr><th></th>${K.map(k=>`<th title="${esc(k)}">${esc(short(k))}</th>`).join('')}<th class="tot">all</th></tr></thead><tbody>${R.map((r,i)=>`<tr><th title="${esc(r)}">${esc(short(r))}</th>${K.map((k,j)=>{const m=M[r+'\u0001'+k];if(!m)return'<td></td>';
  const w=Math.round(18+20*Math.sqrt(m.n/mx_)),s=m.s/m.n;return`<td data-r="${i}" data-k="${j}" title="${esc(short(r))} × ${esc(short(k))}: ${m.n} open, ${Math.round(s*100)}% quiet 3+ years${m.g?', '+m.g+' via suggested labels':''}"><div class="bub${m.g?' sg':''}" style="width:${w}px;height:${w}px;background:rgba(217,130,43,${(0.12+0.85*s).toFixed(2)})">${m.n}</div></td>`}).join('')}<td class="tot">${T[r]}</td></tr>`).join('')}
 <tr><th class="tot">all</th>${K.map(k=>`<td class="tot">${C[k]}</td>`).join('')}<td class="tot">${vis.length}</td></tr></tbody></table>`}
rows.addEventListener('click',e=>{const c=view==='matrix'&&e.target.closest('td[data-r]');if(!c)return;e.stopImmediatePropagation();
 cellF=[matrix.R[+c.dataset.r],matrix.K[+c.dataset.k]];view='list';mx.classList.remove('on');refresh()},true);
mx.onclick=()=>{view=view==='matrix'?'list':'matrix';if(view==='list')mx.classList.remove('on');refresh()};
function renderRows(){if(view==='matrix')return matrix();const vis=items.filter(visible).sort(SORT[sort.value]);count.textContent=vis.length+' / '+items.length;
 rows.innerHTML=vis.slice(0,shown).map(d=>`<div class="row${byNum.get(d.n)===sel?' on':''}" data-i="${byNum.get(d.n)}"><b>${d.k==='pr'?'PR':'Issue'} #${d.n}</b> ${esc(d.t)}<br>${tags(d)}<small>${d.cm} comments · active ${d.up.slice(0,10)}${d.du?' · '+DUP['dup:'+d.du[1][0][1]]:''}${d.ps&&d.ps[0]!=='none'?' · '+PS['pr:'+d.ps[0]]:''}</small></div>`).join('')
  +(vis.length>shown?`<div class="row mute" id="more">Show more (${vis.length-shown} left)</div>`:'')||'<div class="mute" style="padding:8px">Nothing matches.</div>'}
rows.onclick=e=>{if(e.target.closest('#more')){shown+=400;renderRows();return}const r=e.target.closest('.row');if(r)show(+r.dataset.i)};
const ref=o=>{const j=byNum.get(o);return j!==undefined?`<span class="rel" style="display:inline" data-i="${j}">#${o}</span>`:`<a href="${D.repo}/issues/${o}" target="_blank">#${o}</a>`};
const wire=()=>detail.querySelectorAll('.rel[data-i]').forEach(e=>e.onclick=()=>show(+e.dataset.i));
function show(i){sel=i;renderRows();const d=items[i];
 const row=([o,cr,st,t,r])=>`<time>${cr}</time><span>${ref(o)} [${st}] ${esc(t)} <small class="mute">${r}</small></span>`;
 const me=`<time>${d.cr}</time><span class="me">#${d.n} this ${d.k==='pr'?'PR':'issue'}</span>`;
 const hint=(t,h)=>`<div class="hint"><b>${t}</b> ${h}</div>`,sm=t=>`<small class="mute">${t}</small>`;
 detail.innerHTML=`<h2>${esc(d.t)}</h2><div class="meta">${d.k==='pr'?'PR':'Issue'} <a href="${d.u}" target="_blank">#${d.n}</a> · ${esc(d.a||'')} · ${d.cm} comments · active ${d.up.slice(0,10)}</div>
 <div>${tags(d)}<span class="tag" title="category by content">${esc(D.names[d.c])}</span></div>`
 +(d.ps&&d.ps[0]!=='none'?hint(PS['pr:'+d.ps[0]],d.ps[1].map(([n,f])=>`<a href="${D.repo}/pull/${n}" target="_blank">#${n}</a> ${f}`).join(', ')):'')
 +(d.zb?hint(PS['pr:similar'],`${ref(d.zb[0])} ${esc(d.zb[2])} ${sm(Math.round(d.zb[1]*100)+'% similar')}`):'')
 +(d.cp?hint(NAME['cmp:yes'],'<br>'+d.cp.map(([o,r,t])=>`${ref(o)} ${esc(t)} ${sm(r)}`).join('<br>')):'')
 +(d.du?hint(DUP['dup:'+d.du[1][0][1]],(d.du[0]?`· keep ${ref(d.du[0])} (original or oldest)`:'')+'<br>'+d.du[1].map(([o,lv,s,st,t])=>`${ref(o)} [${st}] ${esc(t)} ${sm(lv+' '+Math.round(s*100)+'%')}`).join('<br>')):'')
 +(d.si?'<h3>Most similar items</h3>'+d.si.map(([o,s,t,st])=>`<div>${Math.round(s*100)}% ${ref(o)} [${st}] ${esc(t)}</div>`).join(''):'')
 +(d.tl?`<h3>Timeline (links and similar items)</h3><div class="tl">${d.tl.filter(e=>e[1]<d.cr).map(row).join('')}${me}${d.tl.filter(e=>e[1]>=d.cr).map(row).join('')}</div>`:'')
 +`<pre>${esc(d.b)}</pre>`;wire()}
const OV={close_duplicate_marked:'Marked duplicate on GitHub, still open',close_fixed_linked:'Closing PR merged, still open',close_duplicate_likely:'Likely duplicate of an older open issue',check_recurrence:'Very similar to an older closed issue',close_fixed_similar:'Later merged PR looks like the fix',review_competing:'Open PRs after the same thing'};
function overview(){sel=-1;renderRows();const iss=items.filter(d=>d.k==='issue'),n=k=>items.filter(d=>keysOf(d).includes(k)).length;
 const cat={};items.forEach(d=>{const c=cat[d.c]=cat[d.c]||[0,0];c[0]++;c[1]+=d.cm});
 const hot=Object.entries(cat).sort((a,b)=>b[1][1]-a[1][1]).slice(0,8),talk=items.slice().sort(SORT.cm).slice(0,8);
 const sec=(t,h)=>`<h3>${t}</h3>${h}`,sm=t=>`<small class="mute">${t}</small>`;
 detail.innerHTML=`<h2>Overview</h2><div class="meta">${iss.length} open issues, ${items.length-iss.length} open PRs. Pick filters on the left, an item in the list for its details.</div>`+
 sec('Last activity',Object.keys(AGE).map(k=>`${AGE[k]}: <b>${n(k)}</b>`).join('<br>'))+
 Object.keys(OV).filter(k=>D.over[k]).map(k=>sec(`${OV[k]} (${D.over[k].length})`,D.over[k].slice(0,8).map(([o,c,r])=>`${ref(o)} ${esc(items[byNum.get(o)]?.t||'')} ${sm(esc(c)+' · '+esc(r))}`).join('<br>')+(D.over[k].length>8?'<br>'+sm(`… ${D.over[k].length-8} more in report.md`):''))).join('')+
 sec('Hot categories (comments on open items)',hot.map(([c,[m,cm]])=>`<span class="rel" data-c="${c}">${esc(D.names[c])} ${sm(m+' open, '+cm+' comments')}</span>`).join(''))+
 sec('Most discussed open items',talk.map(d=>`${ref(d.n)} ${esc(d.t)} ${sm(d.cm+' comments')}`).join('<br>'));wire();
 detail.querySelectorAll('.rel[data-c]').forEach(e=>e.onclick=()=>{chosen.clear();chosen.add('cat:'+e.dataset.c);refresh()})}
function renderList(){const gl={},tot={},cnt={};for(const g in GN)gl[g]={};
 for(const d of items)for(const l of keysOf(d)){tot[l]=(tot[l]||0)+1;gl[grp(l)][l]=1;cnt[l]=0}
 for(const d of items){if(!kindOk(d))continue;const k=new Set(keysOf(d));for(const g in gl){if(!passAll(d,g))continue;for(const l of k)if(grp(l)===g)cnt[l]++}}
 const nl=items.filter(d=>kindOk(d)&&!lsOf(d).length&&passAll(d,'none')).length,nm=c=>c===NONE?'(no label)':NAME[c]||c;
 let h=`<div class="chips">${cellF?`<span class="chip" data-cell="1">${esc(short(cellF[0]))} × ${esc(short(cellF[1]))} ×</span>`:''}${[...chosen].map(c=>`<span class="chip" data-l="${esc(c)}">${esc(nm(c))} ×</span>`).join('')}${chosen.size||cellF?'<span class="clear">clear all</span>':'<span class="mute">Pick filters: OR within a group, AND across groups</span>'}</div>`;
 for(const g in GN){const ls=Object.keys(gl[g]).sort((a,b)=>g==='age'?a.localeCompare(b):tot[b]-tot[a]);if(!ls.length)continue;
  h+=`<div class="gh">${GN[g]}</div>`+(g==='type'?`<div class="cl${chosen.has(NONE)?' on':''}" data-l="${NONE}"><span>(no label)</span><em>${nl}</em></div>`:'')
   +ls.map(l=>`<div class="cl${chosen.has(l)?' on':''}${cnt[l]?'':' zero'}" data-l="${esc(l)}"><span>${esc(nm(l))}</span><em>${cnt[l]}</em></div>`).join('')}
 const top=list.scrollTop;list.innerHTML=h;list.scrollTop=top}
function refresh(){shown=200;renderList();renderRows()}
list.onclick=e=>{if(e.target.closest('.clear')){chosen.clear();cellF=null;refresh();return}
 if(e.target.closest('[data-cell]')){cellF=null;refresh();return}
 const el=e.target.closest('.cl,.chip');if(!el)return;const l=el.dataset.l;
 if(chosen.has(l))chosen.delete(l);else{if(l===NONE)chosen.clear();else chosen.delete(NONE);chosen.add(l)}refresh()};
q.oninput=()=>{term=q.value.trim().toLowerCase();shown=200;renderRows()};[showI,showP,showS].forEach(x=>x.onchange=refresh);sort.onchange=renderRows;
home.onclick=overview;frag.textContent=D.frag||'';renderList();overview();
</script></body></html>"""

REL = {"closes": ("closes", "closed by"), "mentions": ("mentions", "mentioned by"),
       "duplicate_of": ("duplicate of", "has duplicate"), "sub_issue": ("sub-issue of", "has sub-issue")}


def main(path):
    db = sqlite3.connect(path, timeout=120)
    repo = db.execute("select v from meta where k='repo'").fetchone()[0]
    has = lambda t: db.execute("select 1 from sqlite_master where name=?", (t,)).fetchone()
    items = [dict(n=n, k=k, t=t, b=(b or "")[:2000], s=(b or "")[:600], a=a, l=json.loads(l or "[]"), cm=cm, up=up, cr=cr[:10], u=u, c=c)
             for n, k, t, b, a, l, cm, up, cr, u, c in db.execute(
                 "select i.number,kind,title,body,author,labels,comments,updated_at,created_at,url,cluster "
                 "from items i join topics t on t.number=i.number where i.state='open'")]
    names = dict(db.execute("select id, name from categories")) | {-1: "Unsorted"}
    is_open = {it["n"] for it in items}
    info = {n: (cr[:10], f"{k} " + ("merged" if m else st), t[:100]) for n, cr, k, m, st, t in db.execute(
        "select number, created_at, kind, merged, state, title from items")}
    # timeline: everything tied to an open item by a link (either direction, any state) or a semantic link, oldest first
    tl = {}
    for a, b, k in db.execute("select src, dst, kind from links"):
        k = "closes" if k.startswith("closes") else k
        for me, other, out in ((a, b, True), (b, a, False)):
            if me in is_open and other in info and (k != "mentions" or other not in tl.get(me, {})):
                tl.setdefault(me, {})[other] = REL[k][not out]
    if has("similar"):
        for a, b, rank in db.execute("select a, b, rank from similar"):
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
        frag = f"{issues} open issues ≈ {issues - sum(1 for it in items if it['n'] in master)} distinct problems"
    zb = {n: [p, round(s, 2), info[p][2]] for n, p, s in db.execute("select number, pr, sim from zombie")} if has("zombie") else {}
    cp = {}
    if has("pr_compete"):
        for a, b, reason, issue, s in db.execute("select a, b, reason, issue, sim from pr_compete"):
            for me, other in ((a, b), (b, a)):
                cp.setdefault(me, []).append([other, f"both close #{issue}" if issue else f"{s:.0%} similar, different authors", info[other][2]])
    over = {}
    if has("actions"):
        for kind, n, conf, reason in db.execute("select kind, number, confidence, reason from actions where kind != 'add_label' order by confidence desc, number"):
            over.setdefault(kind, []).append([n, f"{conf:.2f}", reason])
    sg = {}
    if has("suggested"):
        for n, lab, sc, src in db.execute("select number, label, score, source from suggested order by axis desc, score desc"):
            sg.setdefault(n, []).append([lab, round(sc or 0, 2), src])
    si = {}
    if has("neighbors"):
        for n, o, sim in db.execute("select number, other, sim from neighbors order by number, rank"):
            if n in is_open:
                si.setdefault(n, []).append([o, round(sim, 3), info[o][2], info[o][1]])
    for it in items:
        n = it["n"]
        if n in tl:
            it["tl"] = sorted(([o, *info[o], rel] for o, rel in tl[n].items()), key=lambda e: e[1])[-60:]
        for key, src in (("ps", ps), ("du", du), ("zb", zb), ("cp", cp), ("si", si), ("sg", sg)):
            if n in src:
                it[key] = src[n]
    found = axes.of_repo(db)  # the repo's own type and component labels; none -> pseudo labels in the matrix
    ax = dict(type=bool(found["type"]), component=bool(found["component"]))
    data = dict(items=items, names=names, frag=frag, over=over, types=found["type"], comp=found["component"], ax=ax, now=max((it["up"] for it in items), default=""), repo=f"https://github.com/{repo}")
    html = PAGE.replace("__REPO__", repo).replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    out = Path(path).with_name("browse.html")
    out.write_text(html, encoding="utf-8")
    print(f"{out}  {out.stat().st_size/1e6:.1f} MB")


if __name__ == "__main__":
    main(sys.argv[1])
