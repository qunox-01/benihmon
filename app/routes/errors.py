from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from .auth import get_current_user


templates = Jinja2Templates(directory="app/templates")

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Custom exception handler for HTTP errors.
    """
    error_pages = {
        400: "error.html",
        404: "error.html",
        500: "error.html",
    }
    template_name = error_pages.get(exc.status_code, "error.html")
    user = await get_current_user(request)
    return templates.TemplateResponse(
        template_name,
        {"request": request, "error_code": exc.status_code, "error_message": exc.detail, "user": user},
        status_code=exc.status_code,
    )