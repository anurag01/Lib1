from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.base import get_db
from app.models.user import SubscriptionPlan

router = APIRouter()


class SubscriptionPlanCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None
    duration_days: int = Field(gt=0)
    max_books: int = Field(ge=0, default=0)
    max_magazines: int = Field(ge=0, default=0)
    price: Decimal = Field(ge=0)
    is_active: bool = True


class SubscriptionPlanUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = None
    duration_days: Optional[int] = Field(default=None, gt=0)
    max_books: Optional[int] = Field(default=None, ge=0)
    max_magazines: Optional[int] = Field(default=None, ge=0)
    price: Optional[Decimal] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


class SubscriptionPlanResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    duration_days: int
    max_books: int
    max_magazines: int
    price: Decimal
    is_active: bool


@router.post("/", response_model=SubscriptionPlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(payload: SubscriptionPlanCreate, db: Session = Depends(get_db)):
    plan = SubscriptionPlan(**payload.model_dump())
    try:
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Plan name already exists")


@router.get("/", response_model=List[SubscriptionPlanResponse])
def get_plans(active_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(SubscriptionPlan)
    if active_only:
        query = query.filter(SubscriptionPlan.is_active.is_(True))
    return query.order_by(SubscriptionPlan.id.desc()).all()


@router.get("/{plan_id}", response_model=SubscriptionPlanResponse)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")
    return plan


@router.put("/{plan_id}", response_model=SubscriptionPlanResponse)
def update_plan(plan_id: int, payload: SubscriptionPlanUpdate, db: Session = Depends(get_db)):
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(plan, key, value)

    try:
        db.commit()
        db.refresh(plan)
        return plan
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Plan name already exists")


@router.patch("/{plan_id}/status", response_model=SubscriptionPlanResponse)
def update_plan_status(plan_id: int, is_active: bool, db: Session = Depends(get_db)):
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")

    plan.is_active = is_active
    db.commit()
    db.refresh(plan)
    return plan


@router.delete("/{plan_id}", status_code=status.HTTP_200_OK)
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")

    db.delete(plan)
    db.commit()
    return {"detail": "Subscription plan deleted successfully"}