from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base
from schemas import OrderCreate
from orders import create_order, get_all_orders, get_order_by_id


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Order Management API",
    version="1.0"
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "AI Order Management API is running"
    }


@app.post("/orders")
def create_new_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    new_order = create_order(db, order)

    return {
        "order_id": new_order.order_id,
        "customer": new_order.customer_name,
        "total": new_order.total,
        "status": new_order.status
    }


@app.get("/orders")
def list_orders(
    db: Session = Depends(get_db)
):
    orders = get_all_orders(db)

    results = []

    for order in orders:
        results.append({
            "order_id": order.order_id,
            "customer": order.customer_name,
            "phone": order.phone,
            "fulfillment_type": order.fulfillment_type,
            "location": order.location,
            "payment_method": order.payment_method,
            "total": order.total,
            "status": order.status,
            "created_at": order.created_at
        })

    return results


@app.get("/orders/{order_id}")
def get_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    order = get_order_by_id(db, order_id)

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    items = []

    for item in order.items:
        items.append({
            "product_code": item.product_code,
            "product_name": item.product_name,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "subtotal": item.subtotal
        })

    return {
        "order_id": order.order_id,
        "customer": order.customer_name,
        "phone": order.phone,
        "fulfillment_type": order.fulfillment_type,
        "location": order.location,
        "payment_method": order.payment_method,
        "items": items,
        "total": order.total,
        "status": order.status,
        "created_at": order.created_at
    }