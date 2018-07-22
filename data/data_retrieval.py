import urllib.request
import json
import requests

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