from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class Tag(Base):
     
    __tablename__ = "tags"

    id: Mapped[int]= mapped_column(primary_key=True, nullable=False, index=True)
    word: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Relationships



