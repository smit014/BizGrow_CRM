from sqlalchemy import Column, String, Numeric, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from backend.src.resource.user.model import User

class Item(Base):
    __tablename__ = 'items'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    purchase_price = Column(Numeric(10, 2))  # Purchase price of the item
    sell_price = Column(Numeric(10, 2))  # Selling price of the item
    profit = Column(Numeric(10, 2)) # selling price - purchase price 
    user_id = Column(String,ForeignKey(User.id), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    invoice_items = relationship("InvoiceItem", back_populates="item")
    inventory = relationship("Inventory", back_populates="item")

#todo : add quantity when add inventory
#todo : add image