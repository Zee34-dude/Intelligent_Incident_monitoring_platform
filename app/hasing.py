from passlib.context import CryptContext

pwd_cxt=CryptContext(schemes=['argon2'],deprecated='auto')
class Hash():
    def encrypt(password):
        hashedPassword =pwd_cxt.hash(password[:72])  
        return hashedPassword 
    
    def verify(hashed_password,plain_password):
        return pwd_cxt.verify(plain_password,hashed_password)