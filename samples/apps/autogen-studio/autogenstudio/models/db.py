from typing import Dict, Optional
from sqlmodel import JSON, Column, DateTime, Field, SQLModel, func
from datetime import datetime


class BaseDBModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(), sa_column=Column(
        DateTime(timezone=True), server_default=func.now()))  # pylint: disable=not-callable
    updated_at: datetime = Field(default=datetime.now(), sa_column=Column(
        DateTime(timezone=True), onupdate=func.now()))  # pylint: disable=not-callable
    user_id: Optional[str] = None


class Message(BaseDBModel, table=True):
    role: str
    content: str
    session_id: str
    meta: Optional[Dict] = Field(default={}, sa_column=Column(JSON))
