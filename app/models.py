from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class ExpensesCategories(Base):
    __tablename__ = "expenses_categories"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class IncomeCategories(Base):
    __tablename__ = "income_categories"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    description = Column(String)
    category = Column(String)
    amount = Column(Float)
    currency = Column(String)


class Incomes(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    description = Column(String)
    category = Column(String)
    amount = Column(Float)
    currency = Column(String)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



