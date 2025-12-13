from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from ..models.like import Like


def create_like(db: Session, user_id: int, post_id: int) -> Optional[Like]:
    """Create a like. Returns None if already liked."""
    try:
        db_like = Like(user_id=user_id, post_id=post_id)
        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return db_like
    except IntegrityError:
        db.rollback()
        return None


def delete_like(db: Session, user_id: int, post_id: int) -> bool:
    """Delete a like. Returns True if deleted, False if not found."""
    db_like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == post_id
    ).first()
    
    if not db_like:
        return False
    
    db.delete(db_like)
    db.commit()
    return True


def get_likes_by_post(db: Session, post_id: int) -> List[Like]:
    """Get all likes for a post."""
    return db.query(Like).filter(Like.post_id == post_id).all()


def get_likes_by_user(db: Session, user_id: int) -> List[Like]:
    """Get all likes by a user."""
    return db.query(Like).filter(Like.user_id == user_id).all()


def check_user_liked_post(db: Session, user_id: int, post_id: int) -> bool:
    """Check if a user has liked a post."""
    like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == post_id
    ).first()
    return like is not None
