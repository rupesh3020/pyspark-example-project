"""
test_etl_job.py
~~~~~~~~~~~~~~~

This module contains unit tests for the transformation steps of the ETL
job defined in etl_job.py. It makes use of a local version of PySpark
that is bundled with the PySpark package.
"""
import unittest

import json

from pyspark.sql.functions import mean

from dependencies.spark import start_spark
from jobs.etl_job import transform_data


class SparkETLTests(unittest.TestCase):
    """Test suite for transformation in etl_job.py
    """
    @classmethod
    def setUp(self):
        """Start Spark, define config and path to test data
        """
        with open("configs/spark_config.json") as f:
            data = f.read()
        self.spark_config = json.loads(data)
        self.jar_packages = ["org.apache.hadoop:hadoop-azure:3.2.4","com.microsoft.azure:azure-storage:3.1.0"]
        self.config = json.loads("""{"steps_per_floor": 21}""")
        self.spark, *_ = start_spark(spark_config=self.spark_config, jar_packages=self.jar_packages)
        self.test_data_path = 'wasbs://datasource@datafeed.blob.core.windows.net/'

    @classmethod
    def tearDown(self):
        """Stop Spark
        """
        self.spark.stop()

    def test_normal_date(self):
        data=[("Z", 1),("A", 20),("B", 30),("C", 40),("B", 30),("B", 60)]
        inputRDD = self.spark.sparkContext.parallelize(data)
        count = inputRDD.count()
        assert count == 6

    def test_transform_data(self):
        """Test data transformer.

        Using small chunks of input data and expected output data, we
        test the transformation step to make sure it's working as
        expected.
        """
        # assemble
        input_data = (
            self.spark
            .read
            .parquet(self.test_data_path + 'employees'))

        expected_data = (
            self.spark
            .read
            .parquet(self.test_data_path + 'employees_report'))

        expected_cols = len(expected_data.columns)
        expected_rows = expected_data.count()
        expected_avg_steps = (
            expected_data
            .agg(mean('steps_to_desk').alias('avg_steps_to_desk'))
            .collect()[0]
            ['avg_steps_to_desk'])

        # act
        data_transformed = transform_data(input_data, 21)

        cols = len(expected_data.columns)
        rows = expected_data.count()
        avg_steps = (
            expected_data
            .agg(mean('steps_to_desk').alias('avg_steps_to_desk'))
            .collect()[0]
            ['avg_steps_to_desk'])

        # assert
        self.assertEqual(expected_cols, cols)
        self.assertEqual(expected_rows, rows)
        self.assertEqual(expected_avg_steps, avg_steps)
        self.assertTrue([col in expected_data.columns
                         for col in data_transformed.columns])


if __name__ == '__main__':
    unittest.main()
