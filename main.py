from __future__ import annotations

import datetime as dt
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ------------------------------------------------------------
# Datos mock (ajustar a datos reales cuando haya ETL con la API)
# ------------------------------------------------------------


class Item(BaseModel):
    cod_item: str
    descripcion: str
    marca: str
    peso_kg: Optional[float] = None
    es_estrella: bool = False
    es_senda20: bool = False
    es_jaspe3kg: bool = False


class FacturaDetalle(BaseModel):
    item: Item
    cantidad: float
    precio_unitario: float
    total_linea: float


class Factura(BaseModel):
    id: int
    fecha: dt.date
    vendedor_id: int
    sucursal_id: int
    total: float
    detalles: List[FacturaDetalle]


class Objetivo(BaseModel):
    vendedor_id: int
    periodo: dt.date  # usar primer día del mes
    objetivo_total: float
    objetivo_estrella: float
    objetivo_senda20: float
    objetivo_jaspe3: float


class Vendedor(BaseModel):
    id: int
    nombre: str
    sucursal_id: int


class Sucursal(BaseModel):
    id: int
    nombre: str


vendors = [
    Vendedor(id=1, nombre="Luciano Torres", sucursal_id=1),
    Vendedor(id=2, nombre="María López", sucursal_id=2),
    Vendedor(id=3, nombre="Carlos Pérez", sucursal_id=1),
]

sucursales = [
    Sucursal(id=1, nombre="BANDA"),
    Sucursal(id=2, nombre="BELGRANO"),
]

# Clasificación de productos clave
estrella_brand = "PETS PLUS"
senda_code = "77700001"
jaspe_codes = {
    "900906",
    "900905",
    "900908",
    "900910",
    "900919",
    "900911",
    "900907",
    "900909",
    "900920",
    "900912",
}


def build_item(cod_item: str, descripcion: str, marca: str, peso_kg: Optional[float]) -> Item:
    marca_up = marca.upper()
    desc_up = descripcion.upper()
    es_estrella = marca_up.startswith(estrella_brand)
    es_senda20 = cod_item == senda_code or ("SENDA AD" in desc_up and "20" in desc_up)
    es_jaspe3kg = (marca_up == "JASPE" and (peso_kg or 0) >= 3) or cod_item in jaspe_codes
    return Item(
        cod_item=cod_item,
        descripcion=descripcion,
        marca=marca,
        peso_kg=peso_kg,
        es_estrella=es_estrella,
        es_senda20=es_senda20,
        es_jaspe3kg=es_jaspe3kg,
    )


# Items de ejemplo
item_senda = build_item("77700001", "SENDA AD X20KG", "SENDA", 20)
item_pets_plus = build_item("463257", "PELOTA 3 MODOS P+", "PETS PLUS IMPORTADOS", None)
item_jaspe = build_item("900908", "JASPE ADULTO X 20 KG", "JASPE", 20)

facturas: List[Factura] = [
    Factura(
        id=78266154,
        fecha=dt.date(2025, 9, 15),
        vendedor_id=1,
        sucursal_id=1,
        total=62019.88,
        detalles=[
            FacturaDetalle(item=item_senda, cantidad=2, precio_unitario=15000, total_linea=30000),
            FacturaDetalle(item=item_pets_plus, cantidad=5, precio_unitario=2000, total_linea=10000),
            FacturaDetalle(item=item_jaspe, cantidad=1, precio_unitario=22019.88, total_linea=22019.88),
        ],
    ),
    Factura(
        id=78252726,
        fecha=dt.date(2025, 9, 15),
        vendedor_id=2,
        sucursal_id=2,
        total=27100.37,
        detalles=[
            FacturaDetalle(item=item_senda, cantidad=1, precio_unitario=18000, total_linea=18000),
            FacturaDetalle(item=item_pets_plus, cantidad=2, precio_unitario=1000, total_linea=2000),
            FacturaDetalle(item=item_jaspe, cantidad=1, precio_unitario=7100.37, total_linea=7100.37),
        ],
    ),
    Factura(
        id=78252727,
        fecha=dt.date(2025, 9, 16),
        vendedor_id=1,
        sucursal_id=1,
        total=15000,
        detalles=[
            FacturaDetalle(item=item_pets_plus, cantidad=3, precio_unitario=5000, total_linea=15000),
        ],
    ),
]

objetivos: List[Objetivo] = [
    Objetivo(
        vendedor_id=1,
        periodo=dt.date(2025, 9, 1),
        objetivo_total=200000,
        objetivo_estrella=80000,
        objetivo_senda20=50,
        objetivo_jaspe3=40,
    ),
    Objetivo(
        vendedor_id=2,
        periodo=dt.date(2025, 9, 1),
        objetivo_total=150000,
        objetivo_estrella=60000,
        objetivo_senda20=30,
        objetivo_jaspe3=25,
    ),
]


# ------------------------------------------------------------
# FastAPI
# ------------------------------------------------------------
app = FastAPI(title="Dux Objetivos Vendedores (demo)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_objetivo(vendedor_id: int, periodo: dt.date) -> Optional[Objetivo]:
    for obj in objetivos:
        if obj.vendedor_id == vendedor_id and obj.periodo == periodo:
            return obj
    return None


def kpi_from_facturas(vendedor_id: int, periodo: dt.date) -> Dict:
    facs = [
        f
        for f in facturas
        if f.vendedor_id == vendedor_id and f.fecha.year == periodo.year and f.fecha.month == periodo.month
    ]
    total = sum(f.total for f in facs)
    estrella = 0.0
    senda_unidades = 0.0
    jaspe_unidades = 0.0
    for f in facs:
        for d in f.detalles:
            if d.item.es_estrella:
                estrella += d.total_linea
            if d.item.es_senda20:
                senda_unidades += d.cantidad
            if d.item.es_jaspe3kg:
                jaspe_unidades += d.cantidad
    obj = get_objetivo(vendedor_id, periodo)
    def pct(v, goal): return 0 if not goal else round((v / goal) * 100, 1)
    return {
        "periodo": periodo.isoformat(),
        "total": total,
        "objetivo_total": obj.objetivo_total if obj else None,
        "avance_total_pct": pct(total, obj.objetivo_total if obj else None),
        "estrella": estrella,
        "objetivo_estrella": obj.objetivo_estrella if obj else None,
        "avance_estrella_pct": pct(estrella, obj.objetivo_estrella if obj else None),
        "senda20_unidades": senda_unidades,
        "objetivo_senda20": obj.objetivo_senda20 if obj else None,
        "avance_senda20_pct": pct(senda_unidades, obj.objetivo_senda20 if obj else None),
        "jaspe3kg_unidades": jaspe_unidades,
        "objetivo_jaspe3": obj.objetivo_jaspe3 if obj else None,
        "avance_jaspe3_pct": pct(jaspe_unidades, obj.objetivo_jaspe3 if obj else None),
        "facturas": facs,
    }


@app.get("/api/vendors")
def list_vendors():
    return vendors


@app.get("/api/kpi")
def kpi(vendedor_id: int, periodo: str):
    try:
        p = dt.datetime.strptime(periodo, "%Y-%m").date().replace(day=1)
    except ValueError:
        raise HTTPException(400, "periodo debe ser YYYY-MM")
    if not any(v.id == vendedor_id for v in vendors):
        raise HTTPException(404, "vendedor no encontrado")
    return kpi_from_facturas(vendedor_id, p)


@app.get("/api/admin/kpi")
def kpi_admin(periodo: str):
    try:
        p = dt.datetime.strptime(periodo, "%Y-%m").date().replace(day=1)
    except ValueError:
        raise HTTPException(400, "periodo debe ser YYYY-MM")
    out = []
    for v in vendors:
        data = kpi_from_facturas(v.id, p)
        out.append({"vendedor": v.nombre, "sucursal_id": v.sucursal_id, **data})
    return out


class ObjetivoIn(BaseModel):
    vendedor_id: int
    periodo: str
    objetivo_total: Optional[float] = None
    objetivo_estrella: Optional[float] = None
    objetivo_senda20: Optional[float] = None
    objetivo_jaspe3: Optional[float] = None


@app.post("/api/objetivos")
def set_objetivo(payload: ObjetivoIn):
    try:
        p = dt.datetime.strptime(payload.periodo, "%Y-%m").date().replace(day=1)
    except ValueError:
        raise HTTPException(400, "periodo debe ser YYYY-MM")
    if not any(v.id == payload.vendedor_id for v in vendors):
        raise HTTPException(404, "vendedor no encontrado")
    existing = get_objetivo(payload.vendedor_id, p)
    if existing:
        objetivos.remove(existing)
    objetivos.append(
        Objetivo(
            vendedor_id=payload.vendedor_id,
            periodo=p,
            objetivo_total=payload.objetivo_total or 0,
            objetivo_estrella=payload.objetivo_estrella or 0,
            objetivo_senda20=payload.objetivo_senda20 or 0,
            objetivo_jaspe3=payload.objetivo_jaspe3 or 0,
        )
    )
    return {"status": "ok"}


# Servir frontend estático
app.mount("/", StaticFiles(directory="static", html=True), name="static")
