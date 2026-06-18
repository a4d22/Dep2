import joblib

_model = None


def get_model():
    global _model

    if _model is None:
        _model = joblib.load("artifacts/model.pkl")

    return _model