from database.database import Sessionlocal
from src.resource.invoice.model import Invoice, InvoiceItem
from src.resource.customer.model import Customer
from src.resource.organization.model import Organization
from src.resource.user.model import User
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import uuid
from datetime import datetime,timedelta
from src.resource.invoice.serializer import serializer_for_invoice
from sqlalchemy.orm import joinedload

db = Sessionlocal()

def create_invoice(invoice_details, org_id, user_data):
    invoice_id = str(uuid.uuid4())
    try:
        user_id = user_data.get("id")
        # Retrieve the organization associated with the user
        organization_id = org_id
        organization = db.query(Organization).filter_by(id=organization_id).first()
        
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")

        # Initialize total amount to 0
        total_amount = 0
        
        # Add items to the invoice and calculate total amount
        items = invoice_details.get('items', [])
        for item in items:
            total_price = item.get('quantity') * item.get('unit_price')
            total_price += total_price * 12 / 100
            total_amount += total_price
            
            invoice_item = InvoiceItem(
                id=str(uuid.uuid4()),
                invoice_id=invoice_id,
                item_id=item.get('item_id'),
                quantity=item.get('quantity'),
                unit_price=item.get('unit_price'),
                total_price=total_price
            )
            db.add(invoice_item)

        # Set the overdue date, either provided or default (30 days from invoice date)
        # overdue_date = invoice_details.get('overdue_date', datetime.now() + timedelta(days=30))

        # Create the invoice with the calculated total amount
        invoice = Invoice(
            id=invoice_id,
            invoice_no=invoice_details.get("invoice_no"),
            organization_id=organization_id,
            creator_id=user_id,
            customer_id = invoice_details.get("customer_id"),   
            total_amount=total_amount,
            invoice_date=invoice_details.get("invoice_date"),
            overdue_date=invoice_details.get("overdue_date"),
            status=invoice_details.get('status', 'unpaid')
        )
        db.add(invoice)
        db.commit()

        invoice_responce ={
            "id" : invoice_id,
            "invoice_no":invoice_details.get("invoice_no"),
            "organization_id":organization_id,
            "creator_id":user_id,
            "customer_id" : invoice_details.get("customer_id"),   
            "total_amount":total_amount,
            "invoice_date": invoice_details.get("invoice_date").isoformat() if invoice_details.get("invoice_date") else None,
            "overdue_date": invoice_details.get("overdue_date").isoformat() if invoice_details.get("overdue_date") else None,
            "status":invoice_details.get('status', 'unpaid')
        }
        return JSONResponse({"Message": "Invoice created successfully", "Invoice_responce": invoice_responce})
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        db.close()


def get_invoice(invoice_id, org_id, user_data):
    try:
        # Fetch the invoice
        invoice = db.query(Invoice).filter_by(id=invoice_id, organization_id=org_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        # Serialize invoice details
        filter_data = serializer_for_invoice(invoice)

        return JSONResponse({"Invoices": filter_data})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving invoice: {str(e)}")
    finally:
        db.close()


def get_all_invoices(org_id, user_data):
    try:
        # Fetch all invoices for the given organization
        invoices = db.query(Invoice).options(joinedload(Invoice.items)).filter_by(organization_id=org_id).all()
        
        # Check if any invoices are found
        if not invoices:
            raise HTTPException(status_code=404, detail="No invoices found for this organization")
        
        # Serialize invoice details
        filter_data =[serializer_for_invoice(invoice) for invoice in invoices]

        return JSONResponse({"Invoices": filter_data})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving invoices: {str(e)}")
    finally:
        db.close()


def update_invoice(invoice_id, org_id, invoice_details, user_data):
    try:
        # Fetch the invoice
        invoice = db.query(Invoice).filter_by(id=invoice_id, organization_id=org_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Update invoice fields
        invoice.status = invoice_details.get('status') or invoice.status
        invoice.updated_at = datetime.now()

        db.commit()
        return JSONResponse({"Message": "Invoice updated successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating invoice: {str(e)}")
    finally:
        db.close()

def delete_invoice(invoice_id, org_id, user_data):
    try:
        # Fetch the invoice
        invoice = db.query(Invoice).filter_by(id=invoice_id, organization_id=org_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Delete the invoice
        db.delete(invoice)
        db.commit()
        return JSONResponse({"Message": "Invoice deleted successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting invoice: {str(e)}")
    finally:
        db.close()
