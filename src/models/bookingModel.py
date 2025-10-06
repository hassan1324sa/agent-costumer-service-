from models.dbSchemes import Booking
from datetime import datetime, timedelta

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
    
    async def getBookings(self):
        try:
            cursor = self.collection.find({})
            bookings = await cursor.to_list(length=None)
            return bookings
        except Exception as e:
            print("Error in getBookings:", e)
            return []
    
    async def isExist(self,filters):

        try:
            if not isinstance(filters,dict):
                raise ValueError("Filters must be a dictionary.")
            date= filters["date"].strftime("%Y-%m-%d")
            time =filters["time"].strftime("%I:%M %p")
            result = await self.collection.find_one({
                "date":date,
                "time":time,               
            })
            if result is not None:
                return True

            return result is not None 
        except Exception as e:
            print(f"Error in isExist: {e}")
            raise Exception(f"Failed to check booking existence: {str(e)}")