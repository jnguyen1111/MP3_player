import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import random , os , threading , pyglet , time , sys ,gc

class Mp3_player:
    def garbage_collect(self):
        gc.collect()

    # creates an error when the user presses a button/shortcut when the playlist is not loaded
    def no_playlist(self):
        tk.messagebox.showerror(title="Error", message="Error, please load a playlist first.")

    # loads/updates  song that is chosen
    def update_song(self):
        try:
            self.pick_song = self.songs[self.index]
            self.load = pyglet.media.load(self.pick_play_list + "/" + self.pick_song)          # defines the absolute path to the song
            self.player.next_source()                                                          # clears current song if any
            self.player.queue(self.load)
            # label below clears title by updating with empty string
            self.song_title = tk.Label(text='                                                                                                                                                                                                                              ',background = self.background_color,width = 100,foreground =self.background_color)
            self.song_title.place(x=267, y=15, anchor="center")
            self.song_title = tk.Label(text=self.pick_song,background = self.background_color,width = 100,height = 1,foreground = self.text_color,font = "Arial 8 bold")
            self.song_title.place(x=267, y=15, anchor="center")
            self.create_thread = threading.Thread(target=self.check_endofsong)                # start checking for end of song condition by initializing a thread
            self.create_thread.start()
            self.play()
        except IndexError:
            pass

    def loop_song(self):
        self.loop_state = True                                                               # allows current song to be repeated
        if not self.is_playlist_loaded:
            self.no_playlist()
        if self.loop_message:
            tk.messagebox.showinfo(title="Sucess", message="Song has been looped.")
            self.loop_message = False                                                        # set to false so messagebox above does not appear
        if self.is_playlist_loaded:
            self.update_song()

    #shuffles songs list and set index at 0
    def shuffle_music(self):
        self.loop_state = False                                                          # set false to not loop song
        self.loop_message = True                                                         # reset loop message so that when loop_song() called message appears
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            self.terminate_thread = True                                                 # terminate threads not in use
            random.shuffle(self.songs)
            self.index = 0
            self.garbage_collect()
            self.update_song()

    # adjust  index by -1
    def previous_song(self):
        self.loop_message = True
        self.loop_state = False
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            self.terminate_thread = True
            self.index -= 1
            if self.index == -(len(self.songs) + 1):                                    # if index of song reaches more than its max index set index to -1
                self.index = -1
            self.garbage_collect()
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
                self.garbage_collect()
                self.update_song()

    def load_playlist(self):
        try:
            self.index = 0
            self.is_playlist_loaded = True                                             # sets condition which allows other buttons to function
            self.songs = []
            self.pick_play_list = tk.filedialog.askdirectory()
            self.player = pyglet.media.Player()
            self.volume_scale.set(50)
            self.player.volume = .50
            self.song_list = os.listdir(self.pick_play_list)
            for choose in self.song_list:
                self.songs.append(choose)
            self.update_song()
        except FileNotFoundError:
            self.terminate_thread = True
            self.is_playlist_loaded = False
            pass

    # loads a specific song from playlist chosen
    def load_song(self):
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            try:
                self.open_file = tk.filedialog.askopenfile()
                self.pick_song = str(self.open_file.name)                             # obtain string of file path
                self.find_name = self.pick_song.split("/")
                self.song_track = self.find_name[-1]                                  # picks out title of song
                if self.song_track in self.songs:
                    self.index = self.songs.index(self.song_track)                    # if user picks specific song, index changes to specific index of list
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
            self.player.play()

    def pause_song(self):
        if not self.is_playlist_loaded:
            self.no_playlist()
        elif self.is_playlist_loaded:
            self.player.pause()

    def play(self):
        self.player.play()

    def quit(self):
        self.done = True                     # "destroys" threads by returning in a function to end them in order to properly shutdown the application window
        self.window.destroy()

    # finds specific position of the  volume scale  , volume range is 1.0->0.0
    def volume_adjust(self,delta):
        try:
            self.delta = delta
            self.delta = int(self.delta) / 100
            self.player.volume = self.delta
        except AttributeError:
            pass

    # when song has ended, if loop_state is false, the next song plays
    def auto_play_next(self):
            self.time_playback.set(0)
            self.terminate_thread = False
            self.index += 1
            if self.index == len(self.songs):                       #when end index reached restart at index 0
                self.index = 0
            self.garbage_collect()
            self.update_song()

    #checks when the song ends and  other conditions that are defined.
    def check_endofsong(self):
        self.time_playback["to"] = int(self.load.duration)
        if self.terminate_thread or threading.active_count() >3:                                   # terminate threads that are not in use when you shuffle,play next/previous
            self.terminate_thread = False
            self.n = 0
            return None
        elif not self.terminate_thread:
            self.n = 0
            while True:
                self.time_property.sleep(1)
                self.n += 1
                length = int(self.load.duration)
                self.current_time = int(self.player.time)
                if self.done:                                        # quits threads when quit condition is true
                    return None
                if self.n == 5:
                    self.garbage_collect()
                    self.n = 0
                if self.current_time == length + 1 or self.current_time == length + 2:
                    break

                length_song_hour = length // 3600
                length %= 3600
                length_song_minute = length // 60  # format length of song into minutes and seconds
                length %= 60
                length_song_second = length

                current_hour = self.current_time // 3600
                self.current_time %= 3600
                current_minute = self.current_time // 60
                self.current_time %= 60
                current_sec = self.current_time

                # address when songs are over 59 minutes formating and songs under 59 minutes
                if length_song_hour == 0:

                    if current_sec < 10:
                        current_sec = str(current_sec).zfill(2)
                        int(current_sec)

                    if length_song_second < 10:
                        length_song_second = str(length_song_second).zfill(2)
                        int(length_song_second)

                    self.time_playback.set(int(self.player.time))
                    self.song_time['text'] = "track  length    {}:{}/{}:{}".format(current_minute, current_sec,length_song_minute,length_song_second)  # sets the song time length for user to see

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

                    self.time_playback.set(int(self.player.time))
                    self.song_time['text'] = "track  length    {}:{}:{}/{}:{}:{}".format(current_hour, current_minute,current_sec, length_song_hour,length_song_minute,length_song_second)  # sets the song time length for user to see

            if self.loop_state:                                         #loop condition
                self.loop_song()
            elif not self.loop_state:                                   # next song condition
                self.auto_play_next()

    def key_press(self,event):
        self.key = str(event.char)
        if self.key == 'q':
            if tk.messagebox.askyesno(title="Quit", message="Do you wish to quit?"):
                self.quit()
        # if the playlist_loaded is false, throw error. If playlist_loaded is true, then give shortcut keys ability to function
        else:
            if not self.is_playlist_loaded:
                if self.key == 'w':
                    self.load_playlist()
                elif  self.key == 'd' or self.key == 'k' or self.key == 'l' or self.key == 'o'  or self.key =='e' or self.key == 's'  or self.key == 'i' or self.key == '.' or self.key == ',' or self.key == "p":
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
                elif self.key =='e':
                    self.load_song()
                elif self.key == 's':
                    self.shuffle_music()
                elif self.key == 'd':
                    self.loop_song()
                elif self.key == '.':
                    self.player.volume += (5 / 100)                 # increase volume by 5
                    self.volume_scale.set(self.player.volume*100)
                    if self.player.volume >= 1.0:                    # make sure the volume does not go over 100%
                        self.player.volume = 1.0
                elif self.key == ',':
                    self.player.volume -= (5 / 100)                 # decrease volume by 5
                    self.volume_scale.set(self.player.volume*100)
                    if self.player.volume <= 0.0:                    # make sure the volume does not go below 0%
                        self.player.volume = 0
                elif self.key == 'p' and self.press == 0:
                    self.player.pause()
                    self.press += 1
                elif self.key == "p" and self.press == 1:
                    self.player.play()
                    self.press = 0
                elif self.key == 'l':
                    self.player.seek(self.player.time + 10)
                    self.player.pause()
                    self.time_property.sleep(.06)
                    self.player.play()
                    if self.player.time > self.load.duration:
                        self.auto_play_next()
                elif self.key == 'k':
                    self.player.seek(self.player.time - 10)
                    self.player.pause()
                    self.time_property.sleep(.06)
                    self.player.play()
                else:
                    pass

    # defines the properties of application window
    def __init__(self,window , time_property):
        button_color = "#383838"
        self.background_color = "#282828"
        self.text_color = "#FFFFFF"
        self.font = "ProximaNova 9 bold"
        self.index = 0                                  #song index
        self.time_property = time_property                                #get time properties
        self.done = False                               #quit condition
        self.is_playlist_loaded = False
        self.loop_state = False
        self.press = 0                                  # defines pause and play condition
        self.terminate_thread = False                   # when terminate_thread = True we get rid of threads we dont use
        self.loop_message = True                        #loop messagebox when true it shows info box when song is looped
        self.change_time = False

        self.window = window
        self.window['background'] = self.background_color
        self.window.title("Vibe Player")
        self.window.geometry("585x172")
        self.load_song_button = tk.Button(window, text="Load specific song from playlist", height=1, width=30, command= self.load_song, borderwidth = 1,bg=button_color,foreground=self.text_color,font = self.font,relief="solid")
        self.load_playlist_button = tk.Button(window, text="Load playlist", height=1, width=16, command=self.load_playlist,borderwidth = 1,bg=button_color,foreground=self.text_color,font = self.font,relief="solid")
        self.pause_button = tk.Button(window, text="Pause", height=1, width=16, command=self.pause_song,borderwidth = 1,bg=button_color,foreground=self.text_color,font = self.font,relief="solid")
        self.resume_button = tk.Button(window, text="Resume", height=1, width=16, command=self.resume_song,borderwidth = 1,bg=button_color,foreground=self.text_color,font = self.font,relief="solid")
        self.shuffle_button = tk.Button(window, text="Shuffle", height=1, width=16, command=self.shuffle_music,borderwidth = 1,bg=button_color,foreground=self.text_color,font = self.font,relief="solid")
        self.next_button = tk.Button(window, text="Next", height=1, width=15, command=self.next_song,borderwidth = 1,bg=button_color,foreground=self.text_color,font = self.font,relief="solid")
        self.previous_button = tk.Button(window, text="Previous", height=1, width=16, command=self.previous_song,borderwidth = 1,bg=button_color,foreground=self.text_color,font = self.font,relief="solid")
        self.loop_button = tk.Button(window, text="Loop song", height=1, width=16, command=self.loop_song,borderwidth = 1,bg=button_color,foreground=self.text_color , font = self.font,relief="solid")
        self.song_time = tk.Label(self.window, text="track  length    0:00/0:00",background=self.background_color, width=100, foreground=self.text_color,font=self.font)
        self.volume_scale = tk.Scale(window, from_=100, to=0, orient=tk.VERTICAL, length=110, resolution=1,command=self.volume_adjust, bg=self.background_color, foreground="white",highlightthickness=0, troughcolor="#808080", font=self.font, sliderlength=10 , width = 10)
        self.volume_text = tk.Label(text="Volume", bg=self.background_color, foreground="white", font=self.font)
        self.time_playback = tk.Scale(window, from_=0 , orient=tk.HORIZONTAL, length=400, resolution=1, bg=self.background_color, foreground="white",highlightthickness=0, troughcolor="#808080", sliderlength= 5 , width = 8,showvalue = 0)

        self.window.bind('<Key>', self.key_press)

        self.song_time.place(x=260, y=40, anchor="center")
        self.time_playback.place(x = 260 , y = 67 , anchor = "center")

        self.pause_button.place(x=78, y=95, anchor="center")
        self.resume_button.place(x=204, y=95, anchor="center")
        self.previous_button.place(x=330, y=95, anchor="center")
        self.next_button.place(x=452, y=95, anchor="center")

        self.shuffle_button.place(x=260, y=125, anchor="center")
        self.loop_button.place(x=385, y=125, anchor="center")
        self.load_playlist_button.place(x=135, y=125, anchor="center")
        self.load_song_button.place(x=250, y=155, anchor="center")

        self.volume_scale.place(x=535, y=90, anchor="center")
        self.volume_text.place(x=570, y=157, anchor="e")

if __name__ == "__main__":
    # creation of application window and looping it (start of code)
    applic_window = tk.Tk()
    mmedia = Mp3_player(applic_window,time)
    applic_window.resizable(width=False, height=False)
    def on_exit():
        if tk.messagebox.askyesno(title="Quit", message="Do you wish to quit?"):         # quit when clicking red x button
            mmedia.quit()
            exit()
    applic_window.protocol("WM_DELETE_WINDOW",on_exit)
    applic_window.mainloop()
    sys.exit()








