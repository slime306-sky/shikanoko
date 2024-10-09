from dotenv import load_dotenv
import os
import subprocess
import requests 
import base64
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

class music:

    accessToken : str = None
    client_id : str = CLIENT_ID
    client_secret : str = CLIENT_SECRET

    def __init__(self):
        if not self.accessToken :
            auth_str = f"{self.client_id}:{self.client_secret}"
            b64_auth_str = base64.b64encode(auth_str.encode()).decode()

            url = "https://accounts.spotify.com/api/token"
            headers = {
                "Authorization": f"Basic {b64_auth_str}",
            }
            data = {
                "grant_type": "client_credentials",
            }

            response = requests.post(url, headers=headers, data=data)
            response_data = response.json()
            self.accessToken = response_data["access_token"]

    def get_track(self,track_name: str):
        # print(track_name, type(track_name))  # To check the value and type of track_name
        track_name = track_name.replace(" ","+")
        url = "https://api.spotify.com/v1/search"
        params = {
            "q": track_name,
            "type": "track",

        }
        headers = {
            "Authorization": f"Bearer {self.accessToken}"
        }
        
        response = requests.get(url=url,headers=headers,params=params)

        response = response.json()
        # response = response["tracks"]["items"][0]
        track = []
        

        for i in range(20):
            temp = response["tracks"]["items"][i]
            track_filter = {
                "track" : {
                    "name" : temp["name"],
                    "track_link" : temp["external_urls"]["spotify"]
                    # "images" : temp["album"]["images"]
                }
            }
            track.append(track_filter)

        return track
    


    def download_song_in_folder(self,song_url, folder_path):
        song_url = str(song_url)
        print(f"Song URL: {song_url}")  # Debugging line
        print(f"Folder Path: {folder_path}")  # Debugging line

        # Ensure the folder exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Command to download song into specified folder
        subprocess.run([
            "spotdl", 
            "download", 
            song_url, 
            "--output", os.path.join(folder_path, "{title}")
        ])
