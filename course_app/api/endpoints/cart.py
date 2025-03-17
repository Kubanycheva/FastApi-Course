from course_app.db.models import Cart, CartItem, Course
from course_app.db.schema import CartSchema, CartItemSchema, CourseSchema, CarItemCreateSchema
from fastapi import APIRouter, Depends, HTTPException
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session

cart_router = APIRouter(prefix='/cart', tags=['Cart'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@cart_router.get('/', response_model=CartSchema)
async def cart_list(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail='Корзина не найдена')

    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    total_price = sum(db.query(Course.price).filter(Course.id == item.course_id).scalar() for item in cart_items)
    return {
        'id': cart.id,
        'user_id': cart.user_id,
        'items': cart.items,
        'total_price': total_price
    }


@cart_router.post('/', response_model=CartItemSchema)
async def cart_add(item_data: CarItemCreateSchema, user_id: int,
                   db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    course = db.query(Course).filter(Course.id == item_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail='Курс не найден')
    course_item = db.query(CartItem).filter(CartItem.cart_id == cart.id,
                              CartItem.course_id == item_data.course_id).first()

    if course_item:
        raise HTTPException(status_code=404, detail='Курс уже в корзине')
    cart_item = CartItem(cart_id=cart.id, course_id = item_data.course_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


@cart_router.delete('{course_id}')
async def cart_delete(course_id: int, user_id: int, db: SessionLocal = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail='Корзина не найдена')
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.course_id == course_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail='Курс отсутсвует в корзине')

    db.delete(cart_item)
    db.commit()
    return {'message': 'Курс удален'}

    db.delete()