from hashlib import sha256

def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()

def verify_password(input_password: str, stored_hash: str) -> bool:
    return hash_password(input_password) == stored_hash