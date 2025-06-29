# Shikanoko

🎵 A Discord bot that plays songs using Spotify data and local audio files.

## Features

- Accepts voice commands for music control
- Plays pre-downloaded music stored locally
- Uses Spotify API to manage or retrieve song data (based on implementation)
- Integrates with Discord's voice channels

## Project Structure
```
shikanoko-main/
├── README.md
├── shikanoko.mp3
├── song.mp3
├── spotify_data.py         # Handles Spotify-related functionality
├── voice_command.py        # Processes voice input for commands
└── my_music/               # Folder containing local MP3 files
    ├── 7 Years.mp3
    ├── Snowman.mp3
    └── X.mp3
```
## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/shikanoko.git
cd shikanoko
```
### 2. Set Up Dependencies
Install required libraries (like discord.py, spotipy, speechrecognition, etc.):

```bash
pip install -r requirements.txt
If no requirements.txt is available, let us know to help you generate one.
```
### 3. Run the Bot
```bash
python voice_command.py
```
## Notes
* Ensure you have set up your Discord Bot token and Spotify API credentials.

* Local music files should be stored inside the my_music folder.

* Voice recognition may require additional system dependencies like PyAudio.

## License
MIT License
