import os
from fastapi import FastAPI, File, UploadFile, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from src.models.login import LoginForm
from src.services.ui import return_gradio_ui
from starlette.middleware.sessions import SessionMiddleware
from fastapi import HTTPException, status
import yaml
from datetime import datetime
from contextlib import asynccontextmanager

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

def require_login(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user




@app.get("/health",)
async def home():
    return {"health": "good"}


router = APIRouter(prefix="/auth")

@app.get("/")
def sign_in_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login/")
async def login(request: Request):
    
    form = LoginForm(request)
    await form.load_data()

    username = form.username
    password = form.password


    if await form.is_valid():
        print("login success")
        request.session["user"] = username
        return RedirectResponse(url="/resume_ai", status_code=status.HTTP_303_SEE_OTHER)

    else:
        print("login failed")
        return templates.TemplateResponse("login.html", {"request": request, "username": form.username, "errors": form.errors})

@router.get("/logout/")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.get("/resume_ai")
async def resume_ai(request: Request, user_name = Depends(require_login)):
    return templates.TemplateResponse("sam.html", {"request": request, "username": user_name})


@app.get("/create")
async def create(request: Request, user_name = Depends(require_login)):
    return templates.TemplateResponse("create.html", {"request": request, "username": user_name})


@app.post("/generate_yaml")
async def generate(request: Request, user_name = Depends(require_login)):
    form = await request.form()

    # ---------- HEADER ----------
    header = {
        "name": form.get("header_name"),
        "contact": {
            "phone": form.get("header_phone"),
            "email": form.get("header_email"),
            "linkedin": form.get("header_linkedin")
        }
    }

    # ---------- SUMMARY ----------
    summary = form.get("summary")

    # ---------- EDUCATION ----------
    education = {
        "university": form.get("education_university"),
        "degree": form.get("education_degree"),
        "gpa": form.get("education_gpa"),
        "graduation_date": form.get("education_graduation_date")
    }

    # ---------- EXPERIENCES ----------
    exp_titles = form.getlist("experience_title")
    exp_companies = form.getlist("experience_company")
    exp_durations = form.getlist("experience_duration")
    exp_responsibilities = form.getlist("experience_responsibilities")

    experiences = []
    for i in range(len(exp_titles)):
        if exp_titles[i].strip():  # skip empty entries
            experiences.append({
                "title": exp_titles[i],
                "company": exp_companies[i],
                "duration": exp_durations[i],
                "responsibilities": [r.strip() for r in exp_responsibilities[i].split(",") if r.strip()]
            })

    # ---------- PROJECTS ----------
    proj_names = form.getlist("project_name")
    proj_descriptions = form.getlist("project_description")

    projects = []
    for i in range(len(proj_names)):
        if proj_names[i].strip():
            projects.append({
                "name": proj_names[i],
                "description": proj_descriptions[i]
            })

    # ---------- SKILLS ----------
    skill_category = form.get("skill_category", "").strip()
    skill_items = form.get("skill_items", "").strip()
    skills = {}
    if skill_category and skill_items:
        skills[skill_category] = [s.strip() for s in skill_items.split(",") if s.strip()]

    # ---------- AVAILABILITY ----------
    availability = form.get("availability")

    # ---------- FINAL DATA ----------
    yaml_data_dict = {
        "header": header,
        "summary": summary,
        "education": education,
        "experience": experiences,
        "projects": projects,
        "skills": skills,
        "availability": availability
    }

    # Convert to YAML string
    yaml_text = yaml.dump(yaml_data_dict, sort_keys=False, allow_unicode=True)
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d_%H-%M-%S")  
    output_dir = "yaml_files"
    os.makedirs(output_dir, exist_ok= True)
    file_name = f"{output_dir}/{header['name']}_{formatted_date}.yaml" 
    with open(file_name, "w") as f:
        f.write(yaml_text)


app = return_gradio_ui(app= app, auth_dependency= require_login)
app.include_router(router= router)