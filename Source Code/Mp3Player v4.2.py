import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import random , os , threading , time , sys ,gc , pyglet

class Mp3_player:
    def song_timeformat(self):
        # section below defines song time conversion
        length_song_hour = self.length // 3600
        self.length %= 3600
        length_song_minute = self.length // 60
        self.length %= 60
        length_song_second = self.length
        current_hour = self.current_time // 3600
        self.current_time %= 3600
        current_minute = self.current_time // 60
        self.current_time %= 60
        current_sec = self.current_time

        # hour long songs or less format below
        if length_song_hour == 0:
            if current_sec < 10:
                current_sec = str(current_sec).zfill(2)
                int(current_sec)
            if length_song_second < 10:
                length_song_second = str(length_song_second).zfill(2)
                int(length_song_second)
            self.time_playback.set(self.conv_time)
            self.song_time['text'] = "track  length    {}:{}/{}:{}".format(current_minute, current_sec,length_song_minute, length_song_second)

        elif length_song_hour > 0:
            if current_sec < 10:
                current_sec = str(current_sec).zfill(2)
                int(current_sec)
            if current_minute < 10:
                current_minute = str(current_minute).zfill(2)
                int(current_minute)
            if length_song_second < 10:
                length_song_second = str(length_song_second).zfill(2)
                int(length_song_second)
            if length_song_minute < 10:
                length_song_minute = str(length_song_second).zfill(2)
                int(length_song_minute)
            self.time_playback.set(self.conv_time)
            self.song_time['text'] = "track  length    {}:{}:{}/{}:{}:{}".format(current_hour, current_minute,current_sec, length_song_hour,length_song_minute, length_song_second)

    def reload_song(self):
        print("reloading")
        current_volume = self.volume_scale.get()
        print("current volume set: ",current_volume)
        self.terminate_thread = True
        self.player.delete()
        self.player = pyglet.media.Player()
        self.volume_scale.set(current_volume)
        self.player.volume = current_volume
        time.sleep(.03)  # make sures song plays properly without no hitches
        self.update_song()

    def garbage_collect(self):
        #print(gc.get_count())
        gc.collect()

    def no_playlist(self):
        tk.messagebox.showerror(title="Error", message="Error, please load a playlist first.")

    # loads/updates  song that is chosen
    def update_song(self):
        try:
            self.pick_song = self.songs[self.index]
            self.load = pyglet.media.load(self.pick_play_list + "/" + self.pick_song)          # defines the absolute path to the song
            self.player.next_source()                                                          # clears current song if any
            self.player.queue(self.load)

            # label below and place method clears title by updating with empty string
            self.song_title = tk.Label(text='                                                                                                                                                                                                                              ',background = self.background_color,width = 100,foreground =self.background_color)
            self.song_title.place(x=267, y=15, anchor="center")
            self.song_title = tk.Label(text=self.pick_song,background = self.background_color,width = 100,height = 2,foreground = self.text_color,font = "Arial 8 bold")
            self.song_title.place(x=267, y=15, anchor="center")
            self.play()
        except IndexError:
            pass

    def loop_song(self):
        self.loop_state = True  # allows current song to be repeated
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            if self.loop_message:
                tk.messagebox.showinfo(title="Sucess", message="Song has been looped.")
                self.loop_message = False  # set to false so messagebox above does not appear after first click
            self.status_bar["text"] = "Status: Playing"
            self.update_song()

    #shuffles songs list and set index at 0
    def shuffle_music(self):
        self.loop_state = False                                                          # set false to not loop song
        self.loop_message = True                                                         # reset loop message so that when loop_song() called message appears
        if not self.is_playlist_loaded:                                                  # if playlist isnt loaded shows error message for all buttons
            self.no_playlist()
        elif self.is_playlist_loaded:
            self.terminate_thread = True                                                 # terminate threads not in use
            random.shuffle(self.songs)
            self.index = 0
            self.status_bar["text"] = "Status: Playing"
            self.update_song()

    # adjust  index by -1
    def previous_song(self):
        self.loop_message = True
        self.loop_state = False
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            self.terminate_thread = True                                                # clears previous threads that were created by returning none
            self.index -= 1
            if self.index == -(len(self.songs) + 1):                                    # if index of song reaches more than its max index set index to -1
                self.index = -1
            self.status_bar["text"] = "Status: Playing"
            self.update_song()

    # adjust index  by +1
    def next_song(self):
            self.loop_message = True
            self.loop_state = False
            if not self.is_playlist_loaded:
                self.no_playlist()
            elif self.is_playlist_loaded:
                self.terminate_thread = True
                self.index += 1                                                         # if index of song reaches more than its max index set index to 0
                if self.index == len(self.songs):
                    self.index = 0
                self.status_bar["text"] = "Status: Playing"
                self.update_song()

    # loads playlist and sets shortcut keys to be functional
    def load_playlist(self):
        try:
            self.loop_message = True
            self.is_playlist_loaded = True
            self.index = 0
            self.songs = []
            self.status_bar["text"] = "Status: Playing"
            if self.changing_playlist:  # deletes if starting new playlist which need to be before 104-106 line otherwise it crashes
                self.player.delete()
            self.pick_play_list = tk.filedialog.askdirectory()
            self.song_list = os.listdir(self.pick_play_list)
            self.player = pyglet.media.Player()
            self.volume_scale.set(25)
            self.player.volume = .25
            for choose in self.song_list:
                self.songs.append(choose)
            self.changing_playlist = True  # when you change a playlist it deletes the player to make sure two songs do not play simultaneously
            self.update_song()
        except FileNotFoundError:
            self.loop_message = False
            self.is_playlist_loaded = False
            self.status_bar["text"] = "Status: None"

        # loads a specific song from playlist chosen cannot be another song file from another playlist throws error
    def load_song(self):
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            try:
                self.loop_state = False
                self.loop_message = True
                self.open_file = tk.filedialog.askopenfile()
                self.pick_song = str(self.open_file.name)
                self.find_name = self.pick_song.split("/")
                self.song_track = self.find_name[-1]  # picks out title of song
                if self.song_track in self.songs:
                    self.index = self.songs.index(
                        self.song_track)  # if user picks specific song, index changes to specific index of list if exists in song list
                    self.status_bar["text"] = "Status: Playing"
                    self.update_song()
                elif self.song_track not in self.songs:
                    tk.messagebox.showerror(title="Error",message="Error, file picked is invalid or not in playlist please try again.")
            except AttributeError:
                pass
            except PermissionError:
                tk.messagebox.showerror(title="Error",message="Error, file picked is invalid or not in playlist please try again.")

    def resume_song(self):
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            self.status_bar["text"] = "Status: Resumed"
            self.player.play()

    def pause_song(self):
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            self.status_bar["text"] = "Status: Paused"
            self.player.pause()

    def play(self):
        try:
            self.player.play()
            self.create_thread = threading.Thread(target=self.check_endofsong)  # start checking for end of song condition by initializing a thread
            self.create_thread.start()
            # whenever the player has problems remake the audio player code portion below
            if self.player.playing == False:
                self.reload_song()
        except ValueError:
            self.reload_song()

    def quit(self):
        self.done = True  # "destroys" threads by returning in a function to end them in order to properly shutdown the application window
        self.window.destroy()

    # finds specific position of the  volume scale  , volume range is 0.0(mute) -> 1.0(loud)
    def volume_adjust(self,delta):
        try:
            self.delta = int(delta) / 100
            self.player.volume = self.delta
        except AttributeError:
            pass

    # updates the song track time when user moves scales to a certain point of the song
    def update_song_time(self, event = None):
        try:
            self.value = self.time_playback.get()     # obatins value of the scale when user releases scale
            self.time_playback.set(int(self.value))
            self.player.seek(int(self.value))
            self.player.pause()
            time.sleep(.06)
            self.player.play()
        except AttributeError:
            pass

    # when song has ended, if loop_state is false, the next song plays
    def auto_play_next(self):
        self.time_playback.set(0)
        self.terminate_thread = False
        self.status_bar["text"] = "Status: Playing"
        self.index += 1
        if self.index == len(self.songs):  # when end index reached restart at index 0
            self.index = 0
        self.update_song()

    def check_endofsong(self):
        self.time_playback["to"] = int(self.load.duration)  # defines scale of song length

        if self.terminate_thread or threading.active_count() > 2:  # terminate threads that are not in use when you shuffle,play next/previous etc
            self.terminate_thread = False
            return None

        elif not self.terminate_thread:
            self.timeto_garbage = 0
            while True:
                time.sleep(1)
                self.timeto_garbage += 1
                # length(defines song length)  current time(current time in song) below
                self.length = int(self.load.duration)
                self.conv_time = int(self.player.time)
                self.current_time = self.conv_time
                if self.done:  # quits threads when quit condition is true and exits application
                    return None
                if self.timeto_garbage == 5:
                    self.garbage_collect()
                    self.timeto_garbage = 0
                if self.current_time == self.length + 1 or self.current_time == self.length + 2:
                    self.is_paused = False  #defines and interacts with pause button
                    break
                #obtain song time length format
                self.song_timeformat()
            if self.loop_state:
                self.loop_song()

            elif not self.loop_state:
                self.auto_play_next()

    def dark_light_mode(self):
        if self.dark_mode == True:  # turns off dark mode
            self.button_color = "#F0F0F0"
            self.background_color = "#FFFFFF"
            self.trough_color = "#F5F5F5"
            self.text_color = "#000000"
            self.dark_mode = False

            self.load_song_button["bg"] = self.button_color
            self.load_song_button["foreground"] = self.text_color
            self.load_playlist_button["bg"] = self.button_color
            self.load_playlist_button["foreground"] = self.text_color
            self.pause_button["bg"] = self.button_color
            self.pause_button["foreground"] = self.text_color
            self.resume_button["bg"] = self.button_color
            self.resume_button["foreground"] = self.text_color
            self.shuffle_button["bg"] = self.button_color
            self.shuffle_button["foreground"] = self.text_color
            self.next_button["bg"] = self.button_color
            self.next_button["foreground"] = self.text_color
            self.previous_button["bg"] = self.button_color
            self.previous_button["foreground"] = self.text_color
            self.loop_button["bg"] = self.button_color
            self.status_bar["background"] = self.button_color
            self.status_bar["foreground"] = self.text_color
            self.loop_button["foreground"] = self.text_color
            self.song_time["background"] = self.background_color
            self.song_time["foreground"] = self.text_color
            self.volume_scale["bg"] = self.background_color
            self.volume_scale["foreground"] = self.text_color
            self.volume_scale["troughcolor"] = self.trough_color
            self.time_playback["bg"] = self.background_color
            self.time_playback["foreground"] = self.text_color
            self.time_playback["troughcolor"] = self.trough_color
            self.volume_text["background"] = self.background_color
            self.volume_text["foreground"] = self.text_color
            self.window['background'] = self.background_color
            self.song_title["bg"] = self.background_color
            self.song_title["foreground"] = self.text_color

        elif self.dark_mode == False:   # turns on dark mode
            self.button_color = "#383838"
            self.background_color = "#282828"
            self.trough_color = "#808080"
            self.text_color = "#FFFFFF"
            self.dark_mode = True

            self.load_song_button["bg"] = self.button_color
            self.load_song_button["foreground"] = self.text_color
            self.load_playlist_button["bg"] = self.button_color
            self.load_playlist_button["foreground"] = self.text_color
            self.pause_button["bg"] = self.button_color
            self.pause_button["foreground"] = self.text_color
            self.resume_button["bg"] = self.button_color
            self.resume_button["foreground"] = self.text_color
            self.shuffle_button["bg"] = self.button_color
            self.shuffle_button["foreground"] = self.text_color
            self.next_button["bg"] = self.button_color
            self.next_button["foreground"] = self.text_color
            self.previous_button["bg"] = self.button_color
            self.previous_button["foreground"] = self.text_color
            self.loop_button["bg"] = self.button_color
            self.status_bar["background"] = self.button_color
            self.status_bar["foreground"] = self.text_color
            self.loop_button["foreground"] = self.text_color
            self.song_time["background"] = self.background_color
            self.song_time["foreground"] = self.text_color
            self.volume_scale["bg"] = self.background_color
            self.volume_scale["foreground"] = self.text_color
            self.volume_scale["troughcolor"] = self.trough_color
            self.time_playback["bg"] = self.background_color
            self.time_playback["foreground"] = self.text_color
            self.time_playback["troughcolor"] = self.trough_color
            self.volume_text["background"] = self.background_color
            self.volume_text["foreground"] = self.text_color
            self.window['background'] = self.background_color
            self.song_title["bg"] = self.background_color
            self.song_title["foreground"] = self.text_color

    def key_press(self, event):
        self.key = str(event.char)
        if self.key == 'q':
            if tk.messagebox.askyesno(title="Quit", message="Do you wish to quit?"):
                self.quit()
        else:
            if not self.is_playlist_loaded:
                if self.key == 'w':  # allows playlist to be loaded first
                    self.load_playlist()
                elif self.key == 'd'  or self.key == 'o' or self.key == 'e' or self.key == 's' or self.key == 'i' or self.key == '.' or self.key == ',' or self.key == "p":
                    self.no_playlist()
                else:
                    pass
            elif self.is_playlist_loaded:
                if self.key == 'w':
                    self.load_playlist()
                elif self.key == 'o':
                    self.next_song()
                elif self.key == 'i':
                    self.previous_song()
                elif self.key == 'e':
                    self.load_song()
                elif self.key == 's':
                    self.shuffle_music()
                elif self.key == "":        # key is crtl + z for changing dark/light modes
                    self.dark_light_mode()
                elif self.key == 'd':
                    self.loop_song()
                # player volume below chunks increase/decrease volume by 5 and defines the range of vol scale
                elif self.key == '.':
                    self.player.volume += (5 / 100)
                    self.volume_scale.set(self.player.volume * 100)
                    if self.player.volume >= 1.0:
                        self.player.volume = 1.0
                elif self.key == ',':
                    self.player.volume -= (5 / 100)
                    self.volume_scale.set(self.player.volume * 100)
                    if self.player.volume <= 0.0:
                        self.player.volume = 0
                # play/pause chunk
                elif self.key == "p" and self.is_paused == False:
                    self.is_paused = True
                    self.status_bar["text"] = "Status: Paused"
                    self.player.pause()
                elif self.key == "p" and self.is_paused == True:
                    self.is_paused = False
                    self.status_bar["text"] = "Status: Playing"
                    self.player.play()
                else:
                    pass

    # defines the properties of application window
    def __init__(self,window):
        # define variables to be used later in functions
        self.pick_song = None
        self.load = None
        self.song_title = None
        self.pick_play_list = None
        self.songs = None
        self.create_thread = None
        self.player=  None
        self.song_list = None
        self.find_name = None
        self.song_track = None
        self.length = None
        self.conv_time = None
        self.timeto_garbage = None
        self.key = None
        self.current_time = None
        self.value = None
        self.delta = None
        self.open_file = None

        self.button_color = "#383838"
        self.background_color = "#282828"
        self.trough_color = "#808080"
        self.text_color = "#FFFFFF"
        self.font = "ProximaNova 9 bold"

        self.index = 0                                  #song index
        self.done = False                               #quit condition
        self.is_playlist_loaded = False                 # determines the functionality of buttons and shortcut keys
        self.loop_state = False
        self.is_paused = False                          # defines pause and play condition
        self.terminate_thread = False                   # when terminate_thread = True we get rid of threads we dont use
        self.loop_message = True                        #loop messagebox when true it shows info box when song is looped
        self.changing_playlist = False  # when we change a new playlist, we delete the player and make a new one
        self.dark_mode = True  # changes light/dark mode of mp3 player

        self.window = window
        self.window['background'] = self.background_color
        self.window.title("Vibe Player")
        self.window.iconbitmap("sadcat.ico")
        self.window.geometry("585x200")

        self.load_song_button = tk.Button(window, text="Load specific song from playlist", height=1, width=30,command=self.load_song, borderwidth=1, bg=self.button_color,foreground=self.text_color, font=self.font, relief="solid")
        self.load_playlist_button = tk.Button(window, text="Load playlist", height=1, width=16,command=self.load_playlist, borderwidth=1, bg=self.button_color,foreground=self.text_color, font=self.font, relief="solid")
        self.pause_button = tk.Button(window, text="Pause", height=1, width=16, command=self.pause_song, borderwidth=1,bg=self.button_color, foreground=self.text_color, font=self.font, relief="solid")
        self.resume_button = tk.Button(window, text="Resume", height=1, width=16, command=self.resume_song, borderwidth=1,bg=self.button_color, foreground=self.text_color, font=self.font, relief="solid")
        self.shuffle_button = tk.Button(window, text="Shuffle", height=1, width=16, command=self.shuffle_music,borderwidth=1, bg=self.button_color, foreground=self.text_color, font=self.font,relief="solid")
        self.next_button = tk.Button(window, text="Next", height=1, width=15, command=self.next_song, borderwidth=1,bg=self.button_color, foreground=self.text_color, font=self.font, relief="solid")
        self.previous_button = tk.Button(window, text="Previous", height=1, width=16, command=self.previous_song,borderwidth=1, bg=self.button_color, foreground=self.text_color, font=self.font,relief="solid")
        self.loop_button = tk.Button(window, text="Loop song", height=1, width=16, command=self.loop_song, borderwidth=1,bg=self.button_color, foreground=self.text_color, font=self.font, relief="solid")
        self.song_time = tk.Label(window, text="track  length    0:00/0:00", background=self.background_color,width=100, foreground=self.text_color, font=self.font)
        self.volume_scale = tk.Scale(window, from_=100, to=0, orient=tk.VERTICAL, length=110, resolution=1,command=self.volume_adjust, bg=self.background_color, foreground="white",highlightthickness=0, troughcolor="#808080", font=self.font, sliderlength=10,width=10)
        self.volume_text = tk.Label(text="Volume", bg=self.background_color, foreground="white", font=self.font)
        self.time_playback = tk.Scale(window, from_=0, orient=tk.HORIZONTAL, length=400, resolution=1,bg=self.background_color, foreground="white", highlightthickness=0,troughcolor=self.trough_color, sliderlength=5, width=8, showvalue=0)
        self.status_bar = tk.Label(text="Status: None ", bg=self.button_color, foreground=self.text_color, font=self.font, width=200)

        self.time_playback.bind("<ButtonRelease-1>",self.update_song_time)  # event occurs when scale bar of song is released
        self.window.bind('<Key>', self.key_press)  # event occurs when keys pressede

        self.song_time.place(x=260, y=40, anchor="center")
        self.time_playback.place(x=260, y=67, anchor="center")

        self.pause_button.place(x=78, y=95, anchor="center")
        self.resume_button.place(x=204, y=95, anchor="center")
        self.previous_button.place(x=330, y=95, anchor="center")
        self.next_button.place(x=452, y=95, anchor="center")

        self.shuffle_button.place(x=260, y=125, anchor="center")
        self.loop_button.place(x=385, y=125, anchor="center")
        self.load_playlist_button.place(x=135, y=125, anchor="center")
        self.load_song_button.place(x=260, y=155, anchor="center")

        self.volume_scale.place(x=535, y=90, anchor="center")
        self.volume_text.place(x=570, y=157, anchor="e")
        self.status_bar.place(x=50, y=180, anchor="n")

# Start of the program
if __name__ == "__main__":
    # creation of application window and looping it (start of code)
    applic_window = tk.Tk()
    applic_window.resizable(width=False, height=False)
    mmedia = Mp3_player(applic_window)
    def on_exit():
        if tk.messagebox.askyesno(title="Quit", message="Do you wish to quit?"): # quit when clicking red x button and call protocal to sys.exit()
            mmedia.quit()
            exit()
    applic_window.protocol("WM_DELETE_WINDOW",on_exit)
    applic_window.mainloop()
    sys.exit()








