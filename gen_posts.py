#!/usr/bin/env python3
# Genera posts 1080x1080 para IG/TikTok desde catalog.json.
# Cada post = 1 archivo HTML (post_N.html). Render a PNG con Playwright aparte.
import json, os, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
MARKUP = float(os.environ.get("MARKUP", "1.0"))
WA = "5491123994487"
HANDLE = "@elclubdelagorra.ar"

prods = json.load(open(os.path.join(HERE, "catalog.json"), encoding="utf-8"))
for p in prods:
    p["precio"] = round((p.get("precio_proveedor") or 0) * MARKUP / 100) * 100

def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", (s or "").lower()) if unicodedata.category(c) != "Mn")

_used = set()
def pick(term, low_stock=False):
    t = norm(term)
    cand = [p for p in prods if p["stock_disponible"] and p["url"] not in _used
            and t in norm(p["nombre"] + " " + " ".join(p.get("categorias", [])))]
    if low_stock:
        cand = [p for p in cand if not p["stock_ilimitado"] and p["stock_cantidad"] <= 5]
    if not cand:
        return None
    _used.add(cand[0]["url"])
    return cand[0]

def fmt(n):
    return "$" + format(n or 0, ",d").replace(",", ".")

TEMPLATE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1080px;height:1080px;overflow:hidden}
  .post{width:1080px;height:1080px;background:#ece5d6;position:relative;font-family:'Archivo',sans-serif;padding:46px}
  .post::before{content:"";position:absolute;inset:0;opacity:.05;mix-blend-mode:multiply;pointer-events:none;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
  .frame{position:absolute;inset:24px;border:3px solid #16130d;pointer-events:none}
  .top{display:flex;justify-content:space-between;align-items:center;position:relative;z-index:2}
  .mark{width:60px;height:60px;border-radius:50%;background:#d3262f;color:#ece5d6;display:grid;place-items:center;font-family:'Anton';font-size:26px;transform:rotate(-4deg);border:3px solid #16130d}
  .handle{font-family:'Space Mono',monospace;font-weight:700;font-size:22px;letter-spacing:1px;color:#16130d}
  .eyebrow{font-family:'Anton';font-size:54px;color:#d3262f;text-transform:uppercase;letter-spacing:1px;margin-top:30px;line-height:.95;position:relative;z-index:2}
  .imgbox{margin:24px 0;height:560px;border:3px solid #16130d;background:#f3eee2;display:grid;place-items:center;overflow:hidden;position:relative;z-index:2;box-shadow:10px 10px 0 #16130d;padding:28px}
  .imgbox img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;mix-blend-mode:multiply}
  .badge{position:absolute;top:18px;left:18px;background:#d3262f;color:#fff;font-family:'Anton';font-size:30px;padding:6px 18px;transform:rotate(-6deg);border:3px solid #16130d;z-index:3}
  .name{font-family:'Anton';font-size:46px;color:#16130d;text-transform:uppercase;line-height:.95;position:relative;z-index:2}
  .bottom{position:absolute;left:46px;right:46px;bottom:46px;display:flex;justify-content:space-between;align-items:flex-end;z-index:2}
  .price{font-family:'Anton';font-size:96px;color:#d3262f;line-height:.85}
  .price small{display:block;font-family:'Space Mono',monospace;font-weight:700;font-size:18px;color:#16130d;letter-spacing:2px;margin-bottom:4px}
  .cta{text-align:right}
  .cta .l1{font-family:'Anton';font-size:30px;color:#16130d;text-transform:uppercase;line-height:1}
  .cta .l2{font-family:'Space Mono',monospace;font-weight:700;font-size:20px;color:#16130d;margin-top:6px}
  .cta .wa{background:#16130d;color:#ece5d6;font-family:'Space Mono',monospace;font-weight:700;font-size:18px;padding:8px 14px;display:inline-block;margin-top:8px;letter-spacing:1px}
</style></head><body>
<div class="post">
  <div class="frame"></div>
  <div class="top"><div class="mark">CG</div><div class="handle">__HANDLE__</div></div>
  <div class="eyebrow">__EYEBROW__</div>
  <div class="imgbox">__BADGE__<img src="__IMG__" alt=""></div>
  <div class="name">__NAME__</div>
  <div class="bottom">
    <div class="price"><small>PRECIO</small>__PRICE__</div>
    <div class="cta"><div class="l1">Pedila por</div><div class="wa">WhatsApp __WA__</div><div class="l2">El Club de la Gorra · De la cabeza</div></div>
  </div>
</div>
</body></html>"""

def make(p, eyebrow, badge=""):
    return (TEMPLATE
        .replace("__HANDLE__", HANDLE)
        .replace("__EYEBROW__", eyebrow)
        .replace("__BADGE__", f'<div class="badge">{badge}</div>' if badge else "")
        .replace("__IMG__", p["imagen"] or "")
        .replace("__NAME__", p["nombre"][:42])
        .replace("__PRICE__", fmt(p["precio"]))
        .replace("__WA__", "11 2399-4487"))

# selección de posts (variados)
posts = []
afa = pick("afa")
if afa: posts.append(make(afa, "Gorra del día", "MUNDIAL"))
boca = pick("boca")
if boca: posts.append(make(boca, "Recién llegadas"))
low = pick("", low_stock=True) or pick("nba", low_stock=True)
if low: posts.append(make(low, "Últimas unidades", f"ÚLTIMAS {low['stock_cantidad']}"))
gorro = pick("gorro") or pick("invierno")
if gorro: posts.append(make(gorro, "Para el frío"))

os.makedirs(os.path.join(HERE, "posts"), exist_ok=True)
for i, html in enumerate(posts, 1):
    open(os.path.join(HERE, "posts", f"post_{i}.html"), "w", encoding="utf-8").write(html)
print(f"{len(posts)} posts generados en posts/")
