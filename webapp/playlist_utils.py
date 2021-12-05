import random

MOOOODY_PLAYLIST_NAME = 'Embrace your mood and dance with it!'

VAL_SLOTH = [0.0, 0.3]
ENE_SLOTH = [0.0, 0.3]
TEM_SLOTH = 100
SLOTH_VALUES = f"{VAL_SLOTH[0]}/{VAL_SLOTH[1]}/{ENE_SLOTH[0]}/{ENE_SLOTH[1]}/{TEM_SLOTH}"

VAL_QUOKKA = [0.4, 0.7]
ENE_QUOKKA = [0.4, 0.6]
TEM_QUOKKA = 140
QUOKKA_VALUES = f"{VAL_QUOKKA[0]}/{VAL_QUOKKA[1]}/{ENE_QUOKKA[0]}/{ENE_QUOKKA[1]}/{TEM_QUOKKA}"

VAL_CHEETAH = [0.7, 1.0]
ENE_CHEETAH = [0.7, 1.0]
TEM_CHEETAH = 180
CHEETAH_VALUES = f"{VAL_CHEETAH[0]}/{VAL_CHEETAH[1]}/{ENE_CHEETAH[0]}/{ENE_CHEETAH[1]}/{TEM_CHEETAH}"

VAL_CURIOUS = [0.0, 1.0]
ENE_CURIOUS = [0.0, 1.0]
TEM_CURIOUS = "null"
CURIOUS_VALUES = f"{VAL_CURIOUS[0]}/{VAL_CURIOUS[1]}/{ENE_CURIOUS[0]}/{ENE_CURIOUS[1]}/{TEM_CURIOUS}"


class MoooodyPlaylist():
    def __init__(self):
        self.sp = None
        self.top_artists = None
        self.id = None
        self.url = None

    def set_sp(self, sp):
        self.sp = sp

    def preprocess_top_artists(self):
        if not self.sp:
            raise ValueError()

        artists_short = self.sp.current_user_top_artists(limit=100, time_range='short_term')['items']
        artists_medium = self.sp.current_user_top_artists(limit=100, time_range='medium_term')['items']
        artists = artists_short + artists_medium
        artists_uris = [i['uri'] for i in artists]
        artists_uris = list(dict.fromkeys(artists_uris)) # Remove duplicates
        self.top_artists = artists_uris


    def search_for_playlist(self):
        if not self.sp:
            raise ValueError()

        all_playlists = self.sp.user_playlists(self.sp.me()['id'])

        # check if user already has playlist
        for p in all_playlists['items']:
            if p['name'] == MOOOODY_PLAYLIST_NAME:
                self.id = p['id']
                self.url = p['external_urls']['spotify']
                break

    def get_random_seed_tracks(self):
        """
        Gets single random track per artist
        :param sp_auth: spotipy.Spotify
        :param artists_uris: list
        :return: list
        """
        artists_uris = random.sample(self.top_artists, 2)

        track_uris = []
        for artist in artists_uris:
            top_tracks = self.sp.artist_top_tracks(artist)['tracks']
            random_track = random.sample(top_tracks, 1)[0]
            track_uris.append(random_track['uri'])

        return track_uris

    def create_new_playlist(self):
        p = self.sp.user_playlist_create(self.sp.me()['id'],
                                                    MOOOODY_PLAYLIST_NAME,
                                                    public=True)
        self.id = p['id']
        self.url = p['external_urls']['spotify']

    def get_playlist_id(self):
        if self.id is None:
            self.create_new_playlist()

        return self.id

    def generate_playlist(self, val, ene, tem_target):
        seed_tracks = self.get_random_seed_tracks()

        track_ids = []
        recommended_songs = self.sp.recommendations(
            seed_tracks=seed_tracks,
            min_valence=val[0],
            max_valence=val[1],
            min_energy=ene[0],
            max_energy=ene[1],
            target_tempo=tem_target,
        )

        track_ids = [i['id'] for i in recommended_songs['tracks']]
        self.sp.playlist_replace_items(self.get_playlist_id(), track_ids)

    def clear(self):
        self.sp = None
        self.top_artists = None
        self.id = None
        self.url = None
