from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    """Base post schema."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    tags: str = Field(..., min_length=1, max_length=100, description="Category: technology, mechanics, engineering, etc.")
    llm_model: str = Field(..., min_length=1, max_length=100, description="LLM model used: gpt-4, claude-3, gemini-pro, etc.")


class PostCreate(PostBase):
    """Schema for creating a new post."""
    pass


class PostUpdate(BaseModel):
    """Schema for updating a post."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    tags: Optional[str] = Field(None, min_length=1, max_length=100)
    llm_model: Optional[str] = Field(None, min_length=1, max_length=100)


class PostResponse(PostBase):
    """Schema for post response."""
    id: int
    user_id: int
    created_at: datetime
    likes_count: int
    
    class Config:
        from_attributes = True
