import os
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Query, Header
from pydantic import BaseModel, Field
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    DateTime,
    func,
    select,
    update,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./metaweb.db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class ModelConfigORM(Base):
    __tablename__ = "model_configs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, nullable=False)
    model = Column(String(128), nullable=False)
    temperature = Column(Float, nullable=False, default=0.7)
    max_tokens = Column(Integer, nullable=False, default=1000)
    system_prompt = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ModelConfigIn(BaseModel):
    model: str
    temperature: float = Field(ge=0.0, le=1.0, default=0.7)
    max_tokens: int = Field(gt=0, le=32768, default=1000)
    system_prompt: str = ""


class ModelConfigOut(BaseModel):
    id: int
    version: int
    model: str
    temperature: float
    max_tokens: int
    system_prompt: str | None
    is_active: bool
    created_at: datetime

    @classmethod
    def from_orm_row(cls, row: "ModelConfigORM"):
        return cls(
            id=row.id,
            version=row.version,
            model=row.model,
            temperature=row.temperature,
            max_tokens=row.max_tokens,
            system_prompt=row.system_prompt,
            is_active=row.is_active,
            created_at=row.created_at,
        )


def init_tables():
    Base.metadata.create_all(engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_admin_token(x_admin_token: str = Header(None)):
    token = os.environ.get("ADMIN_TOKEN", "")
    if token and x_admin_token != token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_admin_token


def get_active_config_row(db: Session) -> Optional[ModelConfigORM]:
    return (
        db.execute(
            select(ModelConfigORM)
            .where(ModelConfigORM.is_active.is_(True))
            .order_by(ModelConfigORM.id.desc())
        )
        .scalars()
        .first()
    )


router = APIRouter(prefix="/config", tags=["model-config"])


@router.get("/active", response_model=Optional[ModelConfigOut])
def get_active_config(db: Session = Depends(get_db)):
    row = get_active_config_row(db)
    return ModelConfigOut.from_orm_row(row) if row else None


@router.get("/history", response_model=List[ModelConfigOut])
def get_history(limit: int = Query(20, ge=1, le=200), db: Session = Depends(get_db)):
    rows = (
        db.execute(
            select(ModelConfigORM).order_by(ModelConfigORM.id.desc()).limit(limit)
        )
        .scalars()
        .all()
    )
    return [ModelConfigOut.from_orm_row(r) for r in rows]


@router.post("", response_model=ModelConfigOut)
def create_config(
    payload: ModelConfigIn,
    db: Session = Depends(get_db),
    admin_token: str = Depends(require_admin_token),
):
    last = (
        db.execute(select(ModelConfigORM.version).order_by(ModelConfigORM.version.desc()))
        .scalars()
        .first()
    )
    next_version = (last or 0) + 1

    row = ModelConfigORM(
        version=next_version,
        model=payload.model,
        temperature=payload.temperature,
        max_tokens=payload.max_tokens,
        system_prompt=payload.system_prompt or "",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return ModelConfigOut.from_orm_row(row)


@router.post("/{config_id}/publish")
def publish_config(
    config_id: int,
    db: Session = Depends(get_db),
    admin_token: str = Depends(require_admin_token),
):
    target = db.get(ModelConfigORM, config_id)
    if not target:
        raise HTTPException(404, "Config not found")

    db.execute(update(ModelConfigORM).values(is_active=False))
    target.is_active = True
    db.add(target)
    db.commit()
    return {
        "status": "ok",
        "active_id": target.id,
        "active_version": target.version,
    }
