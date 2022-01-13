# Moooody Spotify Playlist Generator

The program will source the top 10 songs from my top 100 artists in the last 6 months. Out of those, 2 songs are selected as seeds to generate a new playlist.

The playlist is tailored to your mood, and for this moods are associated to animal behaviour. The program asks ‘How do you feel today? Sloth, Quokka, Cheetah or curious?’. Each choice is translated into specific values of valence, beats per minute and energy levels which are matched to the songs selected for the playlist. Sloth will select slower, relaxing and ambient songs; Quokka will select carefree, happy and upbeat ones; Cheetah will generate a very high tempo playlist. Finally, the curious option will allow you to discover mixed mood songs. 

Dance your mood out!

### Dependencies

```
python          3.8
spotipy         2.18.0
flask           2.0.1
flask-session   0.4.0
```

### How to use

This code relies on

Assuming you set the `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET` and `SPOTIPY_REDIRECT_URI` environment variables (according to [Spotipy's documentation](https://spotipy.readthedocs.io/en/2.18.0/#features)), your playlist can be generated with:

```
python generate_playlist.py
```
