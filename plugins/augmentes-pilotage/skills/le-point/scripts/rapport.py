"""
rapport.py — transforme un constat.json en rapport HTML d'arbitrage.

Le rapport n'est pas un compte rendu : c'est un outil de décision. Chaque carte
porte un fait sourcé, une case à cocher, des options cliquables, et un bouton de
commentaire pour corriger ce que l'IA a mal lu. Les retours s'exportent en
markdown et se recollent dans la conversation.

Fond blanc : c'est un outil de travail, pas une présentation.

Aucune dépendance, aucun appel réseau. Le fichier produit est autonome : il
s'ouvre hors ligne et ne charge rien depuis Internet.

    python3 rapport.py --input constat.json --output le-point.html
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

NIVEAUX = {"now": "t-now", "soon": "t-soon", "open": "t-open", "ok": "t-ok"}

CSS = """
:root{
  --ink:#0F1455; --ink-soft:#3B4577; --ink-mute:#7A84AA;
  --rule:#E4E7F2; --surface:#FFFFFF; --surface-alt:#F5F7FB; --surface-deep:#EDEFF7;
  --roi:#001789; --turquoise:#32D7D7; --accent:#ed734a;
  --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
*{box-sizing:border-box}
body{margin:0;background:var(--surface);color:var(--ink);
  font-family:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:var(--roi)}
.wrap{display:grid;grid-template-columns:230px minmax(0,1fr);gap:56px;max-width:1500px;margin:0 auto;padding:0 40px}
nav{position:sticky;top:0;align-self:start;height:100vh;padding:38px 0;overflow-y:auto}
nav .brand{font-weight:700;letter-spacing:-.02em;font-size:14px;margin-bottom:4px}
nav .date{color:var(--ink-mute);font-size:12px;margin-bottom:26px}
nav a{display:block;padding:7px 12px;color:var(--ink-soft);text-decoration:none;font-size:13.5px;border-left:2px solid transparent}
nav a:hover{color:var(--roi)}
nav a.on{color:var(--roi);font-weight:600;border-left-color:var(--turquoise);background:var(--surface-alt)}
nav .prog{margin-top:24px;padding:12px;background:var(--surface-alt);border-radius:8px;font-size:12px;color:var(--ink-soft)}
nav .prog b{display:block;font-size:22px;color:var(--roi);font-weight:700;letter-spacing:-.02em}
main{padding:48px 0 140px;min-width:0}
header.top{border-bottom:1px solid var(--rule);padding-bottom:28px;margin-bottom:14px}
h1{font-size:32px;line-height:1.15;letter-spacing:-.025em;margin:0 0 10px;font-weight:700}
.sub{color:var(--ink-soft);font-size:16px;margin:0;max-width:70ch}
.stats{display:flex;flex-wrap:wrap;margin-top:26px;border:1px solid var(--rule);border-radius:10px;overflow:hidden}
.stat{flex:1 1 130px;padding:14px 18px;border-right:1px solid var(--rule)}
.stat:last-child{border-right:0}
.stat b{display:block;font-size:24px;font-weight:700;letter-spacing:-.02em;color:var(--roi)}
.stat span{font-size:12px;color:var(--ink-mute);text-transform:uppercase;letter-spacing:.04em}
h2{position:relative;font-size:13px;text-transform:uppercase;letter-spacing:.09em;color:var(--ink-mute);font-weight:600;margin:56px 0 6px;padding-top:8px}
h2+p.lede{margin:0 0 22px;color:var(--ink-soft);max-width:74ch}
.card{position:relative;border:1px solid var(--rule);border-radius:12px;padding:20px 22px;margin-bottom:14px;background:var(--surface);transition:border-color .15s}
.card:hover{border-color:#c9cfe4}
.card.done{background:var(--surface-alt);opacity:.62}
.chead{display:flex;align-items:flex-start;gap:13px}
.chead input[type=checkbox]{margin-top:4px;width:17px;height:17px;accent-color:var(--roi);flex:none;cursor:pointer}
.ctitle{font-weight:650;font-size:16.5px;letter-spacing:-.012em;flex:1}
.card.done .ctitle{text-decoration:line-through;text-decoration-color:var(--ink-mute)}
.tag{font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:3px 8px;border-radius:20px;white-space:nowrap;flex:none}
.t-now{background:#fdecE5;color:#b8451c}
.t-soon{background:#fdf3e0;color:#8a5c05}
.t-open{background:var(--surface-deep);color:var(--ink-soft)}
.t-ok{background:#e6f7f0;color:#0a7a55}
.body{margin:11px 0 0 30px;color:var(--ink-soft)}
.body p{margin:0 0 9px}
.body p:last-child{margin-bottom:0}
.body strong{color:var(--ink)}
.why{margin-top:11px;padding:11px 14px;background:var(--surface-alt);border-left:2px solid var(--turquoise);border-radius:0 6px 6px 0;font-size:14px}
.why b{color:var(--ink)}
.opts{margin-top:13px;display:flex;flex-wrap:wrap;gap:8px}
.opt{font-size:13.5px;padding:7px 13px;border:1px solid var(--rule);border-radius:20px;background:var(--surface);color:var(--ink-soft);cursor:pointer;font-family:inherit;transition:all .12s}
.opt:hover{border-color:var(--roi);color:var(--roi)}
.opt.pick{background:var(--roi);border-color:var(--roi);color:#fff;font-weight:600}
.src{margin-top:11px;font-size:12px;color:var(--ink-mute)}
.done-list{border:1px solid var(--rule);border-radius:12px;overflow:hidden}
.row{display:flex;gap:14px;padding:13px 18px;border-bottom:1px solid var(--rule);align-items:baseline}
.row:last-child{border-bottom:0}
.row:nth-child(odd){background:var(--surface-alt)}
.row .k{font-weight:600;flex:0 0 260px;font-size:14.5px}
.row .v{color:var(--ink-soft);font-size:14px;flex:1}
.badge{font-size:10px;font-weight:700;padding:2px 7px;border-radius:4px;background:#e6f7f0;color:#0a7a55;letter-spacing:.05em;flex:none}
.badge.new{background:#e8ecfb;color:var(--roi)}
code{background:var(--surface-deep);padding:1.5px 6px;border-radius:4px;font-size:13px;font-family:var(--mono)}
.foot{margin-top:64px;padding-top:22px;border-top:1px solid var(--rule);color:var(--ink-mute);font-size:13px}
.sig{margin-top:10px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-mute);opacity:.75}
/* Zone de commentaire, reprise du gabarit learn */
.cbtn{position:absolute;right:100%;top:20px;margin-right:12px;width:22px;height:22px;
  border-radius:50%;border:1px solid var(--rule);background:var(--surface);color:var(--ink-mute);
  font-family:var(--mono);font-size:13px;line-height:1;cursor:pointer;opacity:0;
  transition:.15s;display:grid;place-items:center}
.card:hover .cbtn,h2:hover .cbtn{opacity:1}
.cbtn:hover{border-color:var(--accent);color:var(--accent)}
.cbtn.has{opacity:1;background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
@media(max-width:1240px){.cbtn{right:auto;left:auto;position:static;opacity:1;margin:0 0 0 8px;display:inline-grid;vertical-align:middle}}
.fab{position:fixed;right:26px;bottom:26px;z-index:50;display:flex;align-items:center;gap:9px;
  padding:12px 18px;border-radius:999px;border:none;background:var(--ink);color:#fff;
  font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;
  font-weight:600;cursor:pointer;box-shadow:0 6px 22px rgba(15,20,85,.18)}
.fab .n{background:var(--accent);border-radius:999px;padding:1px 7px;font-size:11px}
.drawer{position:fixed;top:0;right:0;bottom:0;width:390px;max-width:92vw;z-index:60;
  background:var(--surface);border-left:1px solid var(--rule);display:flex;flex-direction:column;
  transform:translateX(100%);transition:transform .22s cubic-bezier(.2,.7,.1,1);
  box-shadow:-12px 0 40px rgba(15,20,85,.1)}
.drawer.open{transform:none}
.dr-head{padding:20px 22px;border-bottom:1px solid var(--rule);display:flex;align-items:center;justify-content:space-between}
.dr-head h3{font-size:19px;margin:0}
.dr-x{background:none;border:none;font-size:22px;color:var(--ink-mute);cursor:pointer;line-height:1}
.dr-body{flex:1;overflow-y:auto;padding:8px 22px 22px}
.dr-foot{padding:16px 22px;border-top:1px solid var(--rule);display:flex;gap:8px}
.dr-foot button{flex:1;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  font-weight:600;padding:10px;border-radius:6px;cursor:pointer;border:1px solid var(--rule);
  background:var(--surface);color:var(--ink-soft)}
.dr-foot button.primary{background:var(--ink);color:#fff;border-color:var(--ink)}
.cm-item{padding:14px 0;border-bottom:1px solid var(--rule)}
.cm-item:last-child{border:none}
.cm-sec{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent);font-weight:600;margin-bottom:5px}
.cm-tx{font-size:14.5px;color:var(--ink);white-space:pre-wrap;margin-bottom:6px}
.cm-del{background:none;border:none;font-family:var(--mono);font-size:10px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink-mute);cursor:pointer;padding:0}
.cm-del:hover{color:#c0392b}
.cm-empty{color:var(--ink-mute);font-size:14px;padding:22px 0}
.cm-new{margin-top:6px}
.cm-new textarea{width:100%;min-height:96px;padding:12px;border-radius:7px;border:1px solid var(--rule);
  background:var(--surface);color:var(--ink);font-family:inherit;font-size:14.5px;resize:vertical}
.cm-new textarea:focus{outline:none;border-color:var(--accent)}
.cm-new .lbl{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-mute);margin:14px 0 6px;font-weight:600}
#cm-export{width:100%;height:180px;margin-top:10px;display:none;font-family:var(--mono);
  font-size:11.5px;padding:11px;border-radius:7px;border:1px solid var(--rule);
  background:var(--surface);color:var(--ink)}
@media (max-width:1000px){
  .wrap{grid-template-columns:1fr;gap:0;padding:0 22px}
  nav{display:none}
  main{padding-top:26px}
  .row{flex-direction:column;gap:3px}
  .row .k{flex:none}
}
"""

JS = """
(function(){
  var RUN=document.body.dataset.run||location.pathname.split('/').pop();
  var KEY='lepoint:'+RUN;
  var st={};
  try{
    var raw=localStorage.getItem(KEY);
    // Migration douce : un rapport régénéré ne doit pas effacer les arbitrages
    // déjà posés sous une clé plus ancienne.
    if(raw===null){
      var old=localStorage.getItem('lepoint-'+RUN);
      if(old!==null){ raw=old; localStorage.setItem(KEY,old); }
    }
    st=JSON.parse(raw||'{}');
  }catch(e){ st={}; }
  function save(){ try{ localStorage.setItem(KEY,JSON.stringify(st)); }catch(e){} }

  var cards=[].slice.call(document.querySelectorAll('.card'));
  cards.forEach(function(card){
    var id=card.dataset.id, cb=card.querySelector('input[type=checkbox]'), s=st[id]||{};
    if(s.done){ cb.checked=true; card.classList.add('done'); }
    cb.addEventListener('change',function(){
      card.classList.toggle('done',cb.checked);
      st[id]=st[id]||{}; st[id].done=cb.checked; save(); count();
    });
    card.querySelectorAll('.opt').forEach(function(btn){
      if(s.opt===btn.textContent) btn.classList.add('pick');
      btn.addEventListener('click',function(){
        var on=btn.classList.contains('pick');
        card.querySelectorAll('.opt').forEach(function(b){b.classList.remove('pick')});
        st[id]=st[id]||{};
        if(on){ st[id].opt=null; } else { btn.classList.add('pick'); st[id].opt=btn.textContent; }
        save();
      });
    });
  });
  var out=document.getElementById('pcount');
  function count(){
    out.textContent=cards.filter(function(c){return c.classList.contains('done')}).length+'/'+cards.length;
  }
  count();

  var links=[].slice.call(document.querySelectorAll('nav a'));
  var secs=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))});
  function spy(){
    var y=window.scrollY+130,cur=0;
    secs.forEach(function(s,i){ if(s&&s.offsetTop<=y) cur=i; });
    links.forEach(function(a,i){ a.classList.toggle('on',i===cur); });
  }
  window.addEventListener('scroll',spy,{passive:true}); spy();

  /* ---- commentaires ---- */
  var CK=KEY+':cm';
  var cms=[]; try{ cms=JSON.parse(localStorage.getItem(CK)||'[]'); }catch(e){}
  var target='';

  function addBtn(el,label){
    var b=document.createElement('button');
    b.className='cbtn'; b.type='button'; b.textContent='+';
    b.title='Corriger ou commenter'; b.dataset.sec=label;
    b.onclick=function(e){ e.stopPropagation(); openDrawer(label); };
    el.appendChild(b);
  }
  document.querySelectorAll('main h2').forEach(function(h){ addBtn(h,h.textContent.trim()); });
  cards.forEach(function(c){
    var t=c.querySelector('.ctitle');
    addBtn(c,(c.dataset.id||'')+' · '+(t?t.textContent.trim():''));
  });

  var drawer=document.getElementById('cm-drawer');
  var input=document.getElementById('cm-input');
  var lbl=document.getElementById('cm-target');
  function openDrawer(sec){
    target=sec||'';
    lbl.textContent=target?('Sur : '+target):'Commentaire général';
    drawer.classList.add('open');
    setTimeout(function(){input.focus()},220);
  }
  function saveCm(){ try{ localStorage.setItem(CK,JSON.stringify(cms)); }catch(e){} renderCm(); }
  function renderCm(){
    var list=document.getElementById('cm-list');
    document.getElementById('cm-n').textContent=cms.length;
    list.innerHTML=cms.length?'':'<div class="cm-empty">Aucun retour. Survole une carte ou un titre, clique le « + », et corrige ce qui est faux.</div>';
    cms.forEach(function(c,i){
      var d=document.createElement('div'); d.className='cm-item';
      d.innerHTML='<div class="cm-sec"></div><div class="cm-tx"></div><button class="cm-del">Supprimer</button>';
      d.querySelector('.cm-sec').textContent=c.sec||'Général';
      d.querySelector('.cm-tx').textContent=c.tx;
      d.querySelector('.cm-del').onclick=function(){ cms.splice(i,1); saveCm(); };
      list.appendChild(d);
    });
    document.querySelectorAll('.cbtn').forEach(function(b){
      var n=cms.filter(function(c){return c.sec===b.dataset.sec}).length;
      b.classList.toggle('has',n>0);
      b.textContent=n>0?n:'+';
    });
  }
  document.getElementById('cm-fab').onclick=function(){ openDrawer(''); };
  document.getElementById('cm-close').onclick=function(){ drawer.classList.remove('open'); };
  document.getElementById('cm-add').onclick=function(){
    var tx=input.value.trim(); if(!tx) return;
    cms.push({sec:target,tx:tx}); input.value=''; saveCm();
  };
  input.addEventListener('keydown',function(e){
    if((e.metaKey||e.ctrlKey)&&e.key==='Enter') document.getElementById('cm-add').click();
  });
  document.getElementById('cm-copy').onclick=function(){
    var o=document.getElementById('cm-export');
    var picks=[];
    cards.forEach(function(c){
      var s=st[c.dataset.id]||{};
      if(s.opt) picks.push('- '+c.dataset.id+' · '+c.querySelector('.ctitle').textContent.trim()+' → **'+s.opt+'**');
    });
    o.value='# Retours — '+document.title+'\\n\\n'
      +'## Arbitrages choisis\\n'+(picks.length?picks.join('\\n'):'(aucun)')+'\\n\\n'
      +'## Corrections\\n'+(cms.length?cms.map(function(c){return '### '+(c.sec||'Général')+'\\n'+c.tx}).join('\\n\\n'):'(aucune)');
    o.style.display='block'; o.select();
    try{ document.execCommand('copy'); }catch(e){}
  };
  renderCm();
})();
"""


def esc(s: str) -> str:
    return html.escape(str(s), quote=False)


def card_html(c: dict) -> str:
    tag = ""
    if c.get("tag"):
        tag = f'<span class="tag {NIVEAUX.get(c.get("niveau","open"),"t-open")}">{esc(c["tag"])}</span>'
    corps = "".join(f"<p>{p}</p>" for p in c.get("corps", []))
    why = f'<div class="why">{c["why"]}</div>' if c.get("why") else ""
    opts = ""
    if c.get("options"):
        boutons = "".join(f'<button class="opt">{esc(o)}</button>' for o in c["options"])
        opts = f'<div class="opts">{boutons}</div>'
    src = f'<div class="src">{esc(c["src"])}</div>' if c.get("src") else ""
    return f"""
<div class="card" data-id="{esc(c['id'])}">
  <div class="chead">
    <input type="checkbox">
    <div class="ctitle">{esc(c['titre'])}</div>
    {tag}
  </div>
  <div class="body">{corps}{why}{opts}{src}</div>
</div>"""


def rows_html(rows: list[dict]) -> str:
    out = []
    for r in rows:
        b = "badge new" if r.get("etat") in ("créé", "cree") else "badge"
        out.append(
            f'<div class="row"><span class="{b}">{esc(r.get("etat","patché"))}</span>'
            f'<span class="k">{esc(r["quoi"])}</span>'
            f'<span class="v">{esc(r.get("detail",""))}</span></div>'
        )
    return f'<div class="done-list">{"".join(out)}</div>'


def render(f: dict) -> str:
    nav, body = [], []
    for s in f["sections"]:
        nav.append(f'<a href="#{esc(s["id"])}">{esc(s["nav"])}</a>')
        body.append(f'<h2 id="{esc(s["id"])}">{esc(s["titre"])}</h2>')
        if s.get("lede"):
            body.append(f'<p class="lede">{esc(s["lede"])}</p>')
        if s.get("rows"):
            body.append(rows_html(s["rows"]))
        for c in s.get("cartes", []):
            body.append(card_html(c))

    stats = "".join(
        f'<div class="stat"><b>{esc(s["n"])}</b><span>{esc(s["l"])}</span></div>'
        for s in f.get("stats", [])
    )
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(f['titre'])}</title>
<style>{CSS}</style>
</head>
<body data-run="{esc(f.get('run', f['periode']))}">
<div class="wrap">
<nav>
  <div class="brand">Le Point</div>
  <div class="date">{esc(f['periode'])}</div>
  {''.join(nav)}
  <div class="prog"><b id="pcount">0/0</b>tranché</div>
</nav>
<main>
<header class="top">
  <h1>{esc(f['h1'])}</h1>
  <p class="sub">{f['chapo']}</p>
  <div class="stats">{stats}</div>
</header>
{''.join(body)}
<div class="foot">{f.get('foot','')}
  <div class="sig">Le Point, une recette M:armites.ai</div>
</div>
</main>
</div>

<button class="fab" id="cm-fab">Corriger <span class="n" id="cm-n">0</span></button>
<div class="drawer" id="cm-drawer">
  <div class="dr-head"><h3>Tes corrections</h3><button class="dr-x" id="cm-close">×</button></div>
  <div class="dr-body">
    <div id="cm-list"></div>
    <div class="cm-new">
      <div class="lbl" id="cm-target">Commentaire général</div>
      <textarea id="cm-input" placeholder="Ce qui est faux, ce qui manque, ce que j'ai mal lu…"></textarea>
    </div>
    <textarea id="cm-export" readonly></textarea>
  </div>
  <div class="dr-foot">
    <button id="cm-copy">Exporter</button>
    <button class="primary" id="cm-add">Ajouter</button>
  </div>
</div>
<script>{JS}</script>
</body>
</html>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()
    data = json.loads(Path(a.input).read_text(encoding="utf-8"))
    Path(a.output).write_text(render(data), encoding="utf-8")
    n = sum(len(s.get("cartes", [])) for s in data["sections"])
    print(json.dumps({"output": a.output, "cartes": n}, ensure_ascii=False))


if __name__ == "__main__":
    main()
