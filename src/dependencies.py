from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

__all__ = ('TokenBearer',)


class TokenBearer(HTTPBearer):

    def __init__(self, ):
        super().__init__(scheme_name='Token', description='Token')

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        return credentials.credentials
