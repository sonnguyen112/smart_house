from fastapi import FastAPI, Request
#import RPi.GPIO as GPIO
from fastapi.templating import Jinja2Templates
import databases.models as models
from databases import database
import threading
from utils.util import update_wanIP, update_status_is_watching
from backend.routers import smart_door, water_spray

update_wanIP_thread = threading.Thread(target=update_wanIP)
update_wanIP_thread.start()

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)
templates = Jinja2Templates(directory="frontend/templates")

update_status_is_watching(False)

app.include_router(smart_door.router)
app.include_router(water_spray.router)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
