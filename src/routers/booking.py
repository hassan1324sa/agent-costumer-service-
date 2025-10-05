from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from controllers.bookingController import BookingController
from helpers.config import getSettings, Settings
from models import ResponseEnum, BookingModel
from helpers.jsonEncoder import bson_to_json

bookingRouter = APIRouter(prefix="/api/booking")



@bookingRouter.post("/add/")
async def addBooking(request: Request, username: str, service_type: str, date: str, time: str, appSettings: Settings = Depends(getSettings)):
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
async def getAllBookings(request: Request, username: str, appSettings: Settings = Depends(getSettings)):
    dbClient = request.app.db_client
    bookingModel = await BookingModel.createInstance(dbClient=dbClient)

    try:
        user_bookings = await bookingModel.getBookings(username)
        user_bookings = bson_to_json(user_bookings)

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
