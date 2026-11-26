from datetime import date
from pathlib import Path
import re
import sqlite3

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="Sankar Naik Banavathu | Portfolio")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
templates = Jinja2Templates(directory=ROOT / "templates")

SKILLS = [
    "Python",
    "SQL",
    "Statistics",
    "Data cleaning",
    "Exploratory data analysis",
    "Data visualisation",
    "Feature engineering",
    "Machine learning",
    "Deep learning",
    "Model evaluation",
    "FastAPI", 
    "Jinja2",
]
PROJECTS = [
    {
        "title": "Alcohol detection using voice modulation",
        "description": "An academic project exploring whether changes in speech "
                       "can help a deep learning model identify alcohol consumption.",
        "tech": ["Deep learning", "Speech analysis"],
    },
    {
        "title": "Emotion detection using voice modulation",
        "description": "A research project exploring how variations in a speaker’s "
                       "voice can help identify emotion.",
        "tech": ["Speech analysis"],
    },
    {
        "title": "Personal portfolio",
        "description": "A single-page portfolio that renders project data on the "
                       "server and remembers the visitor’s preferred theme.",
        "tech": ["Python", "FastAPI", "Jinja2"],
    },
]


def current_theme(request: Request) -> str:
    theme = request.cookies.get("theme", "light")
    return theme if theme in {"light", "dark"} else "light"


@app.get("/", response_class=HTMLResponse)
async def portfolio(request: Request, tech: str = "", contact: str = ""):
    selected = tech.strip()
    projects = [
        project for project in PROJECTS
        if not selected or any(tag.casefold() == selected.casefold()
                               for tag in project["tech"])
    ]
    context = {
        "request": request, "theme": current_theme(request), "year": date.today().year,
        "skills": SKILLS, "projects": projects, "selected": selected,
        "contact_status": contact,
        "tags": sorted({tag for project in PROJECTS for tag in project["tech"]}),
    }
    # Explicit rendering also supports the original FastAPI 0.100 template API.
    template = templates.get_template("index.html")
    context["url_for"] = request.url_for
    return HTMLResponse(template.render(context))


@app.post("/set-theme")
async def set_theme(request: Request):
    theme = "dark" if current_theme(request) == "light" else "light"
    response = RedirectResponse("/", status_code=303)
    response.set_cookie("theme", theme, max_age=2592000, httponly=True, samesite="lax")
    return response


@app.post("/contact")
def contact(name: str = Form(""), email: str = Form(""), message: str = Form("")):
    name, email, message = name.strip(), email.strip(), message.strip()
    valid = (0 < len(name) <= 80 and 0 < len(message) <= 2000
             and len(email) <= 254 and re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))
    if not valid:
        return RedirectResponse("/?contact=invalid#contact", status_code=303)

    # Keep local lab messages outside the repository and its static directory.
    data_dir = Path.home() / ".fastapi-portfolio"
    data_dir.mkdir(exist_ok=True)
    connection = sqlite3.connect(data_dir / "contact.sqlite3")
    try:
        with connection:
            connection.execute("CREATE TABLE IF NOT EXISTS messages "
                               "(name TEXT, email TEXT, message TEXT)")
            connection.execute("INSERT INTO messages VALUES (?, ?, ?)", (name, email, message))
    finally:
        connection.close()
    return RedirectResponse("/?contact=saved#contact", status_code=303)
