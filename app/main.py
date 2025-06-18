import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

# --- Route and Handler Imports ---
# The structure is now very clean: feature-based modules for routes.
from .routes import index, login, signup, dashboard, pages, seo, auth
from .routes.errors import http_exception_handler

# Load environment variables from .env file
load_dotenv()

# Get the application version from environment variables, with a default
APP_VERSION = os.getenv("APP_VERSION", "0.0.1")

# Initialize the FastAPI application
app = FastAPI(
    title="Serindit",
    description="A modern web application boilerplate.",
    version=APP_VERSION
)

# --- Middleware and Exception Handling ---

# Register the custom exception handler for HTTP errors
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

# Add session middleware, essential for authentication to work
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))


# --- Static Files and Templates ---

# Mount the 'static' directory to serve files like CSS, JS, and images
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up Jinja2 templates and make the app version available globally
templates = Jinja2Templates(directory="app/templates")
templates.env.globals['APP_VERSION'] = APP_VERSION


# --- Router Inclusion ---

# Get the Google SSO router from the new auth module
google_sso_router = auth.get_google_sso_router(
    os.getenv("GOOGLE_CLIENT_ID"),
    os.getenv("GOOGLE_CLIENT_SECRET")
)

# Include all the modular routers from the 'routes' directory
app.include_router(index.router, tags=["General"])
app.include_router(pages.router, tags=["General"])
app.include_router(seo.router, tags=["SEO"])
app.include_router(login.router, tags=["User"])
app.include_router(signup.router, tags=["User"])
app.include_router(dashboard.router, tags=["User"])
# Include the main auth router (for /logout) and the SSO router (for /auth/google/*)
app.include_router(auth.router, tags=["Authentication"])
app.include_router(google_sso_router, prefix="/auth", tags=["Authentication"])


# --- Application Startup ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
