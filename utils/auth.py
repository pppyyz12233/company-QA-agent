import hashlib
import secrets

def hash_password(password: str):
    if not password:
        raise ValueError("密码不能为空")

    salt = secrets.token_hex(16)
    salted = password + salt
    hashed = hashlib.sha256(salted.encode()).hexdigest()
    return f"{salt}${hashed}"

#验证密码
def verify_password(plain_password: str, hashed_password: str):
    if not plain_password or not hashed_password:
        return False

    # 分离盐值和哈希
    parts = hashed_password.split("$")
    if len(parts) != 2:
        return False

    salt = parts[0]
    stored_hash = parts[1]

    salted = plain_password + salt
    computed_hash = hashlib.sha256(salted.encode()).hexdigest()

    return computed_hash == stored_hash

