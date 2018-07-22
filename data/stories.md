## default
* default{"request": "temp"}
    - utter_default
    - action_get_request

## greet
* greet
    - utter_greet

## bye
* bye
    - utter_bye

## lance_fritz_request
* lance_fritz_request
    - utter_lance_fritz

## price_quote_request
* price_quote_request
    - utter_ask_origin
* location_inform{"location": "Omaha, NE"}
    - action_store_origin
    - utter_ask_destination
* location_inform{"location": "Austin, TX"}
    - action_store_destination
    - action_get_price_quote
    - action_clear_slots