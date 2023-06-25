from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    tags=['Finance']
)


@router.get("/expenses", response_model=List[schemas.ExpensesResponse])
def get_expenses(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,
                 skip: int = 0, search: Optional[str] = ""):
    expenses = (
        db.query(models.Expenses)
        .filter(models.Expenses.user_id == current_user.id,
                models.Expenses.description.contains(search))
        .limit(limit)
        .offset(skip)
        .all())
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Expenses were not found")
    return expenses


@router.get("/expenses/{category}", response_model=List[schemas.ExpensesResponse])
def get_expenses_by_cat(category: str, db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    expenses = db.query(models.Expenses).filter(models.Expenses.user_id == current_user.id,
                                                models.Expenses.category == category).all()
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category '{category}' was not found in expenses")
    return expenses


@router.get("/incomes", response_model=List[schemas.IncomesResponse])
def get_incomes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    incomes = db.query(models.Incomes).filter(models.Incomes.user_id == current_user.id).all()
    if not incomes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"EIncomes were not found")
    return incomes


@router.get("/incomes/{category}", response_model=List[schemas.IncomesResponse])
def get_incomes_by_cat(category: str, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    incomes = db.query(models.Incomes).filter(models.Incomes.user_id == current_user.id,
                                              models.Incomes.category == category).all()
    if not incomes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category '{category}' was not found in incomes")
    return incomes


@router.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=schemas.ExpensesResponse)
def create_expense(expense: schemas.CreateExpenses, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    new_expense = models.Expenses(user_id=current_user.id, **expense.dict())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.post("/incomes", status_code=status.HTTP_201_CREATED, response_model=schemas.IncomesResponse)
def create_income(income: schemas.CreateIncomes, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    new_income = models.Incomes(user_id=current_user.id, **income.dict())
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income


@router.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expenses(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_expense_query = db.query(models.Expenses).filter(models.Expenses.id == id)
    deleted_expense = deleted_expense_query.first()

    if deleted_expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'expense with id: {id} does not exist.')

    if deleted_expense.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action")

    deleted_expense_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/incomes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incomes(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_income_query = db.query(models.Incomes).filter(models.Incomes.id == id)
    deleted_income = deleted_income_query.first()

    if deleted_income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'income with id: {id} does not exist.')

    if deleted_income.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action")

    deleted_income_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/expenses/{id}", response_model=schemas.ExpensesResponse)
def update_expense(id: int, expenses: schemas.CreateExpenses, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    updated_expense_query = db.query(models.Expenses).filter(models.Expenses.id == id)
    expense = updated_expense_query.first()
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'expense with id: {id} does not exist.')

    if expense.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action")

    updated_expense_query.update(expenses.dict(), synchronize_session=False)
    db.commit()

    return updated_expense_query.first()


@router.put("/incomes/{id}", response_model=schemas.IncomesResponse)
def update_income(id: int, incomes: schemas.CreateIncomes, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    updated_income_query = db.query(models.Incomes).filter(models.Incomes.id == id)
    income = updated_income_query.first()

    if income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'income with id: {id} does not exist.')

    if income.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action")

    updated_income_query.update(incomes.dict(), synchronize_session=False)
    db.commit()

    return updated_income_query
