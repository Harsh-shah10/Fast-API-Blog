# FastAPI Project

Welcome to the FastAPI Blog Project!

## Getting Started

### Prerequisites

- Python 3.8 or later
- `pip` (Python package installer)

## Installation and Running

```bash
# Clone the repository
git clone https://github.com/Harsh-shah10/Fast-API-Blog.git
cd Fast-API-Blog

# Create and activate a virtual environment
python -m venv env

# On Windows:
.\env\Scripts\activate

# On macOS/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server with live reloading
uvicorn main:app --reload

## Note
Modify the create_token function in your code to include the following constants for generating JWT tokens:
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

Explanation : 
SECRET_KEY: This is your secret key used for signing JWT tokens.
ALGORITHM: Specifies the hashing algorithm used to sign the tokens (HS256 in this case).
ACCESS_TOKEN_EXPIRE_MINUTES: Sets the expiration time for the access tokens (30 minutes in this example).

