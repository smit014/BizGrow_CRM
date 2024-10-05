from datetime import datetime, timedelta,date
import pandas as pd
from database.database import Sessionlocal
from src.resource.invoice.model import Invoice
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
from fastapi import HTTPException
from sklearn.impute import SimpleImputer
from fastapi.responses import JSONResponse
import os
from fastapi.encoders import jsonable_encoder


db = Sessionlocal()

def train_sales_model(organization_id):
    try:
        # Train the model for the user with the given organization_id
        model = train_sales_prediction_model(organization_id)
        return JSONResponse({"detail": "Model trained and saved successfully.","model": model})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def predict_sales(organization_id, prediction_date):
    # Check if the model exists for the user
    if os.path.exists(f'sales_prediction_model_of_{organization_id}.pkl'):
        try:
            # Predict sales using the trained model
            predicted_sales = predict_sales_for_date(organization_id, prediction_date)
            return JSONResponse({"predicted_sales": predicted_sales})
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Model not found for the organization. Please train the model first.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        # If the model file doesn't exist, raise an exception or return an error
        raise HTTPException(status_code=404, detail="Model not found. Please ensure the model is trained.")



def get_sales_data_for_six_months(organization_id):
    # Fetch sales data for the last 6 months
    six_months_ago = date.today() - timedelta(days=180)
    sales_data = db.query(Invoice).filter(
        Invoice.organization_id == organization_id,
        Invoice.invoice_date >= six_months_ago
    ).all()
    
    # Convert sales data to DataFrame
    data = pd.DataFrame([{
        'invoice_date': sale.invoice_date,
        'total_amount': sale.total_amount
    } for sale in sales_data])

    # Ensure data exists
    if data.empty:
        return None  # Handle no data case
    
    return data

def label_active_months(data):
    # Convert 'invoice_date' to datetime
    data['invoice_date'] = pd.to_datetime(data['invoice_date'])
    
    # Extract month and year from 'invoice_date'
    data['month'] = data['invoice_date'].dt.month
    data['year'] = data['invoice_date'].dt.year

    # Calculate total average sales (across all months)
    total_average_sales = data['total_amount'].mean()

    # Group by year and month to calculate monthly average sales
    monthly_avg_sales = data.groupby(['year', 'month'])['total_amount'].mean().reset_index()

    # Label active month (1 if monthly avg > total avg, else 0)
    monthly_avg_sales['active_month'] = monthly_avg_sales['total_amount'].apply(
        lambda x: 1 if x > total_average_sales else 0
    )

    return monthly_avg_sales


def train_sales_prediction_model(organization_id):
    # Check if the model already exists
    model_file_path = f'sales_prediction_model_of_{organization_id}.pkl'
    if os.path.exists(model_file_path):
        # If model exists, load it
        with open(model_file_path, 'rb') as f:
            model = pickle.load(f)
    else:
        # If no model exists, create a new LinearRegression model
        model = LinearRegression()

    # Fetch the last 6 months of sales data
    sales_data = get_sales_data_for_six_months(organization_id)
    if sales_data is None:
        raise Exception("Insufficient sales data to train the model.")
    
    # Label months as active or inactive
    labeled_data = label_active_months(sales_data)
    
    # Prepare features for the model (active month, month, day of year)
    labeled_data['day_of_year'] = pd.to_datetime(
        labeled_data['year'].astype(str) + labeled_data['month'].astype(str), format='%Y%m'
    ).dt.dayofyear

    # X will have 'active_month', 'month', and 'day_of_year'
    X = labeled_data[['active_month', 'month', 'day_of_year']]
    y = labeled_data['total_amount']  # Target variable: total sales

    # Impute missing values (if any)
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Retrain the existing model with the new data
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Save the updated model after retraining
    with open(model_file_path, 'wb') as f:
        pickle.dump(model, f)

    return JSONResponse({"Message": "Model retrained successfully", "mse": mse, "r2": r2})


def predict_sales_for_date(organization_id, new_date):
    # Load the trained model
    with open(f'sales_prediction_model_of_{organization_id}.pkl', 'rb') as f:
        model = pickle.load(f)

    # Prepare new data for prediction
    new_data = pd.DataFrame({
        'active_month': [1],  # Example: yes for active month
        'month': [new_date.month],
        'day_of_year': [new_date.timetuple().tm_yday]
    })

    # Predict sales
    predicted_sales = model.predict(new_data)
    return predicted_sales[0]

def predict_next_30_days_sales(organization_id, active_month):
    if os.path.exists(f'sales_prediction_model_of_{organization_id}.pkl'):
        # Load the trained model
        with open(f'sales_prediction_model_of_{organization_id}.pkl', 'rb') as f:
            model = pickle.load(f)
        # Calculate the next 30 days from the current date
        current_date = datetime.now() 
        start_date = current_date + timedelta(days=1)  # Start from tomorrow
        next_30_days = [start_date + timedelta(days=i) for i in range(60)]

        # Prepare data for prediction (active month, month, day_of_year)
        prediction_data = pd.DataFrame({
            'active month': [1 if active_month else 0] * 60,
            'month': [d.month for d in next_30_days],
            'day_of_year': [d.timetuple().tm_yday for d in next_30_days]
        })

        # Predict sales for the next 30 days
        predicted_sales = model.predict(prediction_data)

        # Prepare the response [{x: 'date', y: 'predicted_sales'}]
        response = [
            {"x": d.strftime('%Y-%m-%d'), "value": round(sales, 2)}
            for d, sales in zip(next_30_days, predicted_sales)
        ]
        return response
    else:
        # If the model file doesn't exist, raise an exception or return an error
        raise HTTPException(status_code=404, detail="Model not found. Please ensure the model is trained.")

# def gather_sales_data(organization_id):
#     six_months_ago = datetime.now() - timedelta(days=180)
    
#     # Query sales data from the invoice table for the past 6 months
#     sales_data = db.query(
#         func.date(Invoice.invoice_date).label('date'),
#         func.sum(Invoice.total_amount).label('total_amount')
#     ).filter(
#         Invoice.organization_id == organization_id,
#         Invoice.invoice_date >= six_months_ago
#     ).group_by(
#         func.date(Invoice.invoice_date)
#     ).all()

#     # Prepare DataFrame from sales data
#     data = pd.DataFrame([{
#         'active month': 1 if sale.date.month in [1, 12] else 0,  # Customize as per active month logic
#         'month': sale.date.month,
#         'day_of_year': sale.date.timetuple().tm_yday,
#         'total_amount': sale.total_amount
#     } for sale in sales_data])
    
#     return data


# def train_sales_prediction_model(sales_data, organization_id):
#     # Ensure sufficient data
#     if len(sales_data) < 180:  # 6 months of data
#         return None, "Insufficient data for training the model"
    
#     # Prepare features and target variable
#     X = sales_data[['active month', 'month', 'day_of_year']]
#     y = sales_data['total_amount']
    
#     # Split data into training and testing sets
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
#     # Create and train the model
#     model = LinearRegression()
#     model.fit(X_train, y_train)
    
#     # Evaluate the model
#     y_pred = model.predict(X_test)
#     mse = mean_squared_error(y_test, y_pred)
#     r2 = r2_score(y_test, y_pred)
    
#     # Save the model
#     with open(f'sales_prediction_model_{organization_id}.pkl', 'wb') as f:
#         pickle.dump(model, f)

#     return model, {"mse": mse, "r2": r2}


# def make_sales_prediction(date, organization_id):
#     try:
#         # Load the model
#         with open(f'sales_prediction_model_{organization_id}.pkl', 'rb') as f:
#             model = pickle.load(f)

#         # Prepare new data for prediction
#         new_data = pd.DataFrame({
#             'active month': [1 if date.month in [1, 12] else 0],
#             'month': [date.month],
#             'day_of_year': [date.timetuple().tm_yday]
#         })

#         # Make the prediction
#         predicted_sales = model.predict(new_data)
#         return predicted_sales[0]
    
#     except FileNotFoundError:
#         return None, "Model not found"


# def predict_sales(org_id):
    try:
        # Check if user has at least 6 months of sales data
        sales_data = gather_sales_data(org_id)
        if sales_data.empty:
            raise HTTPException(status_code=400, detail="Insufficient sales data")

        # Train the model
        model, result = train_sales_prediction_model(sales_data, org_id)
        if model is None:
            raise HTTPException(status_code=400, detail=result)
        
        # Predict the next month's sales
        next_month = datetime.now() + timedelta(days=30)
        prediction, error = make_sales_prediction(next_month, org_id)
        if error:
            raise HTTPException(status_code=500, detail=error)

        return {"next_month_sales_prediction": prediction}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))