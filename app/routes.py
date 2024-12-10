import random

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import engine
from app.models import User, UserAuth, Vote, VoteCreate

router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/login")
def login(user_auth: UserAuth, session: Session = Depends(get_session)):
    query = select(User).where(User.email == user_auth.email)
    user = session.exec(query).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if user_auth.password != user.password:
        raise HTTPException(status_code=401, detail="Senha inválida")

    token = random.randint(0, 100)
    user.token = token
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "Login bem-sucedido!", "user_id": user.id, "token": user.token}


@router.post("/votes")
def register_vote(
    vote_data: VoteCreate,
    token: int,
    session: Session = Depends(get_session),
):
    user_query = select(User).where(User.id == vote_data.user_id)
    user = session.exec(user_query).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if user.token != token:
        raise HTTPException(status_code=400, detail="Token inválido")

    existing_vote_query = select(Vote).where(Vote.user_id == vote_data.user_id)
    existing_vote = session.exec(existing_vote_query).first()
    if existing_vote:
        raise HTTPException(
            status_code=400, detail="Voto já registrado para este usuário"
        )

    vote = Vote(**vote_data.model_dump())
    session.add(vote)
    session.commit()
    session.refresh(vote)

    return {"message": "Voto registrado com sucesso!", "vote_id": vote.id}
