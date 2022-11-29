from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import Counter
from pandas import read_csv
import spotipy
from spotipy import SpotifyOAuth

client_id = "c91fd423291d43589c9f088704523cb8"
client_secret = "e238259638cf4d54acb1e7d165fd7d50"
redirect_uri = 'http://localhost:9001/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-modify-public"))

user_id = sp.current_user()['id']

FEATURE_KEYS = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
TRAIN_DATA=read_csv('playlist_features_1666975963.csv')
PREDICT_DATA=read_csv('liked_tracks_1666975933.csv')

X_train, X_test, y_train, y_test = train_test_split(TRAIN_DATA[FEATURE_KEYS], TRAIN_DATA['playlist_name'],test_size=0.3)

model = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=7)
model.fit(X_train, y_train)

y_predicted = model.predict(X_test)
print(f'\nModel accuracy is {accuracy_score(y_test, y_predicted)}', end='\n\n')

_predicted_playlist = model.predict(PREDICT_DATA[FEATURE_KEYS])

PREDICT_DATA['assigned_playlist'] = _predicted_playlist


print(f'Prediction completed. Target distribution : {dict(Counter(_predicted_playlist))}', end='\n\n')

print(PREDICT_DATA[['name', 'assigned_playlist']].sample(50))