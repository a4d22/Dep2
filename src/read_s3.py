import boto3
import pandas as pd
from io import StringIO


BUCKET = "aws-mlops-churn-adeetya-2026"
KEY = "data/telco_churn.csv"

s3 = boto3.client("s3")

obj = s3.get_object(Bucket=BUCKET, Key=KEY)
body = obj["Body"].read().decode("utf-8")
df = pd.read_csv(StringIO(body))

print(df.columns)

print(df.head())
print(df.shape)