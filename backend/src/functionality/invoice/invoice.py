from backend.database.database import Sessionlocal
from backend.src.resource.invoice.model import Invoice, InvoiceItem
from backend.src.resource.customer.model import Customer
from backend.src.resource.organization.model import Organization
from backend.src.resource.user.model import User
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import uuid
from datetime import datetime

db = Sessionlocal()

def create_invoice(invoice_details, user_id):
    invoice_id = str(uuid.uuid4())
    try:
        # Retrieve the organization associated with the user
        organization_id = invoice_details.get('organization_id')
        organization = db.query(Organization).filter_by(id=organization_id).first()
        
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
        
        # Create the invoice
        invoice = Invoice(
            id=invoice_id,
            organization_id=organization_id,
            user_id=user_id,
            total_amount=invoice_details.get('total_amount'),
            invoice_date=datetime.now(),
            status=invoice_details.get('status', 'Pending')  # Default status is Pending
        )
        db.add(invoice)
        db.commit()

        # Add items to the invoice
        items = invoice_details.get('items', [])
        for item in items:
            invoice_item = InvoiceItem(
                id=str(uuid.uuid4()),
                invoice_id=invoice_id,
                product_id=item.get('product_id'),
                quantity=item.get('quantity'),
                unit_price=item.get('unit_price'),
                total_price=item.get('quantity') * item.get('unit_price')
            )
            db.add(invoice_item)

        db.commit()

        return JSONResponse({"Message": "Invoice created successfully", "Invoice_id": invoice_id})
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        db.close()

def get_invoice(invoice_id, user_data):
    try:
        # Fetch the invoice
        invoice = db.query(Invoice).filter_by(id=invoice_id, organization_id=user_data.get('organization_id')).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        # Optional: Serialize the invoice details here
        invoice_data = {
            "id": invoice.id,
            "invoice_no": invoice.invoice_no,
            "total_amount": invoice.total_amount,
            "invoice_date": invoice.invoice_date,
            "customer_id": invoice.customer_id,
        }

        return JSONResponse({"Invoice": invoice_data})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving invoice: {str(e)}")
    finally:
        db.close()

def update_invoice(invoice_id, invoice_details, user_data):
    try:
        # Fetch the invoice
        invoice = db.query(Invoice).filter_by(id=invoice_id, organization_id=user_data.get('organization_id')).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Update invoice fields
        invoice.invoice_no = invoice_details.get('invoice_no') or invoice.invoice_no
        invoice.total_amount = invoice_details.get('total_amount') or invoice.total_amount
        invoice.updated_at = datetime.now()

        db.commit()
        return JSONResponse({"Message": "Invoice updated successfully"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating invoice: {str(e)}")
    finally:
        db.close()

def delete_invoice(invoice_id, user_data):
    try:
        # Fetch the invoice
        invoice = db.query(Invoice).filter_by(id=invoice_id, organization_id=user_data.get('organization_id')).first()
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
