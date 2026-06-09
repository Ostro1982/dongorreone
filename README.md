# El Club de la Gorra

Tienda minorista de gorras. Catálogo espejado de gorrasdelparaiso (mayorista), con stock real y precio propio. Venta por WhatsApp.

## Cómo funciona

1. `scrape.py` — baja el catálogo completo de gorrasdelparaiso (nombre, precio proveedor, **stock real**, imagen, categoría) parseando el HTML estático.
2. `gen_site.py` — genera `index.html` estático (self-contained) desde `catalog.json`, aplicando el markup propio.
3. GitHub Actions (`.github/workflows/scrape-deploy.yml`) corre los dos scripts **todos los días 06:00 ART** y publica en GitHub Pages.

## Editar config

En `gen_site.py`, arriba de todo:

- `BRAND` — nombre de la marca
- `WA_NUMERO` — WhatsApp de ventas (sin +)
- `MARKUP` — multiplicador sobre el precio del proveedor (1.00 = mismo precio). Definir con el proveedor.

## Correr local

```
python scrape.py 0      # 0 = catálogo completo; o un número para muestra (ej. 40)
python gen_site.py      # genera index.html
```

## Notas

- Stock real viene embebido en el HTML de cada producto (`var stock=[{s_cantidad}]`). No requiere Playwright ni API.
- El scraper tiene guard: si una corrida trae <200 productos (IP bloqueado), conserva el catálogo previo.
- Pago: transferencia / MercadoPago / QR. Despacho: proveedor.
