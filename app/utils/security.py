from datetime import datetime, timedelta
from typing import Optional
import hashlib
import base64
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Uses SHA-256 pre-hashing to match the hashing process.
    """
    # Pre-hash with SHA-256 to match the hashing process
    password_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    
    return pwd_context.verify(password_hash, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt with SHA-256 pre-hashing.
    
    To handle bcrypt's 72-byte limitation properly, we first hash the password
    with SHA-256. This approach:
    - Supports passwords of any length
    - Preserves the full entropy of long passwords
    - Avoids silent truncation issues
    - Results in a consistent 64-character hex string input to bcrypt (well under 72 bytes)
    
    Args:
        password: The plain text password to hash
        
    Returns:
        The hashed password
    """
    # Pre-hash with SHA-256 to handle bcrypt's 72-byte limitation
    # This ensures passwords of any length are supported without truncation
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    return pwd_context.hash(password_hash)



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """Decode a JWT access token and return the username."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        return username
    except JWTError:
        return None
