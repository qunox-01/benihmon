from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..sso import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("about.html", {"request": request, "user": user})

@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("contact.html", {"request": request, "user": user})