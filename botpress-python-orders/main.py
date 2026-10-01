from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base
from schemas import OrderCreate
from orders import create_order


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