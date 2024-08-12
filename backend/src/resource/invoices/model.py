from database.database import Base
from sqlalchemy import Column, DateTime,Integer,ForeignKey, Numeric
from datetime import datetime
from sqlalchemy.orm import relationship


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, index=True)
    invoice_date = Column(DateTime, default=datetime.now())
    total_amount = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    customer_id = Column(Integer, ForeignKey('customers.id'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    customer = relationship("Customer", back_populates="invoices")
    organization = relationship("Organization", back_populates="invoices")
    user = relationship("User", back_populates="invoices")
    invoice_items = relationship("InvoiceItem", back_populates="invoice")
    # payments = relationship("Payment", back_populates="invoice")
