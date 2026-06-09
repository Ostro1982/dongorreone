#!/usr/bin/env python3
# Scraper gorrasdelparaiso.empretienda.com.ar
# Extrae nombre, precio (retail proveedor), stock real, imagen, categoria desde HTML estatico.
# Stock embebido en: var s_producto / var stock = [{s_cantidad, s_ilimitado, ...}]
import re, json, time, sys, os, urllib.request, gzip, io
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "catalog.json")
STAMP = os.path.join(HERE, "last_scrape.txt")
ART = timezone(timedelta(hours=-3))
BASE = "https://gorrasdelparaiso.empretienda.com.ar"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 40   # 0 = full
SLEEP = 0.8

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
        return data.decode("utf-8", "replace")

def product_urls():
    xml = get(f"{BASE}/sitemap.xml")
    locs = re.findall(r"<loc>(.*?)</loc>", xml)
    # producto = path con >=5 segmentos (categorias tienen menos)
    out = []
    for u in locs:
        path = u.replace(BASE, "").strip("/")
        segs = [s for s in path.split("/") if s]
        if len(segs) >= 5:
            out.append(u)
    return out

def parse(url, html):
    def jvar(name):
        m = re.search(name + r"\s*=\s*(\{.*?\}|\[.*?\]);", html, re.S)
        return m.group(1) if m else None
    nombre = re.search(r'var p_nombre\s*=\s*"(.*?)";', html)
    nombre = nombre.group(1) if nombre else None
    sp = jvar(r"var s_producto")
    st = jvar(r"var stock")
    img = re.search(r'var i_link_principal\s*=\s*"(.*?)";', html)
    if not (nombre and sp):
        return None
    try:
        sp = json.loads(sp)
        st = json.loads(st) if st else []
    except Exception:
        return None
    # stock total
    ilimitado = any(int(x.get("s_ilimitado", 0)) == 1 for x in st)
    qty = sum(int(x.get("s_cantidad", 0)) for x in st)
    disponible = bool(sp.get("stock")) and (ilimitado or qty > 0)
    # categoria desde URL
    segs = [s for s in url.replace(BASE, "").strip("/").split("/") if s]
    cats = segs[:-1]  # ultimo = slug producto
    return {
        "url": url,
        "nombre": nombre,
        "precio_proveedor": sp.get("precio"),
        "stock_disponible": disponible,
        "stock_cantidad": (None if ilimitado else qty),
        "stock_ilimitado": ilimitado,
        "imagen": img.group(1) if img else None,
        "categorias": cats,
        "categoria_principal": cats[2] if len(cats) > 2 else (cats[-1] if cats else "otros"),
    }

def main():
    urls = product_urls()
    print(f"[sitemap] {len(urls)} URLs candidatas a producto", file=sys.stderr)
    if LIMIT:
        stride = max(1, len(urls) // LIMIT)
        urls = urls[::stride][:LIMIT]
        print(f"[sample] tomando {len(urls)} (stride {stride})", file=sys.stderr)
    prods, ok, fail = [], 0, 0
    for i, u in enumerate(urls, 1):
        try:
            p = parse(u, get(u))
            if p:
                prods.append(p); ok += 1
                print(f"  {i}/{len(urls)} OK  {p['nombre'][:30]:30} ${p['precio_proveedor']} stock={p['stock_cantidad'] if not p['stock_ilimitado'] else 'inf'}", file=sys.stderr)
            else:
                fail += 1
        except Exception as e:
            fail += 1
            print(f"  {i}/{len(urls)} ERR {u[-40:]} {e}", file=sys.stderr)
        time.sleep(SLEEP)
    # guard: si la corrida trae muy poco (IP bloqueado), no pisar catalogo bueno previo
    MIN_OK = 200
    if ok < MIN_OK and os.path.exists(OUT):
        prev = json.load(open(OUT, encoding="utf-8"))
        if len(prev) > ok:
            print(f"\n[guard] solo {ok} productos (<{MIN_OK}). Conservo catalogo previo ({len(prev)}). No piso.", file=sys.stderr)
            return
    json.dump(prods, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(STAMP, "w", encoding="utf-8").write(datetime.now(ART).strftime("%Y-%m-%d %H:%M"))
    print(f"\n[done] {ok} productos, {fail} fallos -> catalog.json + last_scrape.txt", file=sys.stderr)

if __name__ == "__main__":
    main()
