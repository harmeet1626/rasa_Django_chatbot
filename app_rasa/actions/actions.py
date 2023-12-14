from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import logging
logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
import os
import django ,sys
# from channels.db import database_sync_to_async


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rasa_chatbot.settings')
import django
django.setup()

from api.models import Bookings
print("bookings",Bookings.objects.filter(id=1),"================")
import concurrent.futures
from django.utils import timezone







class BookTableAction(Action):
    def name(self) -> Text:
        return "action_book_table"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info("action called =======================================>")
        print(tracker.sender_id,"---")
        text =self.run_sync_method(tracker)
        dispatcher.utter_message(text =text)
        # Reset slots after booking
        return [SlotSet("cuisine", None),
                SlotSet("num_people", None),
                SlotSet("outdoor_seating", None)]
    
    def run_sync_method(self,tracker):
        # Replace with your actual synchronous method
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = executor.submit(self.query_your_model,tracker).result()
        return result


    def query_your_model(self, tracker):
        Bookings.objects.create(user_id = tracker.sender_id,
                        cuisine =tracker.get_slot("cuisine"),
                        people_num =tracker.get_slot("num_people"),
                        outdoor_seating =tracker.get_slot("outdoor_seating"),
                        booking_date = datetime.now()+timedelta(days=1)
                        )
        response_text = "Your booking has been made for 8PM sunday, and the booking details has been sent to your registered email"
        return response_text



class GetBookingDetailsAction(Action):
    def name(self) -> Text:
        return "get_booking_details"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info("get booking details action called =======================================>")
        print(tracker.sender_id,"---")
        response_array = self.run_sync_method(tracker)
        for res in response_array:
            dispatcher.utter_message(text=res)
        
    
    def run_sync_method(self,tracker):
        # Replace with your actual synchronous method
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = executor.submit(self.query_your_model,tracker).result()
        return result

    def query_your_model(self, tracker):
        booking = Bookings.objects.filter(user_id = tracker.sender_id, booking_date__gte = timezone.now()).last()
        response_text =[]
        if booking:
            hotel_name='Taj'
            print("booking.created_at",booking.created_at.date())
            response_text.append(f"Your latest bookings is done with Hotel {hotel_name} for {booking.people_num} people on {booking.booking_date.date()} at {booking.booking_date.time()}")
            
            if booking.booking_date > timezone.now():
                response_text.append("See you there :)")
        else:
            response_text.append("You do not have any active bookings")
            response_text.append("If you want then I can assist you in creating one.")
        return response_text



