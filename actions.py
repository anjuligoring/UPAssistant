from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

class ActionGetRequest(Action):

    def name(self):
        return 'action_get_request'
    
    def run(self, dispatcher, tracker, domain):
        # Append failed user request to end of 'requests.txt'
        request = str(tracker.latest_message.text)
        with open('requests.txt', 'a') as requests:
            requests.write(request + '\n')
        return []