from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import books, users, reminders, subscription_plan, rentals

app = FastAPI(title="Library Management API", version="1.0.0")

uploads_dir = Path(__file__).resolve().parent.parent / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost",
        "capacitor://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router, prefix="/api/books", tags=["Books"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["Reminders"])
app.include_router(subscription_plan.router, prefix="/api/subscription-plans", tags=["Subscription Plans"])
app.include_router(rentals.router, prefix="/api/checkouts", tags=["Checkouts"])
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.get("/")
def root():
    return {"message": "Library Management API is running"}