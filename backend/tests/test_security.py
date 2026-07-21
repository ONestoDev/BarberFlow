from src.shared.security.passwords import hash_password, verify_password
from src.shared.security.tokens import create_access_token, decode_access_token


def test_password_hash_is_not_plain_text_and_can_be_verified():
    password_hash = hash_password("uma-senha-segura")

    assert password_hash != "uma-senha-segura"
    assert verify_password("uma-senha-segura", password_hash)
    assert not verify_password("senha-incorreta", password_hash)


def test_access_token_contains_subject():
    token = create_access_token("user-id")

    assert decode_access_token(token) == "user-id"
