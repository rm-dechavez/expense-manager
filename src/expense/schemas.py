from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.expense.models import TransactionType, Category, PaymentMethod


class ExpenseBase(BaseModel):
    description: str
    amount: float
    transaction_type: TransactionType
    category: Category
    payment_method: PaymentMethod


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    transaction_type: Optional[TransactionType] = None
    category: Optional[Category] = None
    payment_method: Optional[PaymentMethod] = None


class Expense(ExpenseBase):
    id: str
    sequence: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
