# The build script supplies lakehouse_root as the first parameter cell.
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("order_id", StringType()), StructField("customer_id", StringType()),
    StructField("product_id", StringType()), StructField("order_date", StringType()),
    StructField("updated_at", StringType()), StructField("quantity", IntegerType()),
    StructField("unit_price", StringType()), StructField("currency", StringType()),
    StructField("_corrupt_record", StringType()),
])
raw = spark.read.schema(schema).option("mode", "PERMISSIVE").json(lakehouse_root + "/Files/landing/orders/*.jsonl")
raw = raw.withColumn("ingested_at", F.current_timestamp()).withColumn("source_file", F.input_file_name())
# Reference workload performs a full fixture snapshot. Do not point at a partial CDC feed.
raw.write.format("delta").mode("overwrite").save(lakehouse_root + "/Tables/bronze_orders")
print({"bronze_rows": raw.count()})
