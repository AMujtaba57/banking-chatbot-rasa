# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests, json
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


def check_missing(tracker):
    missing = []

    for slot in tracker.slots:
        if tracker.get_slot(slot) is None:
            missing.append(slot)

    return missing


class ActionMakeTransaction(Action):

    def name(self) -> Text:
        return "action_make_transaction"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        events = tracker.current_state()['events']
        user_events = []
        for e in events:
            if e['event'] == 'user':
                user_events.append(e)

        custom_data = user_events[-1]['metadata']

        return_slots = []
        missing_slots = check_missing(tracker)

        url = "http://127.0.0.1:8000/make-transaction/"

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "cookie": "csrftoken={}; sessionid={}".format(custom_data['csrf'], custom_data['sessionid'])
        }

        if 'amount-of-money' in missing_slots:
            dispatcher.utter_message(text="How much amount ?")
            return []

        if 'transaction-type' in missing_slots:
            dispatcher.utter_message(response='utter_w_or_d')
            return []

        data = f"csrfmiddlewaretoken={custom_data['csrfmw']}&amount={tracker.get_slot('amount-of-money').replace(',','')}&transaction_type={tracker.get_slot('transaction-type').capitalize()}&source=Other"
        print(data)
        x = requests.post(url, data=data, headers=headers)
        # try:
        dispatcher.utter_message(text=f"{json.loads(x.json())['Message']}")
        # except:
        #   dispatcher.utter_message(text=f"{x.json()}")
        return_slots.append(SlotSet('amount-of-money', None))
        return_slots.append(SlotSet('transaction-type', None))
        return return_slots


class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return_slots = []
        missing_slots = check_missing(tracker)
        events = tracker.current_state()['events']
        user_events = []
        for e in events:
            if e['event'] == 'user':
                user_events.append(e)

        custom_data = user_events[-1]['metadata']

        dispatcher.utter_message(response='utter_menu', name=custom_data['sender_id'])

        return []


class ActionShowBalance(Action):

    def name(self) -> Text:
        return "action_show_balance"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return_slots = []
        missing_slots = check_missing(tracker)
        events = tracker.current_state()['events']
        user_events = []
        for e in events:
            if e['event'] == 'user':
                user_events.append(e)

        custom_data = user_events[-1]['metadata']
        return_slots = []
        missing_slots = check_missing(tracker)
        events = tracker.current_state()['events']
        user_events = []
        for e in events:
            if e['event'] == 'user':
                user_events.append(e)

        custom_data = user_events[-1]['metadata']
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "cookie": "csrftoken={}; sessionid={}".format(custom_data['csrf'], custom_data['sessionid'])
        }
        data = f"csrfmiddlewaretoken={custom_data['csrfmw']}"
        url = "http://127.0.0.1:8000/api/user-profile"
        x = requests.post(url, data=data, headers=headers)
        profile = json.loads(x.json())['profile']
        dispatcher.utter_message(text=f"You currently have {profile['current']} in your account")
        return []


class ActionAccountDetail(Action):

    def name(self) -> Text:
        return "action_account_detail"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return_slots = []
        missing_slots = check_missing(tracker)
        events = tracker.current_state()['events']
        user_events = []
        for e in events:
            if e['event'] == 'user':
                user_events.append(e)

        custom_data = user_events[-1]['metadata']
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "cookie": "csrftoken={}; sessionid={}".format(custom_data['csrf'], custom_data['sessionid'])
        }
        data = f"csrfmiddlewaretoken={custom_data['csrfmw']}"
        url = "http://127.0.0.1:8000/api/user-profile"
        x = requests.post(url, data=data, headers=headers)
        profile = json.loads(x.json())['profile']
        dispatcher.utter_message(text=f"Title :{profile['name']}")
        dispatcher.utter_message(text=f"Account Number :{profile['a_no']}")
        dispatcher.utter_message(text=f"Account Type : {profile['a_type']}")
        dispatcher.utter_message(text=f"Current Balance: {profile['current']}")
        return []
