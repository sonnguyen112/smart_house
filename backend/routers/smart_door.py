from fastapi import APIRouter, Request, Depends, HTTPException
import json
from sqlalchemy.orm import Session
from databases import models
from databases.database import get_db
from fastapi.templating import Jinja2Templates
import threading
from smart_door import control_door


router = APIRouter(
    prefix="/smart_door",
    tags=["Smart Door"]
)

templates = Jinja2Templates(directory="frontend/templates")

watching = None
smart_door = None
is_watching = False
@router.get("/")
async def control(request: Request, db: Session = Depends(get_db)):
    door = db.query(models.Device).filter(models.Device.name == "door").first()
    status = door.status
    global watching, smart_door
    f = open("/home/pi/data/smart_house/src/backend/extra_files/common_var_door_server.json")
    common_var = json.load(f)
    f.close()
    is_watching = common_var["is_watching"]
    if status == 1:
        print("On")
        if is_watching == False:
            common_var["is_watching"] = True
            f = open("/home/pi/data/smart_house/src/backend/extra_files/common_var_door_server.json", "w")
            json.dump(common_var, f)
            f.close()
            smart_door = control_door.SmartDoor()
            watching = threading.Thread(target=smart_door.watch)
            watching.start()
            # os.system("python3 smart_door/control_door.py")
    elif status == 0:
        print("Off")
        if watching != None:
            if watching.is_alive():
                smart_door.is_stop = True
    else:
        print("Error")
    return templates.TemplateResponse("smart_door.html", {"request": request, "status": status})


@router.get("/set_status")
async def update_device(status: int, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.name == "door").first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    device.status = status
    db.commit()
    return "Updated"


@router.get("/get_status")
async def get_status(db: Session = Depends(get_db)):
    door = db.query(models.Device).filter(models.Device.name == "door").first()
    status = door.status
    return status