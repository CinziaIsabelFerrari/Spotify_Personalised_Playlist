import sys
import requests
import spotipy
import spotipy.util as util
import json

username = '1167152572'
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)


#get random songs from seed
endpoint_url = "https://api.spotify.com/v1/recommendations?"

#my filters:
limit = 10
uris = []
market = "GB" #can choose country code asking via input
seed_genres = "indie" #can choose genre via input // look for a list of genres
target_danceability = 0.9 # goes from 0 to 1
#min_popularity = which are the values?
target_popularity = 50 # goes from 0 to 100
# can you add mood on top of genres, and the language instead of country?

query = '{}limit={}&market={}&seed_genres={}&target_danceability={}&target_popularity={}'.format(endpoint_url, limit, market, seed_genres, target_danceability, target_popularity)

response = requests.get(query,
                        headers = {'Content-Type':'application/json',
                                   'Authorization':'Bearer {}'.format(token)})

json_response = response.json()
print(json_response)

for i,j in enumerate (json_response['tracks']):
    uris.append(j['uri'])
    print('{})\"{}\" by \"{}\"'.format(i+1, j['name'],j['artists'][0]['name']))



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

request_body = json.dumps({
          "uris" : uris
        })
response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json",
                        'Authorization':'Bearer {}'.format(token)})

print(response.status_code)


print('Your playlist is ready at {}'.format(url))



