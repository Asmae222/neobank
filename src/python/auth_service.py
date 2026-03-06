from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import jwt
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# ✅ V4 CORRIGÉ : Secrets externalisés
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ✅ V2 CORRIGÉ : JWT avec expiration
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate(username, password, db)
    if not user:
        # ✅ V10 CORRIGÉ : Message générique
        logger.warning(f"Connexion échouée: {username}")
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    # ✅ V9 CORRIGÉ : Log connexion réussie
    logger.info(f"Connexion réussie user_id: {user.id}")
    token = create_access_token({"user_id": user.id, "role": user.role})
    return {"access_token": token}

@router.get("/account/{account_id}")
def get_account(account_id: str, token: str, db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    current_user_id = payload.get("user_id")

    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Compte introuvable")

    # ✅ V3 CORRIGÉ : Vérification IDOR
    if account.user_id != current_user_id:
        logger.warning(f"Accès non autorisé: {current_user_id} -> {account_id}")
        raise HTTPException(status_code=403, detail="Accès non autorisé")

    return account
