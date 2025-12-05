# Codex â€“ IntegraciÃ³n con la API de Dux (La Mascotera)

## Base y autenticaciÃ³n
- Base URL: `https://erp.duxsoftware.com.ar/WSERP/rest/services/`
- Header obligatorio: `authorization: <token>` (sin prefijo `Bearer`)
- Header recomendado: `accept: application/json`

Ejemplo rÃ¡pido en Python:
```python
import requests

TOKEN = "KElzF9CLfChHh1EUe8zSjxXIliIl4SX5zIVgRANfOC8oF5d17PlulQNwP77qF3gV"
BASE = "https://erp.duxsoftware.com.ar/WSERP/rest/services"

resp = requests.get(
    f"{BASE}/deposito",
    headers={
        "accept": "application/json",
        "authorization": TOKEN,
    },
    timeout=30,
)
resp.raise_for_status()
print(resp.json())
```

## Endpoints verificados

### DepÃ³sitos
- GET `/deposito`
- Devuelve listado de depÃ³sitos de la empresa.

### Facturas de venta
- GET `/facturas`
- ParÃ¡metros usados (query):
  - `idEmpresa` (int, requerido)
  - `idSucursal` (int, requerido)
  - `fechaDesde` (yyyy-MM-dd)
  - `fechaHasta` (yyyy-MM-dd)
  - `limit` (por defecto 20, mÃ¡x 50)
  - `offset` (por defecto 0)
- Ejemplo que devuelve resultados:
```
https://erp.duxsoftware.com.ar/WSERP/rest/services/facturas\
  idEmpresa=9425\
  &idSucursal=3\
  &fechaDesde=2025-09-01\
  &fechaHasta=2025-09-15\
  &limit=50\
  &offset=0
```

### Compras
- GET `/compras`
- Requiere rango de fechas (`fechaDesde`, `fechaHasta`) y posiblemente `idEmpresa`/`idSucursal` (el servicio devuelve mensaje de error si faltan fechas).

### Otros GET disponibles (listados)
- `/empresas`
- `/items`
- `/listaprecioventa`
- `/localidades`
- `/pedidos`
- `/percepcionesImpuestos`
- `/personales`
- `/provincias`
- `/rubros`
- `/subrubros`
- `/sucursales`
- `/obtenerEstadoFactura`
- `/obtenerEstadoItem`

## Ejemplos de respuesta (resumidos)
- `facturas` devuelve `paging` y `results` con campos como:
  - `tipo_comp`, `letra_comp`, `nro_pto_vta`, `nro_comp`, `fecha_comp`, `total`
  - `cliente`, `detalles` (items), `detalles_cobro`
  - `url_factura` (enlace PDF con token propio)

## Notas
- El servicio aplica rate limit (â€œHas alcanzado el lÃ­mite de frecuenciaâ€¦â€). Si ocurre, espera al menos 10â€“15 segundos antes de repetir.
- Los parÃ¡metros distinguen mayÃºsculas/minÃºsculas (`idEmpresa`, `fechaDesde`, etc.).

## Script de apoyo
- Archivo: dux_api_examples.py
- Uso:
  1) Define DUX_TOKEN en tu entorno con el token de Dux.
  2) Importa funciones como get_depositos(), get_facturas(params), get_compras(params), etc.
  3) Si quieres correr la demo, descomenta la línea demo() en el __main__ del script.
  4) Respeta el rate limit (el demo incluye un sleep entre llamadas).

## Catálogo de productos (Libro1.xlsx)
- Productos estrella: todos los de marca "PETS PLUS..." (107 ítems en el XLSX).
- SENDA AD X20KG: código `77700001`.
- JASPE ≥ 3kg (10 ítems encontrados, ejemplos):
  - 900906 JASPE CACHORRO RP X 15 KG
  - 900905 JASPE CACHORRO RM/G X 15 KG
  - 900908 JASPE ADULTO X 20 KG
  - 900910 JASPE ADULTO RP X 20 KG
  - 900919 JASPE PREMIUM CRIADORES X 20 KG
  - 900911 JASPE ADULTO RP 2X10 KG
  - 900907 JASPE ADULTO RM X 15 KG
  - 900909 JASPE ADULTO X 3 KG
  - 900920 JASPE BALANCED X 20 KG
  - 900912 JASPE ADULTO LARGE BREED X 20 KG
