import os
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth

# This router will handle all authentication-related endpoints
router = APIRouter()

# Initialize OAuth for handling Google SSO
oauth = OAuth()

# This function creates and configures the Google SSO router.
# It's kept separate to allow for easy configuration from main.py.
def get_google_sso_router(google_client_id: str, google_client_secret: str):
    """
    Configures and returns the Google SSO routes.
    """
    # Register the Google OAuth client
    oauth.register(
        name='google',
        client_id=google_client_id,
        client_secret=google_client_secret,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    sso_router = APIRouter()

    @sso_router.route('/google/login')
    async def login(request: Request):
        """
        Redirects the user to Google's authentication page.
        """
        redirect_uri = request.url_for('auth_callback')
        return await oauth.google.authorize_redirect(request, redirect_uri)

    @sso_router.route('/google/callback')
    async def auth_callback(request: Request):
        """
        Handles the callback from Google after successful authentication.
        Sets the user's session data.
        """
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        if user:
            request.session['user'] = dict(user)
        return RedirectResponse(url='/account')

    return sso_router

# Dependency to get the current user from the session
async def get_current_user(request: Request):
    """
    A dependency that retrieves the current user from the session,
    if they are logged in. Returns None otherwise.
    """
    return request.session.get('user')

# Dedicated logout route
@router.get("/logout")
async def logout(request: Request):
    """
    Clears the user's session and logs them out.
    """
    request.session.pop('user', None)
    return RedirectResponse(url='/')

