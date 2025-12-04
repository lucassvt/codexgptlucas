# Codex – Integración con la API de Dux (La Mascotera)

## Base y autenticación
- Base URL: `https://erp.duxsoftware.com.ar/WSERP/rest/services/`
- Header obligatorio: `authorization: <token>` (sin prefijo `Bearer`)
- Header recomendado: `accept: application/json`

Ejemplo rápido en Python:
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

### Depósitos
- GET `/deposito`
- Devuelve listado de depósitos de la empresa.

### Facturas de venta
- GET `/facturas`
- Parámetros usados (query):
  - `idEmpresa` (int, requerido)
  - `idSucursal` (int, requerido)
  - `fechaDesde` (yyyy-MM-dd)
  - `fechaHasta` (yyyy-MM-dd)
  - `limit` (por defecto 20, máx 50)
  - `offset` (por defecto 0)
- Ejemplo que devuelve resultados:
```
https://erp.duxsoftware.com.ar/WSERP/rest/services/facturas\
  ?idEmpresa=9425\
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
- El servicio aplica rate limit (“Has alcanzado el límite de frecuencia…”). Si ocurre, espera al menos 10–15 segundos antes de repetir.
- Los parámetros distinguen mayúsculas/minúsculas (`idEmpresa`, `fechaDesde`, etc.).
