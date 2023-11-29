import time
from typing import Dict

import jwt

from app.core.settings import settings

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 1200}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"user_id": user_id, "access_token": token}


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else {}
    except jwt.exceptions.DecodeError as e:
        print(f"Decode error: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}
