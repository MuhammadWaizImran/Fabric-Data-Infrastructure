# Read the external share accepted into this consumer-owned lakehouse.
# Name the accepted table shortcut shared_daily_sales, or edit this path before import.
from pyspark.sql import functions as F

shared = spark.read.format("delta").load(lakehouse_root + "/Tables/shared_daily_sales")
shared.groupBy("currency").agg(F.sum("revenue").alias("revenue"), F.sum("orders").alias("orders")).show()
# Deliberately read-only: external share data belongs to the provider.
# Persist consumer-derived results only to a separate consumer-owned write target.
