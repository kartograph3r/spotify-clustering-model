from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from pandas import read_csv 

FEATURE_KEYS = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
K_MAX = 11

df=read_csv('liked_tracks_1666976584.csv')

cost = list()
for i in range(1, K_MAX):
    KM = KMeans(n_clusters = i, max_iter = 500)
    KM.fit(df[FEATURE_KEYS])
    cost.append(KM.inertia_)

plt.plot(range(1, K_MAX), cost, color ='g', linewidth ='2')
plt.xlabel("Value of K")
plt.ylabel("Sqaured Error (Cost)")
plt.show()