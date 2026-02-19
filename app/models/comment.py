from sqlalchemy import Column, ForeignKey, Integer, String , DateTime, Text
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"), nullable=False)
    comment:Mapped[str] = mapped_column(String(125), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    
    #relationship
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
