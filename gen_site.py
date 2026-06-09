#!/usr/bin/env python3
# Genera index.html estatico (self-contained) desde catalog.json.
# Estetica: club deportivo / socio + calle BA, print editorial.
# Deploy: subir index.html a Cloudflare Pages (gratis). Sin build, sin backend.
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

# ===== CONFIG (editar aca) =====
BRAND = "El Club de la Gorra"
WA_NUMERO = "5491123994487"              # WhatsApp ventas (bot)
MARKUP = 1.00                            # multiplicador sobre precio proveedor. Definir con hermano.
# ================================

prods = json.load(open(os.path.join(HERE, "catalog.json"), encoding="utf-8"))
try:
    UPDATED = open(os.path.join(HERE, "last_scrape.txt"), encoding="utf-8").read().strip()
except FileNotFoundError:
    UPDATED = "—"

def precio_final(p):
    base = p.get("precio_proveedor") or 0
    return int(round(base * MARKUP / 100.0) * 100)

def categorize(p):
    s = (" ".join(p.get("categorias", [])) + " " + p.get("nombre", "")).lower()
    reglas = [
        ("Fútbol",      ["afa","boca","river","futbol","seleccion","argentina","independiente","racing","san lorenzo","messi","equipos"]),
        ("NBA",         ["nba","basket","chicago","bulls","lakers","jordan","celtics","knicks"]),
        ("Autos",       ["auto","audi","bmw","ferrari","mercedes","ford","volkswagen","fiat","peugeot","renault","toyota","porsche"]),
        ("Motos",       ["moto","harley","ducati","yamaha","honda","kawasaki","ktm","suzuki"]),
        ("Personajes",  ["naruto","spider","venom","anime","mickey","cars","pokemon","dragon","goku","bob esponja","minnie","disney","marvel","one piece"]),
        ("Marcas",      ["nike","adidas","new era","ny","lacoste","red bull","redbull","caterpillar","puma","jordan","quiksilver"]),
        ("Invierno",    ["gorro","cuello","guante","piluso","rocky","tejido","pompon","polar","invierno","bufanda"]),
        ("Lisas",       ["lisa","plana","vintage","trucker","gabardina","ciclista","cerrada","bordado"]),
    ]
    for nombre, kws in reglas:
        if any(k in s for k in kws):
            return nombre
    return "Otras"

for p in prods:
    p["precio"] = precio_final(p)
    p["categoria_principal"] = categorize(p)
prods.sort(key=lambda p: (not p["stock_disponible"], p["nombre"].lower()))
cats = sorted({p["categoria_principal"] for p in prods})
DATA = json.dumps(prods, ensure_ascii=False)

HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__BRAND__ — Gorras, gorros y accesorios</title>
<meta name="description" content="El Club de la Gorra. Gorras, gorros y accesorios. Stock real, envíos a todo el país.">
<link rel="icon" href="logo_1080.png">
<meta property="og:title" content="El Club de la Gorra">
<meta property="og:description" content="Gorras, gorros y accesorios. Stock real, envíos a todo el país.">
<meta property="og:image" content="logo_1080.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Archivo:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#ece5d6; --paper2:#e2d9c5; --card:#f6f1e6;
    --ink:#16130d; --ink2:#4a4336; --mut:#7a7263;
    --red:#d3262f; --gold:#b07f2e; --green:#1d6b3a;
    --line:#16130d;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{
    background:var(--paper);color:var(--ink);
    font-family:'Archivo',system-ui,sans-serif;font-size:15px;line-height:1.45;
    -webkit-font-smoothing:antialiased;overflow-x:hidden;
  }
  /* grano */
  body::before{
    content:"";position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.05;mix-blend-mode:multiply;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  }
  .mono{font-family:'Space Mono',monospace}
  /* ticker */
  .ticker{background:var(--ink);color:var(--paper);overflow:hidden;border-bottom:2px solid var(--ink);position:relative;z-index:5}
  .ticker .run{display:inline-flex;white-space:nowrap;animation:scroll 28s linear infinite;padding:7px 0;font-family:'Space Mono',monospace;font-size:12px;letter-spacing:1px;text-transform:uppercase}
  .ticker .run span{padding:0 22px}
  .ticker .run span b{color:var(--red)}
  @keyframes scroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
  /* header */
  header{position:sticky;top:0;z-index:20;background:var(--paper);border-bottom:2px solid var(--ink)}
  .hwrap{max-width:1240px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}
  .crest{display:flex;align-items:center;gap:11px;text-decoration:none;color:var(--ink)}
  .mark{width:42px;height:42px;border:2px solid var(--ink);border-radius:50%;display:grid;place-items:center;font-family:'Anton';font-size:18px;background:var(--red);color:var(--paper);transform:rotate(-4deg);flex:none}
  .brand{line-height:.95}
  .brand .t{font-family:'Anton';font-size:21px;letter-spacing:.5px;text-transform:uppercase}
  .brand .t em{font-style:normal;color:var(--red)}
  .brand .s{font-family:'Space Mono',monospace;font-size:9.5px;letter-spacing:3px;color:var(--mut);text-transform:uppercase}
  .search{flex:1;min-width:200px;position:relative}
  .search input{width:100%;background:var(--card);border:2px solid var(--ink);color:var(--ink);padding:11px 14px 11px 38px;font-size:14px;font-family:'Archivo';outline:none;border-radius:0}
  .search input::placeholder{color:var(--mut)}
  .search input:focus{box-shadow:4px 4px 0 var(--ink)}
  .search svg{position:absolute;left:12px;top:50%;transform:translateY(-50%);width:17px;height:17px;stroke:var(--ink)}
  /* hero */
  .hero{max-width:1240px;margin:0 auto;padding:34px 20px 22px;position:relative;z-index:2;display:flex;gap:34px;align-items:center}
  .herotext{flex:1;min-width:0}
  .herologo{width:240px;flex:none;border:3px solid var(--ink);box-shadow:8px 8px 0 var(--ink);display:block}
  .hero h1{font-family:'Anton';font-size:clamp(42px,9vw,104px);line-height:.86;text-transform:uppercase;letter-spacing:-1px}
  .hero h1 .red{color:var(--red);-webkit-text-stroke:0}
  .hero h1 .out{color:transparent;-webkit-text-stroke:2px var(--ink)}
  .hero h1.red{color:var(--red)}
  .brandline{font-family:'Space Mono',monospace;font-weight:700;font-size:clamp(14px,2vw,20px);letter-spacing:4px;text-transform:uppercase;color:var(--red);margin-top:14px;line-height:1}
  .hero .lead{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap;margin-top:18px;border-top:2px solid var(--ink);padding-top:14px}
  .hero .lead p{max-width:440px;font-size:15px;color:var(--ink2)}
  .stats{display:flex;gap:26px}
  .stat .n{font-family:'Anton';font-size:30px;line-height:1}
  .stat .l{font-family:'Space Mono',monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--mut)}
  /* cats */
  .catbar{position:sticky;top:67px;z-index:15;background:var(--paper2);border-top:2px solid var(--ink);border-bottom:2px solid var(--ink)}
  .cats{max-width:1240px;margin:0 auto;padding:10px 20px;display:flex;gap:9px;overflow-x:auto}
  .cats::-webkit-scrollbar{height:0}
  .cats button{white-space:nowrap;background:transparent;border:2px solid var(--ink);color:var(--ink);padding:7px 16px;cursor:pointer;font-family:'Space Mono',monospace;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;transition:.12s}
  .cats button:hover{background:var(--ink);color:var(--paper)}
  .cats button.on{background:var(--red);color:var(--paper);border-color:var(--red)}
  /* grid */
  main{max-width:1240px;margin:0 auto;padding:22px 20px 10px;position:relative;z-index:2}
  .count{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--mut);margin-bottom:16px}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(218px,1fr));gap:18px}
  .card{background:var(--card);border:2px solid var(--ink);display:flex;flex-direction:column;position:relative;transition:transform .14s,box-shadow .14s;opacity:0;transform:translateY(14px);animation:rise .5s forwards}
  @keyframes rise{to{opacity:1;transform:translateY(0)}}
  .card:hover{transform:translate(-3px,-3px);box-shadow:7px 7px 0 var(--ink)}
  .ph{aspect-ratio:1;position:relative;overflow:hidden;border-bottom:2px solid var(--ink);background:var(--paper2)}
  .ph img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s;mix-blend-mode:multiply}
  .card:hover .ph img{transform:scale(1.05)}
  .num{position:absolute;top:7px;right:9px;font-family:'Space Mono',monospace;font-size:10px;color:var(--mut);letter-spacing:1px}
  /* sello sin stock */
  .stamp{position:absolute;inset:0;display:grid;place-items:center;pointer-events:none}
  .stamp span{font-family:'Anton';font-size:26px;letter-spacing:2px;color:var(--red);border:3px solid var(--red);padding:5px 14px;transform:rotate(-11deg);opacity:.82;text-transform:uppercase;background:rgba(246,241,230,.35)}
  .tag{position:absolute;top:9px;left:0;background:var(--gold);color:var(--ink);font-family:'Space Mono',monospace;font-size:10px;font-weight:700;letter-spacing:.5px;padding:4px 10px;text-transform:uppercase;border:2px solid var(--ink);border-left:0}
  .info{padding:12px 13px 14px;display:flex;flex-direction:column;gap:9px;flex:1}
  .cat{font-family:'Space Mono',monospace;font-size:9.5px;letter-spacing:1.5px;text-transform:uppercase;color:var(--red)}
  .nm{font-family:'Archivo';font-weight:700;font-size:14px;line-height:1.22;text-transform:uppercase;min-height:34px}
  .row{display:flex;align-items:baseline;justify-content:space-between;gap:8px;border-top:1.5px dashed var(--ink);padding-top:9px;margin-top:2px}
  .pr{font-family:'Anton';font-size:25px;line-height:1}
  .st{font-family:'Space Mono',monospace;font-size:10px;color:var(--mut);text-transform:uppercase;text-align:right}
  .st.ok{color:var(--green)}
  .buy{margin-top:auto;background:var(--ink);color:var(--paper);border:2px solid var(--ink);padding:11px;font-family:'Space Mono',monospace;font-weight:700;font-size:12.5px;letter-spacing:1px;text-transform:uppercase;cursor:pointer;text-decoration:none;text-align:center;display:flex;align-items:center;justify-content:center;gap:8px;transition:.12s}
  .buy:hover{background:var(--red);border-color:var(--red)}
  .buy svg{width:15px;height:15px;fill:currentColor}
  .buy.dis{background:transparent;color:var(--mut);border-color:var(--mut);cursor:not-allowed;pointer-events:none}
  /* footer */
  footer{border-top:2px solid var(--ink);background:var(--ink);color:var(--paper);margin-top:34px;position:relative;z-index:2}
  .fwrap{max-width:1240px;margin:0 auto;padding:30px 20px;display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:center}
  .fwrap .fb{font-family:'Anton';font-size:28px;text-transform:uppercase}
  .fwrap .fb em{font-style:normal;color:var(--red)}
  .fwrap .pay{font-family:'Space Mono',monospace;font-size:11px;letter-spacing:1px;color:var(--paper);text-transform:uppercase;text-align:right;line-height:1.9}
  .proto{background:var(--gold);color:var(--ink);font-family:'Space Mono',monospace;font-size:11px;text-align:center;padding:6px;letter-spacing:.5px;position:relative;z-index:2;border-bottom:2px solid var(--ink)}
  @media(max-width:760px){.hero{flex-direction:column-reverse;gap:20px}.herologo{width:200px}}
  @media(max-width:560px){.hero .lead{flex-direction:column;align-items:flex-start}.catbar{top:64px}}
</style>
</head>
<body>
<div class="ticker"><div class="run" id="run"></div></div>
<header>
  <div class="hwrap">
    <a class="crest" href="#top">
      <div class="mark">CG</div>
      <div class="brand"><div class="t">El Club de la <em>Gorra</em></div><div class="s">De la cabeza · Buenos Aires</div></div>
    </a>
    <div class="search">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
      <input id="q" placeholder="Buscar club, marca, modelo..." autocomplete="off">
    </div>
  </div>
</header>
<div class="proto">__N__ modelos · stock actualizado a diario · consultá precio y envío por WhatsApp</div>
<section class="hero" id="top">
  <div class="herotext">
  <h1>EL CLUB DE LA<br><span class="red">GORRA.</span></h1>
  <div class="brandline">De la cabeza</div>
  <div class="lead">
    <p>Catálogo completo de gorras, gorros y accesorios. Modelos de fútbol, autos, motos, NBA y más. Stock real, sin vueltas — lo pedís por WhatsApp y listo.</p>
    <div class="stats">
      <div class="stat"><div class="n" id="s-tot">0</div><div class="l">Modelos</div></div>
      <div class="stat"><div class="n" id="s-stk">0</div><div class="l">Con stock</div></div>
    </div>
  </div>
  </div>
  <img class="herologo" src="logo_1080.png" alt="El Club de la Gorra" width="240" height="240">
</section>
<div class="catbar"><div class="cats" id="cats"></div></div>
<main>
  <p class="count" id="count"></p>
  <div class="grid" id="grid"></div>
</main>
<footer>
  <div class="fwrap">
    <div class="fb">El Club de la <em>Gorra</em></div>
    <div class="pay">Transferencia · MercadoPago · QR<br>Envíos a todo el país · Retiro en CABA<br>WhatsApp +54 9 11 2399-4487<br><span style="color:#b07f2e">Catálogo actualizado: __UPDATED__ ART</span></div>
  </div>
</footer>
<script>
const WA="__WA__", BRAND="__BRAND__";
const P=__DATA__;
let cat="todos", q="";
const $=s=>document.querySelector(s);
const fmt=n=>"$"+(n||0).toLocaleString("es-AR");
const cap=s=>s[0].toUpperCase()+s.slice(1);

// ticker
const tk=["Envíos a todo el país","Pagá con MercadoPago","<b>Stock real</b> actualizado","Gorras · Gorros · Cuellos","Pedí por WhatsApp","<b>Club de la Gorra</b>"];
$("#run").innerHTML=(tk.map(t=>`<span>★ ${t}</span>`).join("")).repeat(2);

// stats
$("#s-tot").textContent=P.length;
$("#s-stk").textContent=P.filter(p=>p.stock_disponible).length;

function cats(){
  const cs=["todos",...[...new Set(P.map(p=>p.categoria_principal))].sort()];
  $("#cats").innerHTML=cs.map(c=>`<button data-c="${c}" class="${c==cat?'on':''}">${cap(c)}</button>`).join("");
  $("#cats").onclick=e=>{const b=e.target.closest("button");if(!b)return;cat=b.dataset.c;render();};
}
function waLink(p){
  const msg=`Hola Club de la Gorra! Me interesa: ${p.nombre} (${fmt(p.precio)}). ${p.url}`;
  return `https://wa.me/${WA}?text=${encodeURIComponent(msg)}`;
}
const WAICON='<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 00-8.6 15l-1.3 4.7 4.8-1.3A10 10 0 1012 2zm0 1.8a8.2 8.2 0 11-4.2 15.2l-.3-.2-2.8.7.8-2.7-.2-.3A8.2 8.2 0 0112 3.8zm4.7 10.3c-.3-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 01-2-1.2 7.4 7.4 0 01-1.3-1.7c-.2-.3 0-.4.1-.6l.4-.4.3-.5v-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.7 11.8 11.8 0 004.5 4 5.3 5.3 0 002.4.5 2 2 0 001.4-.9 1.7 1.7 0 00.1-1l-.4-.3z"/></svg>';

function render(){
  cats();
  const f=P.filter(p=>(cat==="todos"||p.categoria_principal===cat)&&(!q||p.nombre.toLowerCase().includes(q)));
  $("#count").textContent=`${f.length} producto${f.length!=1?"s":""}${cat!=="todos"?" · "+cap(cat):""}`;
  $("#grid").innerHTML=f.map((p,i)=>{
    const off=!p.stock_disponible;
    const low=!off&&!p.stock_ilimitado&&p.stock_cantidad<=3;
    const stamp=off?`<div class="stamp"><span>Sin Stock</span></div>`:"";
    const tag=low?`<div class="tag">Últimas ${p.stock_cantidad}</div>`:"";
    const st=off?`<span class="st">Agotado</span>`:(p.stock_ilimitado?`<span class="st ok">Disponible</span>`:`<span class="st ok">${p.stock_cantidad} u.</span>`);
    const img=p.imagen?`<img loading="lazy" src="${p.imagen}" alt="${p.nombre}">`:"";
    const buy=off?`<span class="buy dis">Sin stock</span>`:`<a class="buy" target="_blank" rel="noopener" href="${waLink(p)}">${WAICON} Pedir</a>`;
    const cn=(p.categorias&&p.categorias.length>2)?p.categorias.slice(-2).join(" / "):p.categoria_principal;
    return `<article class="card" style="animation-delay:${Math.min(i*28,420)}ms">
      <div class="ph">${img}${stamp}${tag}<span class="num mono">N°${String(i+1).padStart(3,"0")}</span></div>
      <div class="info">
        <div class="cat">${cn}</div>
        <div class="nm">${p.nombre}</div>
        <div class="row"><div class="pr">${fmt(p.precio)}</div>${st}</div>
        ${buy}
      </div>
    </article>`;
  }).join("");
}
$("#q").oninput=e=>{q=e.target.value.toLowerCase().trim();render();};
render();
</script>
</body>
</html>"""

out = (HTML
  .replace("__BRAND__", BRAND)
  .replace("__WA__", WA_NUMERO)
  .replace("__N__", str(len(prods)))
  .replace("__UPDATED__", UPDATED)
  .replace("__DATA__", DATA))
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print(f"index.html generado: {len(prods)} productos, {len(cats)} categorias")
