from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import logging
logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
import os
import django ,sys
sys.path.append('../')

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "/rasa_chat_app.settings")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rasa_chatbot.settings')

# path =os.getcwd()+"/rasa_chat_app/settings"
# print("patthhhhhhhhhhhhhhh",path)
django.setup()





class BookTableAction(Action):
    def name(self) -> Text:
        return "action_book_table"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info("action called =======================================>")
        from rasa_chat_app.models import Bookings
        try:
            Bookings.objects.create(user_id = 1,
                        cuisine =tracker.get_slot("cuisine"),
                        people_num =tracker.get_slot("num_people"),
                        outdoor_seating =tracker.get_slot("outdoor_seating"),
                        booking_date = datetime.now()+timedelta(days=1)
                        )
        except Exception as e:
            print("eroorororo======",e)


        dispatcher.utter_message(text ="Your booking has been made for 8PM sunday, and the booking details has been sent to your registered email")

        # Reset slots after booking
        return [SlotSet("cuisine", None),
                SlotSet("num_people", None),
                SlotSet("outdoor_seating", None)]
