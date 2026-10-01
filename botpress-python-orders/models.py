from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    customer_name = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=True
    )

    fulfillment_type = Column(
        String,
        nullable=False
    )

    location = Column(
        String,
        nullable=True
    )

    payment_method = Column(
        String,
        nullable=True
    )

    total = Column(
        Float,
        default=0
    )

    status = Column(
        String,
        default="PENDING_PAYMENT"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(
        String,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    product_code = Column(String)

    product_name = Column(String)

    quantity = Column(Integer)

    unit_price = Column(Float)

    subtotal = Column(Float)

    order = relationship(
        "Order",
        back_populates="items"
    )