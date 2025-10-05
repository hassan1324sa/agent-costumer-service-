from models.dbSchemes import Booking

class BookingModel:
    def __init__(self, db):
        self.db = db
        self.collection = db.get_collection("bookings")

    @classmethod
    async def createInstance(cls, dbClient):
        return cls(dbClient)

    async def createBooking(self, booking):
        try:
            result = await self.collection.insert_one(booking.model_dump())
            return result.inserted_id
        except Exception as e:
            print("Error in createBooking:", e)
            return None

    async def getBookings(self, username: str):
        try:
            cursor = self.collection.find({"username": username})
            bookings = await cursor.to_list(length=None)
            return bookings
        except Exception as e:
            print("Error in getBookings:", e)
            return []
