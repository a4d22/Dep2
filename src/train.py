import boto3
import pandas as pd
from io import StringIO

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

BUCKET = "aws-mlops-churn-adeetya-2026"
KEY = "data/telco_churn.csv"

# ------------------
# Load Data
# ------------------

s3 = boto3.client("s3")

obj = s3.get_object(
    Bucket=BUCKET,
    Key=KEY
)

df = pd.read_csv(
    StringIO(
        obj["Body"].read().decode("utf-8")
    )
)

# ------------------
# Cleanup
# ------------------

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df["Churn"] = (
    df["Churn"]
    .map({"Yes": 1, "No": 0})
)

df = df.drop(columns=["customerID"])

# ------------------
# Split
# ------------------

X = df.drop(columns=["Churn"])
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ------------------
# Features
# ------------------

categorical_features = X.select_dtypes(
    include="object"
).columns.tolist()

numeric_features = X.select_dtypes(
    exclude="object"
).columns.tolist()

# ------------------
# Preprocessing
# ------------------

numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ]
)

categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numeric_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        )
    ]
)

# ------------------
# Model Pipeline
# ------------------

model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=200,
                random_state=42
            )
        )
    ]
)

# ------------------
# Train
# ------------------

model.fit(
    X_train,
    y_train
)

# ------------------
# Evaluate
# ------------------

preds = model.predict(X_test)

acc = accuracy_score(
    y_test,
    preds
)

print(f"Accuracy: {acc:.4f}")

# ------------------
# Save Model
# ------------------

joblib.dump(
    model,
    "model.pkl"
)

print("Saved model.pkl")