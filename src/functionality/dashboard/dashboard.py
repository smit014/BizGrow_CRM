from database.database import Sessionlocal
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.resource.organization.model import Organization
from src.resource.invoice.model import Invoice
from src.resource.items.model import Item
from src.resource.customer.model import Customer
from datetime import date, timedelta
from sqlalchemy import func,extract

db = Sessionlocal()

# Helper function to calculate percentage change
def calculate_percentage_change(current, previous):
    if previous == 0:
        return 100 if current > 0 else 0  # Handle divide by zero
    return ((current - previous) / previous) * 100

def get_dashboard(organization_id):
    try:
        today = date.today()

        # 1. Total Revenue
        total_revenue = db.query(Invoice).filter(Invoice.organization_id == organization_id).with_entities(
            func.sum(Invoice.total_amount).label("total_revenue")
        ).scalar() or 0

        # 2. Last 5 Added Customers
        last_five_customers = db.query(Customer).filter(Customer.organization_id == organization_id).order_by(
            Customer.created_at.desc()
        ).limit(5).all()

        # 3. Last 5 Added Items
        last_five_items = db.query(Item).filter(Item.organization_id == organization_id).order_by(
            Item.created_at.desc()
        ).limit(5).all()

        # 4. Last 5 Invoices
        last_five_invoices = db.query(Invoice).filter(Invoice.organization_id == organization_id).order_by(
            Invoice.invoice_date.desc()
        ).limit(5).all()

        # 5. Today's Sales
        today_sales = db.query(
            func.sum(Invoice.total_amount).label("today_sales")
        ).filter(
            Invoice.organization_id == organization_id,
            func.date(Invoice.invoice_date) == today
        ).scalar() or 0

        # 6. Yesterday's Sales
        yesterday = today - timedelta(days=1)
        yesterday_sales = db.query(
            func.sum(Invoice.total_amount).label("yesterday_sales")
        ).filter(
            Invoice.organization_id == organization_id,
            func.date(Invoice.invoice_date) == yesterday
        ).scalar() or 0

        # 7. Daily Percentage Change
        daily_percentage_change = calculate_percentage_change(today_sales, yesterday_sales)

        # 8. Monthly Sales Query (same month as current date)
        monthly_sales = db.query(
            func.sum(Invoice.total_amount).label("monthly_sales")
        ).filter(
            Invoice.organization_id == organization_id,
            extract('year', Invoice.invoice_date) == today.year,  # Filter by current year
            extract('month', Invoice.invoice_date) == today.month  # Filter by current month
        ).scalar() or 0

        # 9. Previous Month Sales Query
        previous_month = today.replace(day=1) - timedelta(days=1)  # Last day of the previous month
        previous_month_sales = db.query(
            func.sum(Invoice.total_amount).label("previous_month_sales")
        ).filter(
            Invoice.organization_id == organization_id,
            extract('year', Invoice.invoice_date) == previous_month.year,  # Filter by previous year
            extract('month', Invoice.invoice_date) == previous_month.month  # Filter by previous month
        ).scalar() or 0

        # 10. Monthly Percentage Change
        monthly_percentage_change = calculate_percentage_change(monthly_sales, previous_month_sales)

        # 11. Sales Data for Graph (Last 30 Days)
        sales_data = db.query(
            func.date(Invoice.invoice_date).label('date'),
            func.sum(Invoice.total_amount).label('total_sales')
        ).filter(
            Invoice.organization_id == organization_id,
            Invoice.invoice_date >= today - timedelta(days=30)
        ).group_by(
            func.date(Invoice.invoice_date)
        ).all()

        # Prepare x-axis and y-axis data for chart
        x_axis = [record.date for record in sales_data]  # Dates
        y_axis = [record.total_sales for record in sales_data]  # Sales values

        # 12. Total Pending Amount (unpaid invoices)
        total_pending_amount = db.query(
            func.sum(Invoice.total_amount).label('total_pending')
        ).filter(
            Invoice.organization_id == organization_id,
            Invoice.status == 'unpaid'
        ).scalar() or 0

        # 13. Outstanding Amount (overdue unpaid invoices)
        outstanding_amount = db.query(
            func.sum(Invoice.total_amount).label('outstanding')
        ).filter(
            Invoice.organization_id == organization_id,
            Invoice.status == 'unpaid',
            Invoice.overdue_date < today
        ).scalar() or 0


        # Prepare and return the response
        response = {
            "total_revenue": total_revenue,
            "last_five_customers": [customer.to_dict() for customer in last_five_customers],
            "last_five_items": [item.to_dict() for item in last_five_items],
            "last_five_invoices": [invoice.to_dict() for invoice in last_five_invoices],
            "today_sales": today_sales,
            "yesterday_sales": yesterday_sales,
            "daily_percentage_change": daily_percentage_change,
            "monthly_sales": monthly_sales,
            "previous_month_sales": previous_month_sales,
            "monthly_percentage_change": monthly_percentage_change,
            "sales_chart_data": {
                "x_axis": x_axis,  # Dates
                "value": y_axis   # Total sales per day
            },
            "total_pending_amount": total_pending_amount,
            "outstanding_amount": outstanding_amount
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
