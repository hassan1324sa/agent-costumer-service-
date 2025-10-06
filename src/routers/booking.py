from fastapi import APIRouter, Request, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse
from helpers.config import getSettings, Settings
from models import ResponseEnum, BookingModel
from controllers.bookingController import BookingController

bookingRouter = APIRouter(prefix="/api/booking")
settings = getSettings()

@bookingRouter.post("/add/")
async def addBooking(
    request: Request,
    username: str,
    service_type: str,
    date: str,
    time: str,
    appSettings: Settings = Depends(getSettings),
    # _: None = Depends(verify_agent),  
):
    try:
        controller = BookingController()
        valid_date = controller.validate_date(date)
        valid_time = controller.validate_time(time)
        
        dbClient = request.app.db_client
        bookingModel = await BookingModel.createInstance(dbClient=dbClient)
        existing_booking = await bookingModel.isExist(
            filters={
                "username": username,
                "service_type": service_type,
                "date": valid_date, 
                "time": valid_time
            }
        )

        if existing_booking:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Booking already exists for this user, service, date, and time."
            )

        booking_id = await controller.createBooking(
            dbClient, username, service_type, str(valid_date).strip(), str(valid_time).strip()
        )

        return JSONResponse(
            content={
                "signal": ResponseEnum.dataAddedSuccessfully.value,
                "booking_id": str(booking_id)
            },
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error:", e)
        return JSONResponse(
            content={"signal": ResponseEnum.dataAddedError.value, "detail": str(e)},
            status_code=status.HTTP_400_BAD_REQUEST
        )

@bookingRouter.get("/all/")
async def getAllBookings(
    request: Request,
    appSettings: Settings = Depends(getSettings),
    # _: None = Depends(verify_agent), 
):
    dbClient = request.app.db_client
    bookingModel = await BookingModel.createInstance(dbClient=dbClient)

    try:
        user_bookings = await bookingModel.getBookings()

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