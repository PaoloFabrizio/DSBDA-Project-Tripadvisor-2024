import findspark
findspark.init()
import pyspark
from pyspark.sql import SparkSession, Row
import re

# Funzione per preprocessare il file CSV
def preprocess_csv(input_path, output_path):
    with open(input_path, 'r') as file:
        lines = file.readlines()
   
    processed_lines = []
    for line in lines:
        # Usa una regex per trovare i campi tra parentesi quadre
        line = re.sub(r'\[([^\]]+)\]', lambda m: m.group(0).replace(',', ';'), line)
        # Usa una regex per trovare i campi tra virgolette doppie
        line = re.sub(r'"([^"]*)"', lambda m: m.group(0).replace(',', ';'), line)


        processed_lines.append(line)
   
    with open(output_path, 'w') as file:
        file.writelines(processed_lines)

# Context with Hadoop
'''
spark = SparkSession.builder \
    .appName("CSV to HDFS") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode_host:54310") \
    .getOrCreate()
'''

# Context without Hadoop
sc = pyspark.SparkContext(appName="CSV Reader")
spark = SparkSession(sc)

def drop_columns_and_save(df, columns_to_drop, num_partitions):
    rdd = df.rdd

    header = df.columns
    columns_to_keep = [i for i in range(len(header)) if i not in columns_to_drop]
    rdd_filtered = rdd.map(lambda row: tuple(row[i] for i in columns_to_keep))

    # First column is 0, 1, 2...
    rdd_with_index = rdd_filtered.zipWithIndex().map(lambda row: (row[1],) + row[0])
    new_header = ['index'] + [header[i] for i in columns_to_keep]
    df_filtered = rdd_with_index.map(lambda x: Row(*x)).toDF(new_header)

    rdd_repartitioned = df_filtered.rdd.repartition(num_partitions)
    df_repartitioned = rdd_repartitioned.map(lambda x: Row(*x)).toDF(new_header)

    # Save locally since Hadoop doesn't work
    df_repartitioned.write.csv("tripadvisor_filtered.csv", header=True, mode='overwrite')
   
    '''
    hdfs_path = "hdfs://namenode_host:54310/projectDSBDA/dataset1.csv"
    df_filtered.write.csv(hdfs_path, header=True, mode='overwrite')
    '''

    return df_repartitioned

def print_shape(dataframe):
    num_rows = dataframe.count()
    num_columns = len(dataframe.columns)
    print(f"Shape of the DataFrame: ({num_rows}, {num_columns})")

#----------MAIN----------

# Preprocess the CSV file
preprocess_csv('tripadvisor.csv', 'tripadvisor_processed.csv')

# Read the preprocessed CSV file
df = spark.read.csv("tripadvisor_processed.csv", header=True, inferSchema=True, quote='"', escape='"', multiLine=True)

print_shape(df)

# divide in partitions otherwise too heavy the csv to handle (more or less 200000 rows for partition)
num_partitions = round(df.count() / 50000)

# Drop columns (give number)
df_filtered = drop_columns_and_save(df, [0, 2, 7, 30, 31, 41], num_partitions)

# Final shape is initial columns count - elements in the list + 1 (for the index column)
print_shape(df_filtered)

spark.stop()
