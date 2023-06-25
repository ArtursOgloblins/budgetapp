from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class CategoryBase(BaseModel):
    category: str


class CategoryResponseBase(BaseModel):
    category: str
    user_id: int

    class Config:
        orm_mode = True


class FinancesBase(BaseModel):
    date: datetime
    year: str
    month: str
    description: str
    category: str
    amount: float
    currency: str


class FinanceResponseBase(BaseModel):
    year: str
    month: str
    description: str
    category: str
    amount: float
    currency: str
    user_id: int

    class Config:
        orm_mode = True


class CreateExpensesCategory(CategoryBase):
    pass


class CreateIncomesCategory(CategoryBase):
    pass


class CreateExpenses(FinancesBase):
    pass


class CreateIncomes(FinancesBase):
    pass


class ExpensesCategoryResponse(CategoryResponseBase):
    pass


class IncomeCategoryResponse(CategoryResponseBase):
    pass


class ExpensesResponse(FinanceResponseBase):
    pass


class IncomesResponse(FinanceResponseBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

