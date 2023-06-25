from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    tags=['Categories']
)


@router.get("/expenses_cat", response_model=List[schemas.ExpensesCategoryResponse])
def get_expenses_categories(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM expenses_categories""")
    # expenses_cat = cursor.fetchall()
    expenses_cat = db.query(models.ExpensesCategories).filter(models.ExpensesCategories.user_id == current_user.id).all()
    if not expenses_cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Expenses categories were not found")
    return expenses_cat


@router.get("/incomes_cat", response_model=List[schemas.IncomeCategoryResponse])
def get_income_categories(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    income_cat = db.query(models.IncomeCategories).filter(models.IncomeCategories.user_id == current_user.id).all()
    if not income_cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Income categories were not found")
    return income_cat


@router.post("/expenses_cat", status_code=status.HTTP_201_CREATED, response_model=schemas.ExpensesCategoryResponse)
def create_expense_category(expenses_cat: schemas.CreateExpensesCategory, db: Session = Depends(get_db),
                            current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO expenses_categories (user_id, category) VALUES (%s, %s) RETURNING * """,
    # (expenses_cat.userId, expenses_cat.type))
    # new_expenses_cat = cursor.fetchone()
    # conn.commit()
    new_expenses_cat = models.ExpensesCategories(user_id=current_user.id, **expenses_cat.dict())
    db.add(new_expenses_cat)
    db.commit()
    db.refresh(new_expenses_cat)
    return new_expenses_cat


@router.post("/income_cat", status_code=status.HTTP_201_CREATED, response_model=schemas.IncomeCategoryResponse)
def create_income_category(income_cat: schemas.CreateIncomesCategory, db: Session = Depends(get_db),
                           current_user: int = Depends(oauth2.get_current_user)):
    new_incomes_cat = models.IncomeCategories(user_id=current_user.id, **income_cat.dict())
    db.add(new_incomes_cat)
    db.commit()
    db.refresh(new_incomes_cat)
    return new_incomes_cat


@router.put("/expenses_cat/{id}", response_model=schemas.ExpensesCategoryResponse)
def update_expenses_cat(id: int, expenses_cat: schemas.CreateExpensesCategory, db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    updated_category_query = db.query(models.ExpensesCategories).filter(models.ExpensesCategories.id == id)
    category = updated_category_query.first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'category: {type} does not exist.')

    if category.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action")

    updated_category_query.update(expenses_cat.dict(), synchronize_session=False)
    db.commit()

    return updated_category_query.first()


@router.put("/income_cat/{id}", response_model=schemas.IncomeCategoryResponse)
def update_income_cat(id: int, income_cat: schemas.CreateIncomesCategory, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    updated_category_query = db.query(models.IncomeCategories).filter(models.IncomeCategories.id == id)
    category = updated_category_query.first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'category: {type} does not exist.')

    if category.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action")

    updated_category_query.update(income_cat.dict(), synchronize_session=False)
    db.commit()

    return updated_category_query.first()

