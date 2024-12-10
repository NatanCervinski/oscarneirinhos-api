from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=100, description="Nome completo do usuário")
    email: str = Field(
        ..., unique=True, index=True, description="E-mail único do usuário"
    )
    password: str = Field(..., min_length=8, description="Senha do usuário")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Data de criação do usuário",
    )
    is_active: bool = Field(default=True, description="Indica se o usuário está ativo")
    token: Optional[int] = Field(
        default=None, description="Token de votação do usuário"
    )


class UserCreate(SQLModel):
    name: str = Field(..., max_length=100, description="Nome completo do usuário")
    email: str = Field(..., description="E-mail único do usuário")
    password: str = Field(..., min_length=8, description="Senha do usuário")


class UserAuth(SQLModel):
    email: str
    password: str


class UserResponse(SQLModel):
    id: int
    name: str
    email: str
    created_at: datetime
    is_active: bool


class Vote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        ..., foreign_key="user.id", description="ID do usuário que fez o voto"
    )
    movie_id: int = Field(..., description="ID do filme votado")
    director_id: int = Field(..., description="ID do diretor votado")
    token: int = Field(..., description="Token de votação usado para validar o voto")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Data em que o voto foi registrado",
    )


class VoteCreate(SQLModel):
    user_id: int
    movie_id: int
    director_id: int
    token: int


class VoteResponse(SQLModel):
    id: int
    user_id: int
    movie_id: int
    director_id: int
    token: int
    created_at: datetime
