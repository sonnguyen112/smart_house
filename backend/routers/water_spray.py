from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from databases import models
from databases.database import get_db
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/water_spray",
    tags=["Water Spray"]
)

templates = Jinja2Templates(directory="backend/templates")

@router.get("/")
async def control(request: Request,db: Session = Depends(get_db)):
    faucet = db.query(models.Device).filter(models.Device.name == "faucet").first()
    status = faucet.status
    if status == 1:
        print("On")
    elif status == 0:
        print("Off")
    else:
        print("Error")
    # elif status == 1 and type == "fan":
    #     print("on fan")
    #     # try:
    #     #     ser2.write(b'1')
    #     # except:
    #     #     pass
    # elif status == 0 and type == "fan": 
    #     print("off fan")
    #     # try:
    #     #     ser2.write(b'0')
    #     # except:
    #     #     pass
    # else:
    #     print("off all")
    #     #ser.write(b'0')
    #     # try:
    #     #     ser2.write(b'0')
    #     # except:
    #     #     # ser2 = serial.Serial("/dev/rfcomm2", 9600, timeout = 1)
    #     #     pass
        
    return templates.TemplateResponse("smart_garden.html", {"request": request, "status": status})