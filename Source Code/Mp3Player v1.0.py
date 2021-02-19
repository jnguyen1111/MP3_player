import tkinter as tk
from tkinter import filedialog
import os
from audioplayer import AudioPlayer

index = 0
songs =[]

# loads song
def load_song():
    global player
    pick_song = tk.filedialog.askopenfile()
    name = (str(pick_song.name))
    player = AudioPlayer(name)
    extract_name = name.split("/")
    song_track = extract_name[-1]
    song_title = tk.Label(text='                                                                                                                                                                            ')
    song_title.place(x=250, y=20, anchor="center")
    play()
    song_title = tk.Label(text=song_track)
    song_title.place(x=250, y=20, anchor="center")
    play()

# loads a list of songs into a playlist *** Note: cannot play the next song in playlist automatically (WIP) ***
def load_playlist():
    global player , songs , pick_play_list
    pick_play_list=tk.filedialog.askdirectory()
    song_list = os.listdir(pick_play_list)
    for choose in song_list:
        songs.append(choose)
    # need it to make a system where it keeps playing
    pick_song = songs[0]
    player = AudioPlayer(pick_play_list + "/" + pick_song)
    # note the song names do not clear and update
    song_title = tk.Label(text=pick_song)
    song_title.place(x=250, y=20, anchor="center")
    play()

def play():
    global player
    player.volume = 50
    player.play(loop=False)

def resume_song():
    global player
    player.resume()

def pause_song():
    global player
    player.pause()

def loop_song():
    global player
    player.play(loop=True)

#adjust volume with slider
def volume_adjust(delta):
    global player
    delta = int(delta)
    player.volume = delta*.69

def __init__():
    # creates the application window for the mp3 player
    applic_window.title("Vibe Player")
    applic_window.geometry("500x200")

    # create buttons and assign specific position
    load_song_button = tk.Button(applic_window, text="LOAD SONG", height=1, width=15, command=load_song)
    pause_button = tk.Button(applic_window, text="PAUSE", height=1, width=15, command=pause_song)
    resume_button = tk.Button(applic_window, text="RESUME", height=1, width=15, command=resume_song)
    loop_button = tk.Button(applic_window, text="LOOP SONG", height=1, width=15, command=loop_song)
    quit_button = tk.Button(applic_window,text="QUIT",height=1,width=15,command=applic_window.destroy)

    pause_button.place(x=60, y=50, anchor="center")
    resume_button.place(x=180, y=50, anchor="center")
    load_song_button.place(x=300, y=50, anchor="center")
    loop_button.place(x=420, y=50, anchor="center")
    quit_button.place(x=245 ,y=80, anchor="center")

    volume_scale = tk.Scale(applic_window, from_=0, to=100, orient=tk.HORIZONTAL, length=475, tickinterval=10,command=volume_adjust, resolution=1)
    volume_text = tk.Label(text="VOLUME")
    volume_scale.place(x=250, y=165, anchor="center")
    volume_scale.set(50)
    volume_text.place(x=15, y=130, anchor="w")

# create application and run a loop
applic_window = tk.Tk()
applic_window.resizable(width=False, height=False)
__init__()
applic_window.mainloop()

