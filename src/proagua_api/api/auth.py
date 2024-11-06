import datetime

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from ninja.security import APIKeyCookie
from ninja import Router
from ninja import Schema

import jwt
from jwt import DecodeError, ExpiredSignatureError

router = Router(tags=["Authentication"])


class JWTBearer(APIKeyCookie):
    param_name = "access_token"
    
    def authenticate(self, request, token):
        return JWTBearer.check_token(token)
    
    @classmethod
    def check_token(cls, token):
        try:
            # Try to decode the token
            payload = jwt.decode(
                jwt=token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except DecodeError as e:
            # Do not authorize if there is a decode error
            print("Ops! There is a DecodeError:", str(e))
            return False

        except ExpiredSignatureError as e:
            # Do not authorize if the token is expired
            print("Ops! The token is expired")
            return False
        
        return payload


def generate_auth_token(user: User) -> str | None:
    if user is None:
        return None
    
    issued_at = datetime.datetime.now()
    expiration_time = issued_at + datetime.timedelta(
        days=settings.JWT_EXPIRATION_TIME['days'],
        hours=settings.JWT_EXPIRATION_TIME['hours'],
        minutes=settings.JWT_EXPIRATION_TIME['minutes'],
        seconds=settings.JWT_EXPIRATION_TIME['seconds']
    )

    token = jwt.encode(
        payload={
            "id": user.id,
            "username": user.username,
            "iat": int(issued_at.timestamp()),
            "exp": int(expiration_time.timestamp())
        },
        key=settings.JWT_SECRET_KEY,
        headers={
            "alg": settings.JWT_ALGORITHM,
            "typ": "JWT"
        }
    )

    return token


class LoginCredentialsSchema(Schema):
    username: str
    password: str


@router.post("/login", auth=None)
def login(request, credentials: LoginCredentialsSchema):
    user = authenticate(request, **credentials.dict())
    if user is not None:
        token = generate_auth_token(user)
        response = JsonResponse({"success": True})
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True, 
            samesite='Strict'
        )
        return response


class TokenSchema(Schema):
    access_token: str


@router.post("/verify_token", auth=None)
def verify_token(request, data: TokenSchema):
    is_valid = JWTBearer.check_token(data.access_token)
    
    if not is_valid:
        return HttpResponse("Unauthorized", status=401)


@router.get('/logout')
def logout_api(request):
    logout(request)
    response = HttpResponse("Logged out")
    response.delete_cookie('csrftoken')
    response.delete_cookie('access_token')
    return response
