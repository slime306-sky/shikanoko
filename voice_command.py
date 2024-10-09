import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord import FFmpegPCMAudio
from spotify_data import music

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
folder_path = "./my_music"
bot = commands.Bot(command_prefix='!',intents = discord.Intents.all())
GUILD = discord.Object(GUILD_ID)
shikanoko = music()

@bot.event
async def on_ready():
    print("bot is up and ready!")
    try:
        synced = await bot.tree.sync(guild=GUILD)
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="hello",guild=GUILD)
async def hello(interaction : discord.Interaction):
    await interaction.response.send_message(f"hello {interaction.user.mention}! This is a slash command",ephemeral=False) 

@bot.tree.command(name="join", description="Joins the voice channel",guild=GUILD)
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio("shikanoko.mp3")
        voice.play(source)
        await interaction.response.send_message(f"Joined {channel}")
    else:
        await interaction.response.send_message("You are not in a voice channel!", ephemeral=True)

@bot.tree.command(name="leave",description="leave's the voice channel",guild=GUILD)
async def leave(interaction : discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await interaction.response.send_message('i left tha voice channel')
    else:
        await interaction.response.send_message("im not in any voice channel")

@bot.tree.command(name="play",guild=GUILD)
async def play(interaction: discord.Interaction, song_name: str):
    voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    
    if voice is None:
        if interaction.user.voice:
            voice = await interaction.user.voice.channel.connect()
        else:
            await interaction.response.send_message("You need to be in a voice channel to play a song.")
            return

    source = FFmpegPCMAudio(f"{song_name}.mp3")
    if not voice.is_playing():
        voice.play(source)
        await interaction.response.send_message(f"Now playing: {song_name}.mp3")
    else:
        await interaction.response.send_message("A song is already playing, bro!")

@bot.tree.command(name="stop",guild=GUILD)
async def stop(interaction: discord.Interaction):
    voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice and voice.is_playing():
        voice.stop()
        await interaction.response.send_message("Stopped playing the song.")
    else:
        await interaction.response.send_message("Not playing any song, bro!")


@bot.tree.command(name="pause",guild=GUILD)
async def pause(interaction: discord.Interaction):
    voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice and voice.is_playing():
        voice.pause()
        await interaction.response.send_message("Paused the current song.")
    else:
        await interaction.response.send_message("Not playing any song, bro!")

@bot.tree.command(name="resume",guild=GUILD)
async def resume(interaction: discord.Interaction):
    voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice and voice.is_paused():
        voice.resume()
        await interaction.response.send_message("Resumed the song.")
    else:
        await interaction.response.send_message("No song is paused.")

# @bot.tree.command(name="test", guild=GUILD)
# async def test(interaction: discord.Interaction, name: str):
#     data = shikanoko.get_track(name)
    
#     # Create a list of track names
#     track_names = [i["track"]["name"] for i in data]
    
#     # Join the list into a single string separated by new lines or commas
#     track_list = "\n".join(track_names)  # or use ", ".join(track_names) for comma separation
    
#     # Send the formatted list of tracks to Discord
#     await interaction.response.send_message(f"Track names:\n{track_list}")
# import discord
# from discord import app_commands
# from discord.ext import commands

# bot = commands.Bot(command_prefix="!")

# import discord
# from discord import app_commands

# # Sample track data
# tracks = [
#     {'name': '7 Years', 'track_link': 'https://open.spotify.com/track/5kqIPrATaCc2LqxVWzQGbk'},
#     {'name': '7 Years (Remix)', 'track_link': 'https://open.spotify.com/track/1kFlDnWmBTvCBxxeGDpIdp'},
#     # ... (include all other tracks here)
# ]

@bot.tree.command(name="test", guild=GUILD)
async def test(interaction: discord.Interaction,name : str):
    # Create a list of track options for the select menu
    tracks = shikanoko.get_track(name)
    temp = []
    for i in tracks:
        data = i["track"]
        temp.append(data)
    track_options = [
        discord.SelectOption(label=track['name'], value=track['track_link']) for track in temp
    ]

    # Create a select menu
    select = discord.ui.Select(placeholder="Choose a track...", options=track_options)

    # Define the callback for when a user selects a track
    async def select_callback(interaction: discord.Interaction):
        selected_url = select.values[0]  # Get the selected track link
        await interaction.response.send_message(f"You selected: {selected_url}")
        print(selected_url)
        print(select)
        shikanoko.download_song_in_folder(selected_url,folder_path)
        # Call the function with the selected URL here
        # For example: await your_function(selected_url)

    select.callback = select_callback

    # Create a view to hold the select menu
    view = discord.ui.View()
    view.add_item(select)

    # Send the message with the select menu
    await interaction.response.send_message("Select a track:", view=view)



# Note: Make sure to have the necessary imports and bot setup code.
@bot.tree.command(name="list", guild=GUILD)

async def list_mp3(interaction: discord.Interaction):
    # global selected_song_path  # Use global to modify the variable in the outer scope
    folder_path = './my_music'  # Change this to your folder path

    # Get a list of all files in the specified directory
    files = os.listdir(folder_path)

    # Filter out MP3 files
    mp3_files = [file for file in files if file.endswith('.mp3')]

    if mp3_files:
        options = [discord.SelectOption(label=file, value=file) for file in mp3_files]
        select = discord.ui.Select(placeholder='Choose an MP3 file...', options=options)

        view = discord.ui.View()
        view.add_item(select)

        async def select_callback(interaction: discord.Interaction):
            selected_file = select.values[0]
            selected_song_path = os.path.join(folder_path, selected_file)
            voice = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    
            if voice is None:
                if interaction.user.voice:
                    voice = await interaction.user.voice.channel.connect()
                else:
                    await interaction.response.send_message("You need to be in a voice channel to play a song.")
                    return

            source = FFmpegPCMAudio(selected_song_path)
            if not voice.is_playing():
                voice.play(source)
                await interaction.response.send_message(f"Now playing: {selected_song_path}")
            else:
                await interaction.response.send_message("A song is already playing, bro!")

            await interaction.response.send_message(f'You selected: {selected_file}', ephemeral=True)

        select.callback = select_callback
        await interaction.response.send_message("Please select an MP3 file:", view=view)
    else:
        await interaction.response.send_message("No MP3 files found in the directory.")




bot.run(token=TOKEN)