from passlib.context import CryptContext


class Hasher:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return Hasher.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password):
        return Hasher.pwd_context.hash(password)