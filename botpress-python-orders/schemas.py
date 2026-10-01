from pydantic import BaseModel, Field
from typing import List, Optional


class OrderItemCreate(BaseModel):
    product_code: str
    product_name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class OrderCreate(BaseModel):
    customer_name: str
    phone: Optional[str] = None
    fulfillment_type: str
    location: Optional[str] = None
    payment_method: Optional[str] = None

    items: List[OrderItemCreate] = Field(min_length=1)  