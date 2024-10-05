from fastapi import APIRouter
from src.resource.sales_forecast.schema import PredictionRequest
from src.functionality.sales_forecast.sales_forecast import predict_sales, predict_next_30_days_sales,train_sales_prediction_model

sales_router = APIRouter()

@sales_router.post("/{org_id}/predict-sales", status_code=200)
def predict_sales_api(org_id:str, prediction_date:PredictionRequest):

    sales_info = predict_sales(org_id,prediction_date.date)
    return sales_info



@sales_router.get("/{organization_id}/predict_next_month_sales", status_code=200)
def predict_next_month_sales_api(organization_id: str):
    active_month = True  # This should come from your active month logic
    # Predict next 30 days' sales
    sales_info= predict_next_30_days_sales(organization_id, active_month)
    return sales_info

@sales_router.post("/train_sales_model/")
def train_sales_model_api(organization_id:str):
    sales_info= train_sales_prediction_model(organization_id)
    return sales_info
    