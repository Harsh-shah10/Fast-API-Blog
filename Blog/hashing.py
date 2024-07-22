from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashPassword():
    def brcypt(password : str):
        return pwd_context.hash(password)

