from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import logging
logger = logging.getLogger(__name__)
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import django ,sys
from datetime import datetime, timedelta
import os, random



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rasa_chatbot.settings')
import django
django.setup()
from api.models import Bookings, Restaurants
import concurrent.futures
from django.utils import timezone



class BookTableAction(Action):
    def name(self) -> Text:
        return "action_book_table"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

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
        all_restaurants = Restaurants.objects.all()
        booking = Bookings.objects.create(user_id = tracker.sender_id,
                        restaurant = random.choice(all_restaurants),
                        cuisine = tracker.get_slot("cuisine"),
                        people_num =tracker.get_slot("num_people"),
                        outdoor_seating =tracker.get_slot("outdoor_seating"),
                        booking_date = datetime.now()+timedelta(days=1)
                        )
        # response_text = f"A booking with {booking.ext_id} has been made for 8PM sunday, and the booking details has been sent to your registered email"
        hotel_name=['Taj', 'Social', 'The Great beer', 'The pirates', 'Pyramid' ]

        response_text=f"A booking with {booking.ext_id}\n at Hotel {booking.restaurant.name} \n for {booking.people_num} people \n on {booking.booking_date.date()} at {booking.booking_date.time()} \n has been created."

        return response_text


class GetActiveBookingDetailsAction(Action):
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
        try:
            bookings = Bookings.objects.filter(user_id = tracker.sender_id, booking_date__gte = timezone.now())
            response_text =[]
            if bookings:
                response_text.append(f"You have {len(bookings)} upcoming bookings.")
                for one_booking in   bookings: 
                    response_text.append(f"Booking id- {one_booking.ext_id} \n at Hotel {one_booking.restaurant.name} \n for {one_booking.people_num} people \n on {one_booking.booking_date.date()} at {one_booking.booking_date.time()}")
                response_text.append("See you there :)")
            else:
                response_text.append("You do not have any active bookings")
                response_text.append("If you want then I can assist you in creating one.")
            return response_text
        except Exception as E:
            print("E========================",E)

class GetlastFiveBookings(Action):
    def name(self) -> Text:
        return "get_last_five_bookings"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response_array = self.run_sync_method(tracker)
        print("response",response_array)
        if response_array["message"]== []:
            dispatcher.utter_message(text="Please select a booking",buttons =response_array["buttons"])
        else:
            for message in response_array['message']:
                dispatcher.utter_message(text=message)


    
    def run_sync_method(self,tracker):
        # Replace with your actual synchronous method
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = executor.submit(self.query_your_model,tracker).result()
        return result

    def query_your_model(self, tracker):
        try:
            bookings = Bookings.objects.filter(user_id = tracker.sender_id).order_by("-booking_date")[0:5]
            if bookings:
                response_text = {"message":[],"buttons":[]}
                for one_booking in   bookings: 
                    print("append")
                    response_text["buttons"].append({"payload": f'/provide_booking_id{{"booking_id":"{one_booking.ext_id}"}}',
                                        "title" : one_booking.restaurant.name,
                                        
                                        })
            else:
                response_text["message"].append("You do not have any active bookings")
                response_text["message"].append("If you want then I can assist you in creating one.")
            return response_text
        except Exception as E:
            print("E========================",E)



class CancelBookingAction(Action):
    def name(self) -> Text:
        return "action_cancel_booking"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response_array = self.run_sync_method(tracker)
        for res in response_array:
            dispatcher.utter_message(text=res)
        # Reset slots after booking
        return [SlotSet("booking_id", None),]
    
    def run_sync_method(self,tracker):
        # Replace with your actual synchronous method
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = executor.submit(self.query_your_model,tracker).result()
        return result

    def query_your_model(self, tracker):
        try:
            booking_id = tracker.get_slot("booking_id")
            booking = Bookings.objects.filter(ext_id = booking_id)
            print("booking==============>",booking)
            response_text = []
            if booking:
                booking.delete()

                response_text.append("Your Booking has been cancelled and the refund will be initiated based on the restaurant policy")
            else:
                if booking_id:
                    response_text.append(f"Sorry, We were not able to fetch the details of booking id {tracker.get_slot('booking_id')}.")
                else:
                    response_text.append(f"Sorry, We were not able to fetch the details of above booking id")
                response_text.append(f"Please re-check and enter the id again.")
            return response_text
        except Exception as e:
            print("error is============>",e)



class ValidateRestaurantForm(FormValidationAction):
    
    def name(self) -> Text:
        return "validate_restaurant_form"

    @staticmethod
    def cuisine_db() -> List[Text]:
        """Database of supported cuisines"""
        return ["caribbean", "chinese", "french"]

    def validate_cuisine(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if slot_value.lower() in self.cuisine_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"cuisine": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text="Sorry, We dont have any restaurant having this cuisine in your area")

            return {"cuisine": None}
        