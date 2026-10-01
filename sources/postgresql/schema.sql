CREATE TABLE IF NOT EXISTS public.orders (
    order_id varchar(64) PRIMARY KEY,
    customer_id varchar(64) NOT NULL,
    product_id varchar(64) NOT NULL,
    order_date timestamptz NOT NULL,
    updated_at timestamptz NOT NULL,
    quantity integer NOT NULL CHECK (quantity > 0),
    unit_price numeric(18,2) NOT NULL CHECK (unit_price >= 0),
    currency char(3) NOT NULL
);
INSERT INTO public.orders VALUES ('O100', 'C01', 'P01', '2026-09-01T10:00:00Z', '2026-09-01T11:00:00Z', 3, 19.95, 'USD')
ON CONFLICT (order_id) DO NOTHING;
-- Configure supported replication/server settings and least-privilege mirroring user
-- separately using the PostgreSQL Fabric connector prerequisites; this DDL does not enable CDC.
