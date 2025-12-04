"""Ejemplos de uso de los endpoints GET de Dux.

- Base URL: https://erp.duxsoftware.com.ar/WSERP/rest/services/
- Autenticación: header `authorization` con tu token (sin prefijo Bearer).
- Rate limit: si responde “Has alcanzado el limite…”, espera ~10 s antes de reintentar.

Define la variable de entorno DUX_TOKEN con tu token antes de ejecutar:
  set DUX_TOKEN=tu_token
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, Optional

import requests

BASE_URL = "https://erp.duxsoftware.com.ar/WSERP/rest/services"
TOKEN = os.getenv("DUX_TOKEN", "REEMPLAZA_CON_TU_TOKEN")


def _session() -> requests.Session:
    """Crea una sesión con headers comunes."""
    s = requests.Session()
    s.headers.update(
        {
            "authorization": TOKEN,
            "accept": "application/json",
        }
    )
    return s


def get(path: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """Hace un GET y devuelve JSON (lanza si hay error HTTP)."""
    url = f"{BASE_URL}/{path.lstrip('/')}"
    with _session() as s:
        resp = s.get(url, params=params, timeout=30)
        resp.raise_for_status()
        # Algunos endpoints devuelven texto plano de error con 200 OK
        try:
            return resp.json()
        except ValueError:
            return resp.text


# --- Endpoints específicos -------------------------------------------------


def get_depositos() -> Any:
    return get("deposito")


def get_empresas() -> Any:
    return get("empresas")


def get_items() -> Any:
    return get("items")


def get_lista_precio_venta() -> Any:
    return get("listaprecioventa")


def get_localidades() -> Any:
    return get("localidades")


def get_pedidos(params: Optional[Dict[str, Any]] = None) -> Any:
    return get("pedidos", params=params)


def get_percepciones_impuestos() -> Any:
    return get("percepcionesImpuestos")


def get_personales() -> Any:
    return get("personales")


def get_provincias() -> Any:
    return get("provincias")


def get_rubros() -> Any:
    return get("rubros")


def get_subrubros() -> Any:
    return get("subrubros")


def get_sucursales() -> Any:
    return get("sucursales")


def get_obtener_estado_factura(params: Dict[str, Any]) -> Any:
    """Parámetros esperados (ejemplo): {'idCompVenta': 123}"""
    return get("obtenerEstadoFactura", params=params)


def get_obtener_estado_item(params: Dict[str, Any]) -> Any:
    """Parámetros esperados (ejemplo): {'idItem': 123}"""
    return get("obtenerEstadoItem", params=params)


def get_compras(params: Dict[str, Any]) -> Any:
    """Requiere al menos fechaDesde y fechaHasta (yyyy-MM-dd)."""
    return get("compras", params=params)


def get_facturas(params: Dict[str, Any]) -> Any:
    """Requiere idEmpresa, idSucursal, fechaDesde, fechaHasta."""
    return get("facturas", params=params)


def demo() -> None:
    """Ejemplo mínimo (no se llama por defecto para evitar rate-limit)."""
    if TOKEN == "REEMPLAZA_CON_TU_TOKEN":
        raise SystemExit("Configura DUX_TOKEN con tu token antes de usar.")

    ejemplos = [
        ("deposito", get_depositos, None),
        (
            "facturas",
            get_facturas,
            {
                "idEmpresa": 9425,
                "idSucursal": 3,
                "fechaDesde": "2025-09-01",
                "fechaHasta": "2025-09-15",
                "limit": 2,
                "offset": 0,
            },
        ),
    ]

    for nombre, fn, params in ejemplos:
        print(f"\n### {nombre}")
        data = fn(params) if params else fn()  # type: ignore[arg-type]
        print(str(data)[:2000])  # salida recortada
        time.sleep(6)  # evitar rate-limit


if __name__ == "__main__":
    # Para ejecutar ejemplos, descomenta la siguiente línea:
    # demo()
    print("Este módulo expone funciones GET. Importe y use, o habilita demo().")
