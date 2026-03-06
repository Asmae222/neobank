from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
import os
from database import get_db

router = APIRouter()
Base = declarative_base()

# ✅ V4 CORRIGÉ : Secret externalisé
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ✅ Modèle SQLAlchemy
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    description = Column(String)
    amount = Column(Float)

# ✅ Schéma Pydantic de validation
class TransactionSearch(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50)
    keyword: str = Field(..., min_length=1, max_length=100)

# ✅ V1 CORRIGÉ : Requêtes paramétrées via ORM
@router.get("/transactions/search")
def search_transactions(user_id: str, keyword: str, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.description.ilike(f"%{keyword}%")
    ).all()
    return {"transactions": transactions}
