from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..sso import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("login.html", {"request": request, "user": user})