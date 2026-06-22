from pwdlib import PasswordHash

# 1  비밀번호 해싱 설정 객체 생성
password_hash = PasswordHash.recommended()

# 2 평문 비밀번호를 해시 문자열로 변환
def hash_password(plain_password: str):
    return password_hash.hash(plain_password)

# 평문 비밀번호와 해시값 비교
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)