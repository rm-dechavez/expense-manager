from pydantic import BaseModel
from typing import Optional


class Expense(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    payment_method: str
    date: str
    description: Optional[str] = None


class ExpenseCreate(BaseModel):
    amount: float
    type: str
    category: str
    payment_method: str
    date: str
    description: Optional[str] = None


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    payment_method: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
