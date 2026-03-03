from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, event


class Base(DeclarativeBase):
    pass


class TransactionType(str, PyEnum):
    """Enum to differentiate between income and expenses"""

    INCOME = "income"
    EXPENSE = "expense"


class Category(str, PyEnum):
    """Enum for expense categories"""

    FOOD = "food"
    TRANSPORTATION = "transportation"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    SHOPPING = "shopping"
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    OTHER = "other"


class PaymentMethod(str, PyEnum):
    """Enum for payment methods"""

    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    E_WALLET = "e_wallet"


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, index=True)
    sequence = Column(Integer, nullable=False, default=0)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(
        Enum(TransactionType), nullable=False, default=TransactionType.EXPENSE
    )
    category = Column(Enum(Category), nullable=False, default=Category.OTHER)
    payment_method = Column(
        Enum(PaymentMethod), nullable=False, default=PaymentMethod.CASH
    )
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    def __repr__(self):
        return f"<Expense(id={self.id}, description='{self.description}', amount={self.amount}, type={self.transaction_type})>"


@event.listens_for(Expense, "before_insert")
def generate_expense_id(mapper, connection, target):
    """Generate custom ID with format: INC:YYYY-MM-DD-XXXX or EXP:YYYY-MM-DD-XXXX"""
    if not target.id:
        # Get the prefix based on transaction type
        type_prefix = (
            "INC" if target.transaction_type == TransactionType.INCOME else "EXP"
        )

        # Get today's date
        today = datetime.utcnow().date()
        date_str = today.strftime("%Y-%m-%d")

        # Query database for the next sequence number for today
        from sqlalchemy import text

        # PostgreSQL syntax: SUBSTRING extracts the last 4 characters
        result = connection.execute(
            text(
                f"SELECT COALESCE(MAX(CAST(SUBSTRING(id FROM LENGTH(id)-3) AS INTEGER)), 0) + 1 FROM {Expense.__tablename__} WHERE id LIKE :pattern"
            ),
            {"pattern": f"{type_prefix}:{date_str}%"},
        )
        sequence_num = result.scalar() or 1

        # Generate the ID with 4-digit padded sequence
        target.id = f"{type_prefix}:{date_str}-{sequence_num:04d}"
        target.sequence = sequence_num
