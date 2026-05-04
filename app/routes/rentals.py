from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.models.base import get_db
from app.models.book import Book
from app.models.user import Rental, User

router = APIRouter()


class CheckoutActionPayload(BaseModel):
    user_id: int
    book_id: int
    due_date: Optional[datetime] = None


class CheckoutRecord(BaseModel):
    id: int
    user_id: int
    book_id: int
    member_id: str
    member_name: str
    title: str
    author: str
    borrowed_date: Optional[datetime] = None
    returned_date: Optional[datetime] = None
    due_date: datetime
    status: str


def _book_or_404(db: Session, book_id: int) -> Book:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def _user_or_404(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def _serialize_record(rental: Rental, user: User, book: Book) -> CheckoutRecord:
    member_name = getattr(user, "name", None) or "Member"
    return CheckoutRecord(
        id=rental.id,
        user_id=user.id,
        book_id=book.id,
        member_id=f"#{user.id:05d}",
        member_name=member_name,
        title=book.title,
        author=book.author,
        borrowed_date=rental.rented_at,
        returned_date=rental.returned_at,
        due_date=rental.due_date,
        status=rental.status,
    )


def _refresh_book_availability(book: Book) -> None:
    book.is_available = book.available_copies > 0


@router.get("/", response_model=List[CheckoutRecord])
def list_checkouts(db: Session = Depends(get_db)):
    rentals = db.query(Rental).order_by(Rental.id.desc()).all()
    records: List[CheckoutRecord] = []
    for rental in rentals:
        user = _user_or_404(db, rental.user_id)
        book = _book_or_404(db, rental.book_id)
        records.append(_serialize_record(rental, user, book))
    return records


@router.post("/allocate", response_model=CheckoutRecord, status_code=status.HTTP_201_CREATED)
def allocate_book(payload: CheckoutActionPayload, db: Session = Depends(get_db)):
    user = _user_or_404(db, payload.user_id)
    book = _book_or_404(db, payload.book_id)

    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No copies available for allocation")

    rental = Rental(
        user_id=user.id,
        book_id=book.id,
        rented_at=datetime.utcnow(),
        due_date=payload.due_date or (datetime.utcnow() + timedelta(days=14)),
        is_returned=False,
        status="borrowed",
    )
    book.available_copies -= 1
    _refresh_book_availability(book)

    db.add(rental)
    db.commit()
    db.refresh(rental)
    db.refresh(book)
    return _serialize_record(rental, user, book)


@router.post("/reserve", response_model=CheckoutRecord, status_code=status.HTTP_201_CREATED)
def reserve_book(payload: CheckoutActionPayload, db: Session = Depends(get_db)):
    user = _user_or_404(db, payload.user_id)
    book = _book_or_404(db, payload.book_id)

    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No copies available for reservation")

    rental = Rental(
        user_id=user.id,
        book_id=book.id,
        rented_at=datetime.utcnow(),
        due_date=payload.due_date or (datetime.utcnow() + timedelta(days=3)),
        is_returned=False,
        status="reserved",
    )
    book.available_copies -= 1
    _refresh_book_availability(book)

    db.add(rental)
    db.commit()
    db.refresh(rental)
    db.refresh(book)
    return _serialize_record(rental, user, book)


@router.post("/{rental_id}/return", response_model=CheckoutRecord)
def return_book(rental_id: int, db: Session = Depends(get_db)):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Checkout record not found")
    if rental.is_returned:
        raise HTTPException(status_code=400, detail="Book is already returned")

    user = _user_or_404(db, rental.user_id)
    book = _book_or_404(db, rental.book_id)

    rental.returned_at = datetime.utcnow()
    rental.is_returned = True
    rental.status = "available"
    book.available_copies += 1
    _refresh_book_availability(book)

    db.commit()
    db.refresh(rental)
    db.refresh(book)
    return _serialize_record(rental, user, book)


@router.post("/{rental_id}/renew", response_model=CheckoutRecord)
def renew_book(rental_id: int, db: Session = Depends(get_db)):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Checkout record not found")
    if rental.is_returned:
        raise HTTPException(status_code=400, detail="Returned books cannot be renewed")

    user = _user_or_404(db, rental.user_id)
    book = _book_or_404(db, rental.book_id)

    rental.due_date = rental.due_date + timedelta(days=7)
    rental.renewal_count += 1
    rental.status = "renewed"

    db.commit()
    db.refresh(rental)
    return _serialize_record(rental, user, book)