-- Esquema base para la app de objetivos de ventas

CREATE TABLE IF NOT EXISTS sucursales (
    id           BIGINT PRIMARY KEY,
    nombre       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vendedores (
    id           BIGINT PRIMARY KEY,
    nombre       TEXT NOT NULL,
    sucursal_id  BIGINT REFERENCES sucursales(id)
);

CREATE TABLE IF NOT EXISTS items (
    id           BIGINT PRIMARY KEY,  -- id interno de Dux si se usa; si no, usar cod_item como PK
    cod_item     TEXT UNIQUE,
    descripcion  TEXT,
    marca        TEXT,
    rubro        TEXT,
    sub_rubro    TEXT,
    peso_kg      NUMERIC,
    es_estrella  BOOLEAN DEFAULT FALSE,
    es_senda20   BOOLEAN DEFAULT FALSE,
    es_jaspe3kg  BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS objetivos (
    id              BIGSERIAL PRIMARY KEY,
    vendedor_id     BIGINT REFERENCES vendedores(id),
    periodo         DATE NOT NULL, -- usar primer día del mes como período
    objetivo_total  NUMERIC,
    objetivo_estrella NUMERIC,
    objetivo_senda20 NUMERIC,
    objetivo_jaspe3  NUMERIC
);

CREATE TABLE IF NOT EXISTS facturas (
    id              BIGINT PRIMARY KEY, -- id de la factura en Dux
    fecha           DATE NOT NULL,
    vendedor_id     BIGINT REFERENCES vendedores(id),
    sucursal_id     BIGINT REFERENCES sucursales(id),
    punto_venta     TEXT,
    numero          TEXT,
    tipo_comp       TEXT,
    letra_comp      TEXT,
    total           NUMERIC
);

CREATE TABLE IF NOT EXISTS facturas_detalle (
    id              BIGSERIAL PRIMARY KEY,
    factura_id      BIGINT REFERENCES facturas(id),
    item_id         BIGINT REFERENCES items(id),
    cantidad        NUMERIC,
    precio_unitario NUMERIC,
    total_linea     NUMERIC
);

CREATE INDEX IF NOT EXISTS idx_facturas_fecha ON facturas(fecha);
CREATE INDEX IF NOT EXISTS idx_facturas_vendedor ON facturas(vendedor_id);
CREATE INDEX IF NOT EXISTS idx_facturas_detalle_item ON facturas_detalle(item_id);
