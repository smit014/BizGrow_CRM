from database.database import Sessionlocal
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.resource.organization.model import Organization
from src.resource.invoice.model import Invoice
from src.resource.items.model import Item
from src.resource.customer.model import Customer
from datetime import date
from sqlalchemy import func,extract

db = Sessionlocal()

def get_dashboard(organization_id):
    try:
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
        today = date.today()
        today_sales = db.query(Invoice).filter(
            Invoice.organization_id == organization_id,
            func.date(Invoice.invoice_date) == today
        ).with_entities(
            func.sum(Invoice.total_amount).label("today_sales")
        ).scalar() or 0

        # 6.Monthly Sales Query (same month as current date)
        monthly_sales = db.query(
            func.sum(Invoice.total_amount).label("monthly_sales")
        ).filter(
            Invoice.organization_id == organization_id,
            extract('year', Invoice.invoice_date) == today.year,  # Filter by current year
            extract('month', Invoice.invoice_date) == today.month  # Filter by current month
        ).scalar() or 0

        # Prepare and return the response
        response = {
            "total_revenue": total_revenue,
            "last_five_customers": [customer.to_dict() for customer in last_five_customers],
            "last_five_items": [item.to_dict() for item in last_five_items],
            "last_five_invoices": [invoice.to_dict() for invoice in last_five_invoices],
            "today_sales": today_sales,
            "monthly_sales": monthly_sales
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
