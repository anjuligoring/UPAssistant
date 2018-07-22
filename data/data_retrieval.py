import urllib.request
import json
import requests

sample_data = {
  "id": "SHMC6134",
  "empty": "false",
  "commodity": "Coal",
  "carType": "Uncovered Hopper",
  "serviceIssue": {
    "referenceNumber": "00516",
    "status": "Open"
  },
  "eta": "2018-07-23T05:04:00.000-05:00",
  "completedEvents": [
    {
      "name": "Released for Movement",
      "dateTime": "2018-06-04T13:47:00.000-05:00",
      "location": {
        "city": "Stexlead",
        "state": "TX"
      }
    },
    {
      "name": "Pulled from Industry",
      "dateTime": "2018-06-12T09:07:00.000-05:00",
      "location": {
        "city": "Stexlead",
        "state": "TX"
      }
    },
    {
      "name": "Arrived",
      "dateTime": "2018-06-12T10:09:00.000-05:00",
      "location": {
        "city": "Stexlead",
        "state": "TX"
      }
    },
    {
      "name": "Departed",
      "dateTime": "2018-06-22T11:02:00.000-05:00",
      "location": {
        "city": "Stexlead",
        "state": "TX"
      }
    },
    {
      "name": "Arrived",
      "dateTime": "2018-06-22T14:20:00.000-05:00",
      "location": {
        "city": "Texarkana",
        "state": "AR"
      }
    },
    {
      "name": "General Hold",
      "dateTime": "2018-06-25T22:12:00.000-05:00",
      "location": {
        "city": "Texarkana",
        "state": "AR"
      }
    },
    {
      "name": "Released from Hold",
      "dateTime": "2018-07-05T15:57:00.000-05:00",
      "location": {
        "city": "Texarkana",
        "state": "AR"
      }
    }
  ],
  "scheduledEvents": [
    {
      "name": "Scheduled Departure",
      "dateTime": "2018-07-21T11:15:00.000-05:00",
      "location": {
        "city": "Stexlead",
        "state": "TX"
      }
    },
    {
      "name": "Scheduled Arrival",
      "dateTime": "2018-07-21T20:00:00.000-05:00",
      "location": {
        "city": "Texarkana",
        "state": "AR"
      }
    },
    {
      "name": "Scheduled Departure",
      "dateTime": "2018-07-22T23:11:00.000-05:00",
      "location": {
        "city": "Texarkana",
        "state": "AR"
      }
    },
    {
      "name": "Scheduled Arrival",
      "dateTime": "2018-07-23T05:04:00.000-05:00",
      "location": {
        "city": "Nlitrock",
        "state": "AR"
      }
    },
    {
      "name": "Scheduled Departure",
      "dateTime": "2018-07-24T13:00:00.000-05:00",
      "location": {
        "city": "Nlitrock",
        "state": "AR"
      }
    }
  ]
}

def get_quote_price(origin, destination):
    origin = origin.replace(" ", "+") + "+USA"
    destination = destination.replace(" ", "+") + "+USA"
    origin = origin.replace(",", "")
    destination = destination.replace(",", "")

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + origin + "&destinations=" + destination
    contents = urllib.request.urlopen(url).read()
    response = requests.get(url)
    obj = json.loads(response.content.decode('utf-8'))
    distance = obj['rows'][0]['elements'][0]['distance']['text'][:-2]
    distance = distance.replace(',', '')
    cost = float(distance) * 3.15
    cost = str('${:,.2f}'.format(cost))
    return cost

def get_data():
    json_data = json.dumps(sample_data)
    data = json.loads(json_data)
    return data

def get_car_status():
    data = get_data()

    num_completed = 0.0
    completed_events = data['completedEvents']
    for event in completed_events:
        if event['name'] == 'Arrived':
            num_completed = num_completed + 1
    
    num_remaining = 0.0
    remaining_events = data['scheduledEvents']
    for event in remaining_events:
        if event['name'] == 'Scheduled Departure':
            num_remaining = num_remaining + 1
    
    completion_percent = float(num_completed / (num_completed + num_remaining))
    completion_percent = "{0:.2%}".format(completion_percent)

    return completion_percent

def get_car_eta():
    data = get_data()
    eta = data['eta']

    year = eta[:4]
    month = eta[5:7]
    day = eta[8:10]
    hour = (int)(eta[11:13]) % 12
    min = eta[14:16]
    if (int)(eta[11:13]) > 12:
        ampm = "pm"
    else:
        ampm = "am"

    switcher = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
    }
    month = switcher.get(month, 'Invalid Month')
    date = month + " " + day + ", " + year
    time = (str)(hour) + ":" + min + " " + ampm
    return date + " @ " + time

def get_car_service_issues():
    data = get_data()
    if('serviceIssue' not in data):
        return 'There are no service issues!'
    else:
        return 'WARNING: You have a service issue. Your reference # is ' + data['serviceIssue']['referenceNumber'] + '.'