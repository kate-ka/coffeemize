import os
import foursquare
import requests


def get_coffee_places():
    client_id = os.environ.get("CLIENT_ID", None)
    client_secret = os.environ.get("CLIENT_SECRET", None)
    client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, version='20120609')
    return client.venues.explore(params={'query': 'coffee', 'near': 'Lviv', 'venuePhotos': True})
# print(get_coffee_places()['groups'][0]['items'][1]['venue'])
# print(get_coffee_places()['groups'][0]['items'][1]['venue']['location'])
# pprint(get_coffee_places().keys())dict_keys(['geocode', 'suggestedBounds', 'groups', 'totalResults', 'headerFullLocation', 'query', 'headerLocation', 'headerLocationGranularity', 'suggestedFilters'])
#
print((get_coffee_places()['groups'][0]['items']))

for item in get_coffee_places()['groups'][0]['items']:
    client_id = os.environ.get("CLIENT_ID", None)
    client_secret = os.environ.get("CLIENT_SECRET", None)
    print('*'*60)
    client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, version='20120609')
    print(client.venues(item['venue']['id'])['venue'].get("page", {}).get("user", {}).get('photo'), "VENUUE BY ID")

    try:
        print(item['venue']['id'])
        print(item['venue']['name'])
        print(item['tips'][0]['text'])


        print(item['tips'][0]['canonicalUrl'])
        '4ffb08cde4b0e8d00f2fd4b5'

        print(item['venue']['photos']['groups'][0]['items'][0]['prefix'] + 'width400' + item['venue']['photos']['groups'][0]['items'][0]['suffix'])
        print(item['venue']['categories'][0]['icon']['prefix'] + '64' + item['venue']['categories'][0]['icon']['suffix'], "ICON")

        # {'pluralName': 'Snack Places', 'id': '4bf58dd8d48988d1c7941735', 'name': 'Snack Place', 'primary': True,
        #  'icon': {'suffix': '.png', 'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/snacks_'},
        #  'shortName': 'Snacks'}

        print(item['venue']['rating'])
        print(item['venue']['url'])
        print(item['venue']['contact']['formattedPhone'])
        print(item['venue']['location']['address'])
        print(item['venue']['categories'][0]['name'])
        print(item['venue']['hours']['status'])
        # print(item['venue']['hours']['isOpen'])
        print(item['venue']['price']['message'])
        print(item['venue']['location']['city'])

    except KeyError:
        pass






