# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC ## Overview
# MAGIC 
# MAGIC This notebook will show you how to create and query a table or DataFrame that you uploaded to DBFS. [DBFS](https://docs.databricks.com/user-guide/dbfs-databricks-file-system.html) is a Databricks File System that allows you to store data for querying inside of Databricks. This notebook assumes that you have a file already inside of DBFS that you would like to read from.
# MAGIC 
# MAGIC This notebook is written in **Python** so the default cell type is Python. However, you can use different languages by using the `%LANGUAGE` syntax. Python, Scala, SQL, and R are all supported.

# COMMAND ----------

# File location and type
file_location = "/FileStore/tables/data_with_features.csv"
file_type = "csv"

# CSV options
infer_schema = "true"
first_row_is_header = "true"
delimiter = ";"

# The applied options are for CSV files. For other file types, these will be ignored.
df = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .load(file_location)

import pyspark.sql.functions as F

df = df.withColumn("decision_date", F.to_date("decision_date", "yyyy-MM-dd HH:mm:ss"))
df = df.withColumn("registration_date", F.to_date("registration_date", "yyyy-MM-dd HH:mm:ss"))

# Create a view or table
temp_table_name = "SQL_data"

df.createOrReplaceTempView(temp_table_name)

df.dtypes

# COMMAND ----------

df.withColumn(
    "brand2",
    col("brand").rlike("MERCED")).show()

# COMMAND ----------

from pyspark.sql.functions import *
df = df.withColumn('brand2', regexp_extract(col('brand'), 'MCLAREN', 1))
temp_table_name = "SQL_data"

df.createOrReplaceTempView(temp_table_name)

# COMMAND ----------

# MAGIC %sql
# MAGIC select mean(car_tax), mean(power_KW), brand2 from SQL_data group by brand2
# MAGIC                                           order by mean(car_tax) desc

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC /* Query the created temp table in a SQL cell */
# MAGIC 
# MAGIC select COUNT(decision_date), decision_date from SQL_data group by decision_date order by decision_date

# COMMAND ----------

# MAGIC 
# MAGIC 
# MAGIC %sql
# MAGIC select COUNT(brand), brand from SQL_data group by brand
# MAGIC                                 

# COMMAND ----------

# MAGIC %sql
# MAGIC select COUNT(decision_date), year(decision_date), month(decision_date) from SQL_data 
# MAGIC                                   group by year(decision_date), month(decision_date)
# MAGIC                                   order by year(decision_date), month(decision_date)

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(brand), brand from SQL_data group by brand
# MAGIC                                           order by count(brand) desc
# MAGIC                                   

# COMMAND ----------

# MAGIC %sql
# MAGIC select sum(car_tax), brand from SQL_data group by brand
# MAGIC                                           order by sum(car_tax) desc

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC update SQL_data SET brand=REGEXP_REPLACE(brand, 'MC%', 'MCLAREN') WHERE brand REGEXP 'MC%'

# COMMAND ----------

# MAGIC %sql
# MAGIC select mean(car_tax), mean(power_KW), brand from SQL_data group by brand
# MAGIC                                           order by mean(car_tax) desc

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT brand FROM SQL_data WHERE brand like '%SAAB%' group by brand

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT brand FROM SQL_data WHERE brand like '%HUYNDAI%' or brand like 'HYUNDAI' group by brand

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT brand FROM SQL_data WHERE brand like 'TESLA%' group by brand

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT brand FROM SQL_data WHERE brand like '%MERCED%' or brand like 'MB' or brand like '%M-B' group by brand

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT brand FROM SQL_data WHERE brand like '%FERR%' group by brand

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT brand FROM SQL_data WHERE brand like 'POR%' group by brand

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT brand FROM SQL_data WHERE brand like 'ROL%' group by brand

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT brand FROM SQL_data WHERE brand like '%ROV%' group by brand

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT brand FROM SQL_data WHERE brand like '%JAG%' group by brand

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT brand FROM SQL_data WHERE brand like 'BMW%' or brand like 'ALPINA' group by brand

# COMMAND ----------


