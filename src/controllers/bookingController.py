from models.bookingModel import BookingModel
from models.dbSchemes import Booking
from datetime import datetime
from helpers.config import getSettings
from fastapi import HTTPException
import re

class BookingController:
    def __init__(self):
        self.settings = getSettings()

    async def createBooking(self, dbClient, username, service_type, date, time):
        bookingModel = await BookingModel.createInstance(dbClient)

        valid_date = self.validate_date(date)
        valid_time = self.validate_time(time)
        booking = Booking(
            username=username,
            service_type=service_type,
            date=valid_date.strftime("%Y-%m-%d"),
            time=valid_time.strftime("%I:%M %p"),
            created_at=datetime.now()
        )
        return await bookingModel.createBooking(booking)

    def validate_date(self, date_str: str):
        possible_formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]
        for fmt in possible_formats:
            try:
                date_obj = datetime.strptime(date_str.strip(), fmt).date()
                break
            except ValueError:
                date_obj = None

        if not date_obj:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD or similar.")

        if date_obj < datetime.now().date():
            raise HTTPException(status_code=400, detail="Date cannot be in the past.")

        return date_obj

    def validate_time(self, time_str: str):
        
        time_str = time_str.strip().upper().replace(".", "")
        time_str = re.sub(r"\s+", " ", time_str)

        match = re.match(r"^(\d{1,2})(?::?(\d{2}))?(?::?(\d{2}))?\s*(AM|PM)?$", time_str, re.IGNORECASE)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if match.group(2) else 0
            second = int(match.group(3)) if match.group(3) else 0
            meridiem = match.group(4)

            if meridiem:
                try:
                    result = datetime.strptime(f"{hour:02d}:{minute:02d}:{second:02d}{meridiem}", "%I:%M:%S%p").time()
                    return result
                except ValueError:
                    try:
                        result = datetime.strptime(f"{hour:02d}:{minute:02d}:{second:02d} {meridiem}", "%I:%M:%S %p").time()
                        return result
                    except ValueError:
                        try:
                            result = datetime.strptime(f"{hour:02d}:{minute:02d}{meridiem}", "%I:%M%p").time()
                            return result
                        except ValueError:
                            try:
                                result = datetime.strptime(f"{hour:02d}:{minute:02d} {meridiem}", "%I:%M %p").time()
                                return result
                            except ValueError:
                                print("Failed to parse with regex formats")
            else:
                try:
                    result = datetime.strptime(f"{hour:02d}:{minute:02d}:{second:02d}", "%H:%M:%S").time()
                    return result
                except ValueError:
                    try:
                        result = datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time()
                        return result
                    except ValueError:
                        print("Failed to parse 24-hour format")

        possible_formats = [
            "%I:%M:%S %p",  # 3:00:00 PM
            "%I:%M %p",     # 3:00 PM
            "%I %p",        # 3 PM
            "%I:%M:%S%p",   # 3:00:00PM
            "%I:%M%p",      # 3:00PM
            "%I%p",         # 3PM
            "%H:%M:%S",     # 15:00:00
            "%H:%M",        # 15:00
            "%H"            # 15
        ]
        for fmt in possible_formats:
            try:
                result = datetime.strptime(time_str, fmt).time()
                print(f"Parsed time with {fmt}: {result}")
                return result
            except ValueError:
                print(f"Failed to parse with {fmt}")
                continue