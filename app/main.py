import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from . import routes
from .sso import get_google_sso_router, get_current_user

load_dotenv()

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include routers
google_sso_router = get_google_sso_router(os.getenv("GOOGLE_CLIENT_ID"), os.getenv("GOOGLE_CLIENT_SECRET"))
app.include_router(routes.router)
app.include_router(google_sso_router, prefix="/auth")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Custom exception handler for HTTP errors.
    """
    error_pages = {
        400: "error.html",
        404: "error.html",
        500: "error.html", # 505 is less common, using 500 for general server errors
    }
    template_name = error_pages.get(exc.status_code, "error.html")
    user = await get_current_user(request)
    return templates.TemplateResponse(
        template_name,
        {"request": request, "error_code": exc.status_code, "error_message": exc.detail, "user": user},
        status_code=exc.status_code,
    )

@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    data = """User-agent: *
Allow: /
"""
    return data

@app.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap(request: Request):
    """
    Generates a sitemap.xml for the website.
    """
    # In a real app, you would generate this from your database
    static_urls = [
        {"loc": str(request.url_for("index"))},
        {"loc": str(request.url_for("about"))},
        {"loc": str(request.url_for("contact"))},
        {"loc": str(request.url_for("privacy_policy"))},
        {"loc": str(request.url_for("cookie_policy"))},
        {"loc": str(request.url_for("terms_and_conditions"))},
        {"loc": str(request.url_for("login"))},
    ]

    xml_content = templates.get_template("sitemap.xml").render({"static_urls": static_urls})
    return PlainTextResponse(xml_content, media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)