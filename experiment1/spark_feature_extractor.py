from __future__ import division  # running in py2
import math
import json

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import FloatType
from pyspark.sql import functions as F


MAPPING_FILE = 'mapping.json'
# CSV_FILE = 's3://dnsdatajhu/data/dns.csv'
CSV_FILE = 'dns.csv'


def shannon_entropy(s):
    """computes the shannon entropy of a given string. returns a float"""
    prob = [float(s.count(c)/len(s)) for c in s]
    entropy = -1 * sum([p*math.log(p)/math.log(2) for p in prob])
    return entropy


def load_mapping():
    """loads the mapping dictionary of domains to ints"""
    with open(MAPPING_FILE) as f:
        mapping = json.load(f)
    return mapping

        
def main():
    conf = SparkConf().setMaster('local').setAppName('Feature Extractor')
    sc = SparkContext(conf=conf)
    sqlcontext = SQLContext(sc)
    df = sqlcontext.read.format('com.databricks.spark.csv').options(header='true',
                                inferschema='true').load(CSV_FILE)
    # drop NaN rows
    df_drop = df.dropna()
    '''
    # add column for entropy
    entropy = F.udf(shannon_entropy, FloatType())
    df_ent = df_drop.withColumn('ENTROPY', entropy(df_drop.RRNAME))
    # now do the mapping
    '''


if __name__ == '__main__':
    main()

