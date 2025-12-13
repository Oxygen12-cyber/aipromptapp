from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from ..models.post import Post
from ..schemas.post import PostCreate, PostUpdate


def create_post(db: Session, post: PostCreate, user_id: int) -> Post:
    """Create a new post."""
    db_post = Post(
        title=post.title,
        content=post.content,
        tags=post.tags,
        llm_model=post.llm_model,
        user_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(db: Session, post_id: int) -> Optional[Post]:
    """Get a post by ID."""
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    """Get all posts with pagination."""
    return db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()


def get_posts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
    """Get all posts by a specific user."""
    return db.query(Post).filter(Post.user_id == user_id).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()


def search_posts(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[Post]:
    """Search posts by query (searches in title, content, tags, and llm_model)."""
    search_pattern = f"%{query}%"
    return db.query(Post).filter(
        or_(
            Post.title.ilike(search_pattern),
            Post.content.ilike(search_pattern),
            Post.tags.ilike(search_pattern),
            Post.llm_model.ilike(search_pattern)
        )
    ).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()


def update_post(db: Session, post_id: int, post_update: PostUpdate) -> Optional[Post]:
    """Update a post."""
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    
    update_data = post_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> bool:
    """Delete a post."""
    db_post = get_post(db, post_id)
    if not db_post:
        return False
    
    db.delete(db_post)
    db.commit()
    return True
