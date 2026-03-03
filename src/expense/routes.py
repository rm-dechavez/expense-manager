from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.expense.models import Expense as ExpenseModel
from src.expense.schemas import Expense, ExpenseCreate, ExpenseUpdate
from src.db.main import get_db


expense_router = APIRouter()


@expense_router.get("/", response_model=List[Expense])
async def get_expenses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ExpenseModel))
    expenses = result.scalars().all()
    return expenses


@expense_router.get("/{expense_id}", response_model=Expense)
async def get_expense(expense_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ExpenseModel).where(ExpenseModel.id == expense_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    return expense


@expense_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Expense)
async def create_expense(expense: ExpenseCreate, db: AsyncSession = Depends(get_db)):
    new_expense = ExpenseModel(**expense.model_dump())
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    return new_expense


@expense_router.put("/{expense_id}", response_model=Expense)
async def update_expense(
    expense_id: str, updated_expense: ExpenseUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ExpenseModel).where(ExpenseModel.id == expense_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )

    update_data = updated_expense.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    await db.commit()
    await db.refresh(expense)
    return expense


@expense_router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ExpenseModel).where(ExpenseModel.id == expense_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )

    await db.delete(expense)
    await db.commit()
    return None
