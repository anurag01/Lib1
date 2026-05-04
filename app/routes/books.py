from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.base import get_db
from app.models.book import Book

router = APIRouter()

UPLOADS_DIR = Path(__file__).resolve().parent.parent.parent / "uploads" / "books"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    price: float
    genre: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    publisher: Optional[str] = None
    published_year: Optional[int] = None
    total_copies: int = 1


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    price: Optional[float] = None
    genre: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    publisher: Optional[str] = None
    published_year: Optional[int] = None
    total_copies: Optional[int] = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    price: float
    genre: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    publisher: Optional[str] = None
    published_year: Optional[int] = None
    total_copies: int
    available_copies: int


def _parse_optional_int(value: Optional[str]) -> Optional[int]:
    if value in (None, ""):
        return None
    return int(value)


def _parse_required_int(value: str) -> int:
    return int(value)


def _parse_required_float(value: str) -> float:
    return float(value)


def _save_uploaded_image(image: UploadFile) -> str:
    suffix = Path(image.filename or "cover").suffix or ".png"
    file_name = f"{uuid4().hex}{suffix}"
    file_path = UPLOADS_DIR / file_name
    with file_path.open("wb") as buffer:
        buffer.write(image.file.read())
    return f"/uploads/books/{file_name}"


@router.get("/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    title: str = Form(...),
    author: str = Form(...),
    isbn: str = Form(...),
    price: str = Form(...),
    genre: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    publisher: Optional[str] = Form(None),
    published_year: Optional[str] = Form(None),
    total_copies: str = Form("1"),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    image_url = _save_uploaded_image(image) if image and image.filename else None
    book = BookCreate(
        title=title,
        author=author,
        isbn=isbn,
        price=_parse_required_float(price),
        genre=genre,
        summary=summary,
        image_url=image_url,
        publisher=publisher,
        published_year=_parse_optional_int(published_year),
        total_copies=_parse_required_int(total_copies),
    )
    new_book = Book(
        **book.model_dump(),
        available_copies=book.total_copies,
        is_available=book.total_copies > 0,
    )

    try:
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Book with same ISBN may already exist")

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    title: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    isbn: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    genre: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    publisher: Optional[str] = Form(None),
    published_year: Optional[str] = Form(None),
    total_copies: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    payload = BookUpdate(
        **{
            key: value
            for key, value in {
                "title": title,
                "author": author,
                "isbn": isbn,
                "price": _parse_required_float(price) if price not in (None, "") else None,
                "genre": genre,
                "summary": summary,
                "image_url": _save_uploaded_image(image) if image and image.filename else None,
                "publisher": publisher,
                "published_year": _parse_optional_int(published_year),
                "total_copies": _parse_optional_int(total_copies),
            }.items()
            if value is not None
        }
    )

    update_data = payload.model_dump(exclude_unset=True)
    previous_total = book.total_copies
    previous_available = book.available_copies

    for field, value in update_data.items():
        setattr(book, field, value)

    if payload.total_copies is not None:
        checked_out_copies = max(previous_total - previous_available, 0)
        book.available_copies = max(book.total_copies - checked_out_copies, 0)

    book.is_available = book.available_copies > 0

    try:
        db.commit()
        db.refresh(book)
        return book
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Book with same ISBN may already exist")