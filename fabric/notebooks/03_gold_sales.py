from pyspark.sql import functions as F

orders = spark.read.format("delta").load(lakehouse_root + "/Tables/silver_orders")
gold = orders.groupBy("date", "currency").agg(
    F.count("order_id").alias("orders"), F.sum("quantity").alias("quantity"), F.sum("revenue").alias("revenue"))
if gold.filter(F.col("revenue") < 0).count():
    raise ValueError("Gold quality gate failed: negative revenue")
gold.write.format("delta").mode("overwrite").save(lakehouse_root + "/Tables/gold_daily_sales")
print({"gold_days": gold.count(), "orders": orders.count()})
