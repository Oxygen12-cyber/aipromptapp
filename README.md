# **Prompt.ly:** AI Prompt Sharing Backend

A Twitter-like backend for sharing AI prompts, built with FastAPI and SQLAlchemy.

## Features

- 🔐 **JWT Authentication** - Secure user registration and login
- 📝 **Post Management** - Create, read, update, and delete AI prompts
- ❤️ **Like System** - Like and unlike posts with automatic like counting
- 🔍 **Search Functionality** - Search posts by title, content, tags, or LLM model
- 🏷️ **Categorization** - Organize posts by tags (technology, mechanics, engineering, etc.)
- 🤖 **LLM Tracking** - Track which LLM model each prompt worked with

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **JWT** - JSON Web Tokens for authentication
- **Bcrypt** - Password hashing
- **Pydantic** - Data validation

## Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and receive JWT token

### Users

- `GET /api/v1/users/me` - Get current user profile
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users/{user_id}/posts` - Get all posts by user

### Posts

- `POST /api/v1/posts` - Create new post (authenticated)
- `GET /api/v1/posts` - List all posts (with pagination)
- `GET /api/v1/posts/search?q={query}` - Search posts
- `GET /api/v1/posts/{post_id}` - Get specific post
- `PUT /api/v1/posts/{post_id}` - Update post (owner only)
- `DELETE /api/v1/posts/{post_id}` - Delete post (owner only)

### Likes

- `POST /api/v1/posts/{post_id}/like` - Like a post
- `DELETE /api/v1/posts/{post_id}/like` - Unlike a post
- `GET /api/v1/posts/{post_id}/likes` - Get all likes for a post
- `GET /api/v1/users/me/likes` - Get all posts liked by current user

## Example Usage

### Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepass123"
```

### Create a Post

```bash
curl -X POST "http://localhost:8000/api/v1/posts" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Great ChatGPT Prompt for Code Review",
    "content": "Act as a senior software engineer...",
    "tags": "technology",
    "llm_model": "gpt-4"
  }'
```

### Search Posts

```bash
curl "http://localhost:8000/api/v1/posts/search?q=technology"
```

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email
- `hashed_password` - Bcrypt hashed password
- `created_at` - Timestamp

### Posts Table
- `id` - Primary key
- `title` - Post title
- `content` - Post content
- `tags` - Category (technology, mechanics, engineering, etc.)
- `llm_model` - LLM model used
- `created_at` - Timestamp
- `user_id` - Foreign key to users

### Likes Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `post_id` - Foreign key to posts
- `created_at` - Timestamp
- Unique constraint on (user_id, post_id)

## License

MIT
