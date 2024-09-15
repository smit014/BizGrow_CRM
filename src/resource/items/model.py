# The `Item` class represents an item with attributes such as name, description, purchase price, sell
# price, profit, organization ID, creator ID, creation timestamp, and update timestamp, with
# relationships to Organization, User, and InvoiceItem.
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base
from src.resource.user.model import User
from src.resource.organization.model import Organization

class Item(Base):
    __tablename__ = 'items'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    purchase_price = Column(Numeric(10, 2))  # Purchase price of the item
    sell_price = Column(Numeric(10, 2))  # Selling price of the item
    profit = Column(Numeric(10, 2))  # Selling price - Purchase price
    organization_id = Column(String, ForeignKey(Organization.id))  # Organization ID
    creator_id = Column(String, ForeignKey(User.id)) # User who created the item
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    # Relationships
    # organization = relationship("Organization", back_populates="items")
    # creator = relationship("User", back_populates="items")
    # invoice_items = relationship("InvoiceItem", back_populates="item")

#TODO: Add quantity when adding inventory
#TODO: Add image