
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    data = """User-agent: *
Allow: /
"""
    return data

@router.get("/sitemap.xml", response_class=PlainTextResponse)
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