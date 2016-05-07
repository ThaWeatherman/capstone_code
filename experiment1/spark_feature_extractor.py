import math
import json
from __future__ import division  # running in py2

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import FloatType
from pyspark.sql import functions as F


MAPPING_FILE = 'mapping.json'


def shannon_entropy(s):
    prob = [float(s.count(c)/len(s)) for c in s]
    entropy = -1 * sum([p*math.log(p)/math.log(2) for p in prob])
    return entropy


def load_mapping():
	with open(MAPPING_FILE) as f:
		mapping = pickle.load(f)
	return mapping

	
def main():
	conf = SparkConf().setMaster('TODO').setAppName('Feature Extractor')
	sc = SparkContext(conf=conf)
	sqlcontext = SQLContext(sc)
	df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('s3://dnsdatajhu/data/dns.csv')
	# drop NaN rows
	df_drop = df.dropna()
	# add column for entropy
	entropy = F.udf(shannon_entropy, FloatType())
	df_ent = df_drop.withColumn('ENTROPY', entropy(df_drop.RRNAME))
	# now do the mapping


if __name__ == '__main__':
	main()
