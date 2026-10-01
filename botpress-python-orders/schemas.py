from pydantic import BaseModel
from typing import List, Optional


class OrderItemCreate(BaseModel):

    product_code: str

    product_name: str

    quantity: int

    unit_price: float


class OrderCreate(BaseModel):

    customer_name: str

    phone: Optional[str] = None

    fulfillment_type: str

    location: Optional[str] = None

    payment_method: Optional[str] = None

    items: List[OrderItemCreate]