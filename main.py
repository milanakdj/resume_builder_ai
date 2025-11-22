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
import json
from datetime import datetime
import uvicorn

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

@app.get("/", )
def sign_in_form(request: Request, ):
    user = request.session.get("user")
    if user:
        return RedirectResponse(url="/resume_ai", status_code=status.HTTP_303_SEE_OTHER)
    else:
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


@app.post("/generate_json")
async def generate(request: Request, user_name = Depends(require_login)):
    form = await request.form()

    # ---------- HEADER ----------
    file_name = form.get("file_name")
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
    edu_universities = form.getlist("education_university")
    edu_degrees = form.getlist("education_degree")
    edu_gpas = form.getlist("education_gpa")
    edu_graduation_dates = form.getlist("education_graduation_date")

    education = []
    for i in range(len(edu_universities)):
        if edu_universities[i].strip():  # skip empty entries
            education.append({
                "university": edu_universities[i],
                "degree": edu_degrees[i],
                "gpa": edu_gpas[i],
                "graduation_date": edu_graduation_dates[i]
            })

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
    skill_names = form.getlist("skill_name")
    skill_descriptions = form.getlist("skill_description")

    skills = []
    for i in range(len(skill_names)):
        if skill_names[i].strip():
            skills.append({
                "name": skill_names[i],
                "description": skill_descriptions[i]
            })

    # ---------- AVAILABILITY ----------
    availability = form.get("availability")

    # ---------- FINAL DATA ----------
    data_dict = {
        "header": header,
        "summary": summary,
        "education": education,
        "experience": experiences,
        "projects": projects,
        "skills": skills,
        "availability": availability
    }

    # Add to a file
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d_%H-%M-%S")  
    output_dir = "json_files"
    os.makedirs(output_dir, exist_ok= True)
    output_file_name = f"{output_dir}/{file_name}_{formatted_date}.json" 
    with open(output_file_name, "w") as f:
        json.dump(data_dict, f, indent =4)

    return RedirectResponse(url="/resume_ai", status_code=status.HTTP_302_FOUND)


app = return_gradio_ui(app= app, auth_dependency= require_login)
app.include_router(router= router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
