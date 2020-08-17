# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
import requests
import string


class GetCovidStateCount(Action):
    def name(self) -> Text:
        return "action_get_state_count"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = 'No such location present in India.'

        response = requests.get("https://api.covid19india.org/data.json").json()

        location = tracker.get_slot("location")

        if(str(location).lower == 'india'):
            for jobj in response["statewise"]:
                if(jobj["state"].lower().strip() == "total"):
                    message = "The current stats in {} is : \nConfirmed : {}\nActive : {}\nDeaths : {}\nRecovered : {}\nLast Updated : {}".format(location, jobj["confirmed"],
                    jobj["active"], jobj["deaths"], jobj["recovered"], jobj['lastupdatedtime'])
                    break
        
        else:
            for jobj in response["statewise"]:
                if(str(jobj["state"]).lower().strip() == str(location).lower().strip()):
                    message="The current stats in {} is : \nConfirmed : {}\nActive : {}\nDeaths : {}\nRecovered : {}\nLast Updated : {}".format(location, jobj["confirmed"],
                    jobj["active"], jobj["deaths"], jobj["recovered"], jobj['lastupdatedtime'])
                    break
        
        dispatcher.utter_message(text=message)

        return [AllSlotsReset()]
