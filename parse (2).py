import pandas as pd

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10000)

songs = pd.read_csv('fin_nogenre.csv', header=None)
songs.columns = ["Name", "Explicit", "ReleaseDate", "Duration", "id", "sad", "chill", "happy", "hype"]
songs2 = songs.sample(frac=0.001).reset_index()
songs2 = songs2.loc[songs2['Explicit'] == False]
songs2.to_csv('songs2.csv', index=False)
new_songs = pd.read_csv('songs2.csv')
new_songs = new_songs.loc[new_songs['happy'] + new_songs['sad'] > 0.9]
happy_songs = new_songs[(new_songs['happy'] >= 0.5)]
sad_songs = new_songs[(new_songs['sad'] >= 0.5)]
happy = happy_songs.sample(frac=0.3).sort_values('happy').reset_index()
sad = sad_songs.sample(frac=0.3).sort_values('sad', ascending=False).reset_index()
# new_songs = new_songs.sort_values(["happy", "sad"], ascending=[1, 0])[["Name", "id", "sad", "happy"]]
playlist_songs = []
# print(happy_songs)
# print(sad_songs)

for index, row in sad.iterrows():
    playlist_songs.append(row['id'])
    print(index, row['Name'], row['id'], row['sad'], row['happy'])
    if len(playlist_songs) == 50:
        break
for index, row in happy.iterrows():
    playlist_songs.append(row['id'])
    print(index, row['Name'], row['id'], row['sad'], row['happy'])
    if len(playlist_songs) == 100:
        break
# for i in range(len(sad_songs.index)):
#     playlist_songs.append(sad_songs['id'].str.get(i))
#     i += random.randint(1, 2)
#     if len(playlist_songs) == 50:
#         break
# for i in range(len(happy_songs.index)):
#     playlist_songs.append(sad_songs['id'].str.get(i))
#     i += random.randint(1, 2)
#     if len(playlist_songs) == 50:
#         break
