# The above class defines SQLAlchemy models for invoices and invoice items with relationships to
# customers, users, items, and organizations.
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Numeric, String
from datetime import datetime
from sqlalchemy.orm import relationship
from database.database import Base
from src.resource.customer.model import Customer
from src.resource.user.model import User
from src.resource.items.model import Item
from src.resource.organization.model import Organization


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(String, primary_key=True, index=True)
    invoice_date = Column(DateTime)
    invoice_no = Column(String, nullable=True)  # Invoice number should be unique in organization
    total_amount = Column(Numeric(10, 2), nullable=False)  # Total amount of the invoice
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    customer_id = Column(String, ForeignKey(Customer.id))
    organization_id = Column(String, ForeignKey(Organization.id))
    creator_id = Column(String, ForeignKey(User.id))
    overdue_date = Column(DateTime) # overdue date for invoice
    status = Column(String,nullable=False)

    # Define relationship with InvoiceItem
    items = relationship('InvoiceItem', back_populates='invoice')
    # Relationships
    # organization = relationship("Organization", back_populates="invoices")
    # creator = relationship("User", back_populates="invoices")
    # invoice_items = relationship("InvoiceItem", back_populates="invoice")
    # customer = relationship("Customer", back_populates="invoices") 
    def to_dict(self):
        return {
            "id": self.id,
            "total_amount": self.total_amount,
            "invoice_date": self.invoice_date,
            "status": self.status
            # Include other fields as needed
        }

class InvoiceItem(Base):
    __tablename__ = 'invoice_items'

    id = Column(String, primary_key=True, index=True)
    invoice_id = Column(String, ForeignKey(Invoice.id))
    item_id = Column(String, ForeignKey(Item.id))
    quantity = Column(Integer, default=1, nullable=False)  # Quantity of the item
    unit_price = Column(Numeric(10, 2), nullable=False)  # Unit price of the item
    total_price = Column(Numeric(10, 2), nullable=False)  # Total price (unit_price * quantity)

    # Define back reference to Invoice
    invoice = relationship('Invoice', back_populates='items')
    # Relationships
    # invoice = relationship("Invoice", back_populates="invoice_items")
    # item = relationship("Item", back_populates="invoice_items")
