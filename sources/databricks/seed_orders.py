# Databricks notebook source
# Set catalog_name to an existing Unity Catalog catalog you are authorized to use.
dbutils.widgets.text("catalog_name", "fabric_demo")
catalog_name = dbutils.widgets.get("catalog_name")
import re
if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", catalog_name):
    raise ValueError("Invalid catalog identifier")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.sales")
spark.sql(f"""CREATE TABLE IF NOT EXISTS {catalog_name}.sales.orders
    (order_id STRING, customer_id STRING, quantity INT, unit_price DECIMAL(18,2)) USING DELTA""")
spark.sql(f"""MERGE INTO {catalog_name}.sales.orders t
    USING (SELECT 'O100' order_id, 'C01' customer_id, 3 quantity, CAST(19.95 AS DECIMAL(18,2)) unit_price) s
    ON t.order_id = s.order_id WHEN NOT MATCHED THEN INSERT *""")
# Configure Fabric mirrored Azure Databricks catalog for supported Unity Catalog tables.
# This is metadata mirroring; storage connectivity and grants are still required.
