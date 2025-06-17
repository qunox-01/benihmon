from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .sso import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("about.html", {"request": request, "user": user})

@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("contact.html", {"request": request, "user": user})

@router.get("/legal/privacy", response_class=HTMLResponse)
async def privacy_policy(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("legal/privacy.html", {"request": request, "user": user})

@router.get("/legal/cookies", response_class=HTMLResponse)
async def cookie_policy(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("legal/cookies.html", {"request": request, "user": user})

@router.get("/legal/tnc", response_class=HTMLResponse)
async def terms_and_conditions(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("legal/tnc.html", {"request": request, "user": user})

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("login.html", {"request": request, "user": user})

@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("signup.html", {"request": request, "user": user})


@router.get("/account", response_class=HTMLResponse)
async def account(request: Request, user: dict = Depends(get_current_user)):
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "user": None})
    return templates.TemplateResponse("account.html", {"request": request, "user": user})