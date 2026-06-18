from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from src.model import get_model

app = FastAPI()

model = get_model()


class Customer(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/")
def root():
    return {"status": "healthy"}


@app.post("/predict")
def predict(customer: Customer):

    df = pd.DataFrame([customer.model_dump()])

    probability = float(
        model.predict_proba(df)[0][1]
    )

    prediction = int(
        model.predict(df)[0]
    )

    return {
        "prediction": prediction,
        "churn_probability": probability
    }