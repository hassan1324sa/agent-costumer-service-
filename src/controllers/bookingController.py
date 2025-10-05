from models.bookingModel import BookingModel
from models.dbSchemes import Booking
from datetime import datetime

class BookingController:
    async def createBooking(self, dbClient, username, service_type, date, time):
        bookingModel = await BookingModel.createInstance(dbClient)
        booking = Booking(
            username=username,
            service_type=service_type,
            date=date,
            time=time,
            created_at=datetime.now()
        )
        return await bookingModel.createBooking(booking)

    async def getBookings(self, dbClient, username=None):
        bookingModel = await BookingModel.createInstance(dbClient)
        return await bookingModel.getBookings(username)
