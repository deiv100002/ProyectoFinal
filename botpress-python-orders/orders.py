from datetime import datetime
from sqlalchemy.orm import Session

from models import Order, OrderItem


def generate_order_id(db: Session):
    today = datetime.now().strftime("%Y%m%d")
    count = db.query(Order).count() + 1

    return f"ORD-{today}-{count:03d}"


def create_order(db, order_data):
    order_id = generate_order_id(db)

    total = 0

    new_order = Order(
        order_id=order_id,
        customer_name=order_data.customer_name,
        phone=order_data.phone,
        fulfillment_type=order_data.fulfillment_type,
        location=order_data.location,
        payment_method=order_data.payment_method,
        status="PENDING_PAYMENT"
    )

    db.add(new_order)

    for item in order_data.items:
        subtotal = item.quantity * item.unit_price
        total += subtotal

        order_item = OrderItem(
            order_id=order_id,
            product_code=item.product_code,
            product_name=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=subtotal
        )

        db.add(order_item)

    new_order.total = total

    db.commit()
    db.refresh(new_order)

    return new_order


def get_all_orders(db: Session):
    return db.query(Order).all()


def get_order_by_id(db: Session, order_id: str):
    return (
        db.query(Order)
        .filter(Order.order_id == order_id)
        .first()
    )