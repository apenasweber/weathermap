from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        authorization = await super().__call__(request)
        if authorization:
            if not self.verify_jwt(authorization):
                raise HTTPException(status_code=403, detail="Invalid or expired token!")
            return authorization.credentials
        else:
            raise HTTPException(status_code=403, detail="Not authenticated!")

    def verify_jwt(self, jwtoken: str) -> bool:
        payload = decodeJWT(jwtoken.credentials)
        return bool(payload)
