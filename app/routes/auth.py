# Import necessary libraries and modules
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from starlette.config import Config

# Import the dependency to get the current user from the dashboard route
from app.routes.dashboard import get_current_user

# Load environment variables from a .env file for configuration
# This is where you'll store your Google Client ID and Secret
config = Config(".env")

# Initialize the OAuth client with the loaded configuration
oauth = OAuth(config)

# Register the Google OAuth provider with the necessary details
# The server_metadata_url automatically fetches the required endpoints from Google
# The client_kwargs specifies the permissions (scopes) we are requesting
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

def get_google_sso_router():
    """
    Creates and returns an APIRouter for Google SSO authentication.
    This function encapsulates all authentication-related routes.
    """
    sso_router = APIRouter()

    @sso_router.route("/google/login", name="login_google")
    async def login(request: Request):
        """
        Redirects the user to Google's authentication page.
        The `redirect_uri` is the URL that Google will send the user back to
        after they have authenticated. We use `url_for` to generate this URL dynamically.
        """
        # The callback route is named 'auth_callback'
        redirect_uri = request.url_for("auth_callback")
        return await oauth.google.authorize_redirect(request, redirect_uri)

    @sso_router.route("/google/callback", name="auth_callback")
    async def auth_callback(request: Request):
        """
        Handles the callback from Google after successful authentication.
        It authorizes the access token and retrieves the user's information.
        The user's info is then stored in the session.
        """
        # Exchange the authorization code for an access token
        token = await oauth.google.authorize_access_token(request)
        # The user's profile information is included in the token
        user = token.get("userinfo")
        if user:
            # Store the user's information in the session
            request.session["user"] = dict(user)
        # Redirect the user to their dashboard after logging in
        return RedirectResponse(url="/dashboard")

    @sso_router.get("/logout", name="logout")
    async def logout(request: Request):
        """
        Logs the user out by clearing their session data.
        After clearing the session, it redirects the user to the homepage.
        """
        # Remove the user data from the session
        request.session.pop("user", None)
        # Redirect to the homepage
        return RedirectResponse(url="/")

    return sso_router
