from fastapi import APIRouter, Request, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse
from helpers.config import getSettings, Settings
from models import ResponseEnum, BookingModel
from controllers.bookingController import BookingController
from bson import ObjectId

bookingRouter = APIRouter(prefix="/api/booking")
settings = getSettings()

async def verify_agent(authorization: str = Header(...)):
    if authorization != f"Bearer {settings.AGENT_SECRET_KEY}":
        raise HTTPException(status_code=403, detail="Unauthorized agent")


@bookingRouter.post("/add/")
async def addBooking(
    request: Request,
    username: str,
    service_type: str,
    date: str,
    time: str,
    appSettings: Settings = Depends(getSettings),
    _: None = Depends(verify_agent),  
):
    try:
        dbClient = request.app.db_client
        controller = BookingController()
        booking_id = await controller.createBooking(dbClient, username, service_type, date, time)
        return JSONResponse(
            content={
                "signal": ResponseEnum.dataAddedSuccessfully.value,
                "booking_id": str(booking_id)
            },
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        print("Error:", e)
        return JSONResponse(
            content={"signal": ResponseEnum.dataAddedError.value},
            status_code=status.HTTP_400_BAD_REQUEST
        )


@bookingRouter.get("/all/")
async def getAllBookings(
    request: Request,
    username: str,
    appSettings: Settings = Depends(getSettings),
    _: None = Depends(verify_agent), 
):
    dbClient = request.app.db_client
    bookingModel = await BookingModel.createInstance(dbClient=dbClient)

    try:
        user_bookings = await bookingModel.getBookings(username)

        for booking in user_bookings:
            booking["_id"] = str(booking["_id"])
            booking["created_at"] = str(booking["created_at"])

        return JSONResponse(
            content={
                "signal": ResponseEnum.dataFetchedSuccessfully.value,
                "data": user_bookings
            },
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        print("Error:", e)
        return JSONResponse(
            content={"signal": ResponseEnum.dataFetchError.value},
            status_code=status.HTTP_400_BAD_REQUEST
        )
