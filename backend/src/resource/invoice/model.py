from sqlalchemy import Column, DateTime, Integer, ForeignKey, Numeric, String
from datetime import datetime
from sqlalchemy.orm import relationship
from backend.database.database import Base
from backend.src.resource.customer.model import Customer
from backend.src.resource.user.model import User
from backend.src.resource.items.model import Item
from backend.src.resource.organization.model import Organization


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(String, primary_key=True, index=True)
    invoice_date = Column(DateTime, default=datetime.now())
    invoice_no = Column(String, nullable=False)  # Invoice number should be unique in organization
    total_amount = Column(Numeric(10, 2), nullable=False)  # Total amount of the invoice
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    customer_id = Column(String, ForeignKey(Customer.id))
    organization_id = Column(String, ForeignKey(Organization.id))
    creator_id = Column(String, ForeignKey(User.id))

    # Relationships
    # organization = relationship("Organization", back_populates="invoices")
    # creator = relationship("User", back_populates="invoices")
    # invoice_items = relationship("InvoiceItem", back_populates="invoice")
    # customer = relationship("Customer", back_populates="invoices") 


class InvoiceItem(Base):
    __tablename__ = 'invoice_items'

    id = Column(String, primary_key=True, index=True)
    invoice_id = Column(String, ForeignKey(Invoice.id))
    item_id = Column(String, ForeignKey(Item.id))
    quantity = Column(Integer, default=1, nullable=False)  # Quantity of the item
    unit_price = Column(Numeric(10, 2), nullable=False)  # Unit price of the item
    total_price = Column(Numeric(10, 2), nullable=False)  # Total price (unit_price * quantity)

    # Relationships
    # invoice = relationship("Invoice", back_populates="invoice_items")
    # item = relationship("Item", back_populates="invoice_items")
