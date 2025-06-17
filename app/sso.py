import os
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from itsdangerous import URLSafeTimedSerializer

# This should be a securely generated key
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key")
serializer = URLSafeTimedSerializer(SECRET_KEY)

def get_google_sso_router(client_id: str, client_secret: str) -> APIRouter:
    router = APIRouter()
    oauth = OAuth()

    oauth.register(
        name='google',
        client_id=client_id,
        client_secret=client_secret,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    @router.get('/login/google')
    async def login_google(request: Request):
        redirect_uri = request.url_for('auth_google')
        return await oauth.google.authorize_redirect(request, redirect_uri)

    @router.get('/auth/google')
    async def auth_google(request: Request):
        token = await oauth.google.authorize_access_token(request)
        user = token['userinfo']
        request.session['user'] = dict(user)
        return RedirectResponse(url='/')

    @router.get('/logout')
    async def logout(request: Request):
        request.session.pop('user', None)
        return RedirectResponse(url='/')

    return router

async def get_current_user(request: Request):
    user = request.session.get('user')
    if user:
        return user
    return None