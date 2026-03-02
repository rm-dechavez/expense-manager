from fastapi import APIRouter, HTTPException, status
from typing import List
from src.expense.expenses import expenses
from src.expense.schemas import Expense, ExpenseCreate, ExpenseUpdate


expense_router = APIRouter()


@expense_router.get("/", response_model=List[Expense])
async def get_expenses():
    return expenses


@expense_router.get("/{expense_id}")
async def get_expense(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )


@expense_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Expense)
async def create_expense(expense: ExpenseCreate) -> Expense:
    new_id = max(expense["id"] for expense in expenses) + 1
    new_expense = expense.model_dump()
    new_expense["id"] = new_id
    expenses.append(new_expense)
    return Expense(**new_expense)


@expense_router.put("/{expense_id}")
async def update_expense(expense_id: int, updated_expense: ExpenseUpdate) -> Expense:
    for expense in expenses:
        if expense["id"] == expense_id:
            updated_dict = updated_expense.model_dump(exclude_unset=True)
            expense.update(updated_dict)
            return Expense(**expense)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )


@expense_router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int):
    for i, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            del expenses[i]
            return {"message": "Expense deleted"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )
