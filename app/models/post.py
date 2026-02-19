from typing import List

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from app.models import User, Like, Comment, Tag, Image
from ..database import Base


class Post(Base):
    """Post model for AI prompts shared by users."""
    
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[str] = mapped_column(String(100), nullable=False)  
    llm_model: Mapped[str] = mapped_column(String(100), nullable=False)  
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    # additonal Relationships
    tags: Mapped[List[Tag]] = relationship("Tag")
    
    @property
    def likes_count(self) -> int:
        """Get the number of likes for this post."""
        return len(self.likes)
    
    @property
    def comment_count(self) -> int:
        #total number of comment on this post
        return len(self.comments)
    
    @property
    def image_count(self) -> int:
        # total number of images in the post
        return len(self.images)
