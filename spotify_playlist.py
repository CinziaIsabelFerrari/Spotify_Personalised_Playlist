import sys
import requests
import spotipy
import spotipy.util as util
import json
import random

username = '1167152572'
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)


#get random songs from seed
endpoint_url = "https://api.spotify.com/v1/recommendations?"

#my filters:
limit = 4
uris1 = []

market = "GB" #can choose country code asking via input
#country = "GB"
#locale = "es_ES" #language of the tracks
#seed_genres = "jazz" #can choose genre via input // look for a list of genres
target_danceability = 0.9 # goes from 0 to 1
#min_popularity = which are the values?
target_popularity = 50 # goes from 0 to 100
# can you add mood on top of genres, and the language instead of country?

genre1 = input('Choose a genre between indie, jazz, classical, dance, groove: ')

query1 = '{}limit={}&seed_genres={}&target_danceability={}&target_popularity={}&market={}'.format(
    endpoint_url,
    limit,
    genre1,
    target_danceability,
    target_popularity,
    market)

response1 = requests.get(query1,
                        headers = {'Content-Type':'application/json',
                                   'Authorization':'Bearer {}'.format(token)})

json_response = response1.json()

genre2 = input('Choose a genre between rock, disco, electronic, funk, rockabilly: ')

query2 = '{}limit={}&seed_genres={}&target_danceability={}&target_popularity={}&market={}'.format(
    endpoint_url,
    limit,
    genre2,
    target_danceability,
    target_popularity,
    market)

response2 = requests.get(query2,
                        headers = {'Content-Type':'application/json',
                                   'Authorization':'Bearer {}'.format(token)})

json_response2 = response2.json()

genre3 = input('Choose a genre between blues, funk, groove, hip-hop, rock-n-roll ')

query3 = '{}limit={}&seed_genres={}&target_danceability={}&target_popularity={}&market={}'.format(
    endpoint_url,
    limit,
    genre3,
    target_danceability,
    target_popularity,
    market,)

response3 = requests.get(query3,
                        headers = {'Content-Type':'application/json',
                                   'Authorization':'Bearer {}'.format(token)})

json_response3 = response3.json()
print(json_response3)

for i,j in enumerate (json_response['tracks']):
    uris1.append(j['uri'])
    print('{})\"{}\" by \"{}\"'.format(i+1, j['name'],j['artists'][0]['name']))

for i,j in enumerate (json_response2['tracks']):
    uris1.append(j['uri'])
    print('{})\"{}\" by \"{}\"'.format(i+5, j['name'],j['artists'][0]['name']))

for i,j in enumerate (json_response3['tracks']):
    uris1.append(j['uri'])
    print('{})\"{}\" by \"{}\"'.format(i+9, j['name'],j['artists'][0]['name']))

# Randomly shuffle the order of elements in uris1
random.shuffle(uris1)

#create a playlist

endpoint_url = "https://api.spotify.com/v1/users/{}/playlists".format(username)

request_body = json.dumps({
          "name": "My new cose-a-caso playlist",
          "description": "Finally!",
          "public": True
        })
response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json",
                        'Authorization':'Bearer {}'.format(token)})

url = response.json()['external_urls']['spotify']
print(response.status_code)

#add songs to the playlist

playlist_id = response.json()['id']

endpoint_url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

request_body = json.dumps({"uris" : uris1})

response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json",
                        'Authorization':'Bearer {}'.format(token)})

print(response.status_code)


print('Your playlist is ready at {}'.format(url))



