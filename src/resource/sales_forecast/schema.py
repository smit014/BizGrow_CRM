from pydantic import BaseModel
from datetime import date


class PredictionRequest(BaseModel):
    date : date