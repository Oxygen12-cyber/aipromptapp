from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...dependencies import get_current_user
from ...schemas.like import LikeResponse
from ...schemas.post import PostResponse
from ...crud import like as like_crud
from ...crud import post as post_crud
from ...models.user import User

router = APIRouter()


@router.post("/posts/{post_id}/like", response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Like a post."""
    # Check if post exists
    post = post_crud.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Create like
    like = like_crud.create_like(db, user_id=current_user.id, post_id=post_id)
    if not like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this post"
        )
    
    return like


@router.delete("/posts/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unlike a post."""
    # Check if post exists
    post = post_crud.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Delete like
    deleted = like_crud.delete_like(db, user_id=current_user.id, post_id=post_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You have not liked this post"
        )


@router.get("/posts/{post_id}/likes", response_model=List[LikeResponse])
def get_post_likes(post_id: int, db: Session = Depends(get_db)):
    """Get all likes for a post."""
    # Check if post exists
    post = post_crud.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    likes = like_crud.get_likes_by_post(db, post_id=post_id)
    return likes


@router.get("/users/me/likes", response_model=List[PostResponse])
def get_my_liked_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all posts liked by the current user."""
    likes = like_crud.get_likes_by_user(db, user_id=current_user.id)
    
    # Get the posts from the likes
    posts = [post_crud.get_post(db, post_id=like.post_id) for like in likes]
    # Filter out None values in case a post was deleted
    posts = [post for post in posts if post is not None]
    
    return posts
