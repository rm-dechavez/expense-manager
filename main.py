from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional


app = FastAPI()


expenses = [
    {
        "id": 1,
        "amount": 100.0,
        "type": "expense",
        "category": "Food",
        "payment_method": "Credit Card",
        "date": "2022-01-01",
        "description": "Dinner at restaurant ABC",
    },
    {
        "id": 2,
        "amount": 50.0,
        "type": "expense",
        "category": "Entertainment",
        "payment_method": "Cash",
        "date": "2022-01-02",
        "description": "Movie tickets",
    },
    {
        "id": 3,
        "amount": 200.0,
        "type": "income",
        "category": "Salary",
        "payment_method": "Direct Deposit",
        "date": "2022-01-03",
        "description": "Monthly salary",
    },
    {
        "id": 4,
        "amount": 30.0,
        "type": "expense",
        "category": "Transportation",
        "payment_method": "Debit Card",
        "date": "2022-01-04",
        "description": "Gas for car",
    },
    {
        "id": 5,
        "amount": 75.0,
        "type": "expense",
        "category": "Groceries",
        "payment_method": "Credit Card",
        "date": "2022-01-05",
        "description": "Weekly groceries",
    },
]


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


@app.get("/expenses", response_model=List[Expense])
async def get_expenses():
    return expenses


@app.get("/expenses/{expense_id}")
async def get_expense(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )


@app.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=Expense)
async def create_expense(expense: ExpenseCreate) -> Expense:
    new_id = max(expense["id"] for expense in expenses) + 1
    new_expense = expense.model_dump()
    new_expense["id"] = new_id
    expenses.append(new_expense)
    return Expense(**new_expense)


@app.put("/expenses/{expense_id}")
async def update_expense(expense_id: int, updated_expense: ExpenseUpdate) -> Expense:
    for expense in expenses:
        if expense["id"] == expense_id:
            updated_dict = updated_expense.model_dump(exclude_unset=True)
            expense.update(updated_dict)
            return Expense(**expense)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )


@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int):
    for i, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            del expenses[i]
            return {"message": "Expense deleted"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )
