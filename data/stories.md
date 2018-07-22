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

<!--- CAR -->

<!-- status -->
## car_status_request 1
* car_status_request
    - utter_ask_car_id
* car_id_inform{"car_id": "SHMC6134"}
    - action_get_car_status
    - slot{"is_valid": true}

## car_status_request 2
* car_status_request
    - utter_ask_car_id
* car_id_inform{"car_id": "null"}
    - action_get_car_status
    - slot{"is_valid": false}
    - utter_invalid

## car_status_inform 1
* car_status_inform{"car_id": "SHMC6134"}
    - action_get_car_status
    - slot{"is_valid": true}

## car_status_inform 1
* car_status_inform{"car_id": "null"}
    - action_get_car_status
    - slot{"is_valid": false}
    - utter_invalid

<!-- eta -->
## car_eta_request 1
* car_eta_request
    - utter_ask_car_id
* car_id_inform{"car_id": "SHMC6134"}
    - action_get_car_eta
    - slot{"is_valid": true}

## car_eta_request 2
* car_eta_request
    - utter_ask_car_id
* car_id_inform{"car_id": "null"}
    - action_get_car_eta
    - slot{"is_valid": false}
    - utter_invalid

## car_eta_inform 1
* car_eta_inform{"car_id": "SHMC6134"}
    - action_get_car_eta
    - slot{"is_valid": true}

## car_eta_inform 2
* car_eta_inform{"car_id": "null"}
    - action_get_car_eta
    - slot{"is_valid": false}
    - utter_invalid