import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

goon = True
while goon == True:
  choice = input("Do you want to create a Spotify Playlist? (Y/N): ").lower()

  if choice == 'y':
    
    date = input("What year do you want your ears to travel to? (YYYY-MM-DD): ")
    URL = f"https://www.billboard.com/charts/hot-100/{date}/"
    year = date.split("-")[0]
    
    response = requests.get(URL)
    website_html = response.text
    
    # now use beautiful soup on website html
    soup = BeautifulSoup(website_html, "html.parser")
    songs = soup.select("li ul li h3")
    # artists = soup.select("li ul li span") this is getting other things too, still NOT good at looking at html and figuring out where things go
    artists = soup.findAll(name="span", class_="a-no-trucate")
    
    song_names = [song.getText().strip() for song in songs]
    artist_names = [artist.getText().strip() for artist in artists]
    
    song_artist_list = dict(zip(song_names, artist_names))
    # print(song_artist_list)

    # check if songs added to list
    if len(song_artist_list):
      ID = MY ID
      SECRET = MY SECRET
      
      sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
          scope="playlist-modify-private",
          redirect_uri="http://example.com",
          client_id=ID,
          client_secret=SECRET,
          show_dialog=True,
          cache_path="token.txt",
        )
      )
      
      user_id = sp.current_user()["id"]
  
      playlist_name = f"{date} Billboard Top Tracks"
      my_playlist = sp.user_playlist_create(user=f"{user_id}", name=playlist_name, public=False,
                                          description=f"Top Tracks from {date}")
      # was going to try to make sure the playlist didnt already exist but id have to use spotify's api and not just spotipy ?
      # if playlist_name not in sp.user_playlists(XXXXXX):
      #   my_playlist = sp.user_playlist_create(user=f"{user_id}", name=playlist_name, public=False,
      #                                     description=f"Top Tracks from {date}")
      playlist_id = my_playlist['id']
      
      spotify_song_uris = []
      ##TAKEN OUT OF BELOW FOR LOOP ['artists'][0] -> remember to add back in
      for key, value in song_artist_list.items():
        # spotify_result = sp.search(q=f"artist:{key} track:{value} year:{year}", type="track")
        spotify_result = sp.search(value)
        try:
          song_uri = spotify_result['tracks']['items'][0]['uri']
          spotify_song_uris.append(song_uri)
        except IndexError:
          print(f"{value} doesn't exist in Spotify. Skipped.")
      # print(len(spotify_song_uris))
      
  
      sp.user_playlist_add_tracks(user_id, playlist_id, spotify_song_uris)

  elif choice == 'n':
    goon = False
