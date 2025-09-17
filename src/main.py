import os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from src.models.login import LoginForm
from src.services.ui import return_gradio_ui

app = FastAPI()
# os.makedirs("static", exist_ok=True)
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

videos = []

@app.get("/health",)
async def home():
    return {"health": "good"}

templates = Jinja2Templates(directory="src/templates")
router = APIRouter(prefix="/auth")

@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login/")
async def login(request: Request):
    
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        print("login success")
        return templates.TemplateResponse("sam.html", {"request": request, "username": form.username})
    else:
        print("login failed")
        print(form.username, form.password)
        print(form.errors)  


# @app.get("/gradio_ui")
# async def gradio_ui(request: Request):
#     global app
#     return return_gradio_ui(app= app)
#     print(type(app))

app = return_gradio_ui(app= app)
app.include_router(router= router)