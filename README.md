# Spotify song clustering models

Please make sure to run `get_liked_tracks.py` first to fetch your liked tracks, please note to input your `client_id`, and `client_secret`.

## Unsupervised algorithm

Uses k-means clustering on the given set of liked songs to create clusters - and then create them using the spotify API.
**Steps:**
1. Run `identify-k.py` to identify the number of clusters.
2. Run `unsupervised.py` to run the model and find the clusters.

## Supervised algorithm

Uses a set of selected playlists as training data to identify which song corresponds to which playlist.
For the purpose of demonstration and API limitations, I've only ran this on 6 of my own small (50 - ish songs) playlists.

Just run `supervised.py` to train and run the supervised algorithm.
