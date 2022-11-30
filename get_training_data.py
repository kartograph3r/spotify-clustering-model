import spotipy
from spotipy.oauth2 import SpotifyOAuth
from creds import client_id, client_secret
from pandas import DataFrame
from time import time

redirect_uri = 'https://example.com/callback'

TRACK_LIMIT = 100

FEATURE_KEYS = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

TRAIN_PLAYLISTS =   [
                    {'playlist_name': 'pl_1', 'playlist_id':'5odVcGhacZRipA6icQBXGJ'},
                    {'playlist_name': 'pl_2', 'playlist_id':'16o2PmthNAkEgvxpXkhQDL'},
                    {'playlist_name': 'pl_3', 'playlist_id':'4UxEztKJnKkjvl6yvmyoYZ'},
                    {'playlist_name': 'pl_4', 'playlist_id':'2GkbJdZcGMEjFSh94vrT2z'},
                    {'playlist_name': 'pl_5', 'playlist_id':'2uvkMAB6ipu8NhcWLLAMEr'},
                    {'playlist_name': 'pl_6', 'playlist_id':'2DBM92lgqEQF43CbihWGtw'}
                    ]

TRACKS = [[] for i in range(len(TRAIN_PLAYLISTS))]


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-read-private"))

for idx, train_playlist in enumerate(TRAIN_PLAYLISTS):
    print(f'Fetching tracks from playlist {train_playlist["playlist_name"]}')
    offset=0
    while True:
        paged_tracks = sp.playlist_items(train_playlist['playlist_id'], limit=TRACK_LIMIT, offset=offset)
        TRACKS[idx].extend([{'name':el['track']['name'], 'id':el['track']['id']} for el in paged_tracks['items']])
        print(f'Fetched {len(TRACKS[idx])} tracks')
        offset+=TRACK_LIMIT
        if paged_tracks['next'] is None:
            break

TRAIN_DATA = []

def get_windowed_track_ids(_tracks, limit):
    for i in range(0, len(_tracks), limit): 
        track_window = _tracks[i:i + limit]
        yield track_window, [t['id'] for t in track_window]

for idx, train_playlist in enumerate(TRAIN_PLAYLISTS):
    for track_window, track_window_ids in get_windowed_track_ids(TRACKS[idx], TRACK_LIMIT):
        track_features = sp.audio_features(tracks=track_window_ids)
        for index, _track in enumerate(track_window):
            _track.update({k:v for k,v in track_features[index].items() if k in FEATURE_KEYS})
            _track.update(train_playlist)
            TRAIN_DATA.append(_track)
        print(f'Fetched {len(TRAIN_DATA)} features')

df=DataFrame.from_dict(TRAIN_DATA)
filename = f'playlist_features_{int(time())}.csv'
df.to_csv(filename, index=False)
print(f'Saved features to {filename}')