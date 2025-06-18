from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.get("/privacy-policy", response_class=HTMLResponse, name="privacy_policy")
async def privacy_policy(request: Request):
    return templates.TemplateResponse("legal/privacy.html", {"request": request})

@router.get("/cookie-policy", response_class=HTMLResponse, name="cookie_policy")
async def cookie_policy(request: Request):
    return templates.TemplateResponse("legal/cookies.html", {"request": request})

@router.get("/terms-and-conditions", response_class=HTMLResponse, name="terms_and_conditions")
async def terms_and_conditions(request: Request):
    return templates.TemplateResponse("legal/tnc.html", {"request": request})