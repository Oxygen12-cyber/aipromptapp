from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Post(Base):
    """Post model for AI prompts shared by users."""
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(100), nullable=False)  # Category: technology, mechanics, engineering, etc.
    llm_model = Column(String(100), nullable=False)  # e.g., "gpt-4", "claude-3", "gemini-pro"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    author = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    
    @property
    def likes_count(self) -> int:
        """Get the number of likes for this post."""
        return len(self.likes)
