from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred



inputDate = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD : ")
URL = f"https://www.billboard.com/charts/hot-100/{inputDate}/"

year = inputDate.split("-")[0]
response = requests.get(URL)

billboardWebPage = response.text

soup = BeautifulSoup(billboardWebPage, 'html.parser')
songTitleHeaders = soup.find_all(name = "h3", class_ = "a-no-trucate")
songNames = [title.getText().strip() for title in songTitleHeaders]
print(songNames)
print(len(songNames))

scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=cred.clientID, 
    client_secret=cred.clientSecret, 
    redirect_uri= cred.redirectURL, 
    scope=scope,
    cache_path= "token.txt", 
    show_dialog=True))

userID = sp.current_user()["id"]

songURI = []

for song in songNames:
    result = sp.search(q=f"track : {song}, year: {year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songURI.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist= sp.user_playlist_create(user = userID, name=f"{inputDate} Billboard 100 untuk Dwi", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items= songURI)