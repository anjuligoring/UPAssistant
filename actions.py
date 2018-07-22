from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import data.data_retrieval as data_retrieval

class ActionGetRequest(Action):

    def name(self):
        return 'action_get_request'
    
    def run(self, dispatcher, tracker, domain):
        # Append failed user request to end of 'requests.txt'
        request = str(tracker.latest_message.text)
        with open('requests.txt', 'a') as requests:
            requests.write(request + '\n')
        return []

class ActionStoreOrigin(Action):

    def name(self):
        return 'action_store_origin'
    
    def run(self, dispatcher, tracker, domain):
        origin = str(tracker.latest_message.text)
        return [SlotSet('origin', origin)]

class ActionStoreDestination(Action):

    def name(self):
        return 'action_store_destination'
    
    def run(self, dispatcher, tracker, domain):
        destination = str(tracker.latest_message.text)
        return [SlotSet('destination', destination)]

class ActionGetPriceQuote(Action):

    def name(self):
        return 'action_get_price_quote'
    
    def run(self, dispatcher, tracker, domain):
        # Calculate the cost of price of transporting between 2 places
        origin = str(tracker.get_slot('origin'))
        destination = str(tracker.get_slot('destination'))

        cost = data_retrieval.get_quote_price(origin, destination)
        dispatcher.utter_message('Quote: ' + cost)
        return []

class ActionClearSlots(Action):

    def name(self):
        return 'action_clear_slots'
    
    def run(self, dispatcher, tracker, domain):
        return [SlotSet('request', ''), SlotSet('car_id', ''), SlotSet('location', ''), SlotSet('origin', ''), SlotSet('destination', '')]