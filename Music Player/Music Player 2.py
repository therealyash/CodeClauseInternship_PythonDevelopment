from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
from tkinter import ttk
import random
import os

class MusicPlayer:
    def __init__(self, root):

        self.root = root

        self.root.title("Music Player")
        #self.root.configure(bg="blue")

        self.root.geometry("500x400")

        pygame.mixer.init()
        self.paused = False
        self.stopped = False
        self.head = ""
        self.tail = ""
        self.song_length = 0


        self.create_gui()

    def create_gui(self):
        title_label = Label(self.root, text="Music Player", font=("Helvetica", 20))
        title_label.pack(pady=10)

        self.song_box = Listbox(self.root, bg="gray", fg="white", width=65, height=12,
                                selectbackground="black", selectforeground="white")
        self.song_box.pack(pady=20)



        self.play_img = PhotoImage(file="icons/1play.png")
        self.back_img = PhotoImage(file="icons/2back.png")
        self.pause_img = PhotoImage(file="icons/3pause.png")
        self.forward_img = PhotoImage(file="icons/4forward.png")
        self.shuffle_img = PhotoImage(file="icons/5shuffle.png")

        self.controls_frame = Frame(self.root)
        self.controls_frame.pack()

        self.play_btn = Button(self.controls_frame, image=self.play_img, borderwidth=0, command=self.play)
        self.back_btn = Button(self.controls_frame, image=self.back_img, borderwidth=0, command=self.prev_song)
        self.pause_btn = Button(self.controls_frame, image=self.pause_img, borderwidth=0, command=self.toggle_pause)
        self.forward_btn = Button(self.controls_frame, image=self.forward_img, borderwidth=0, command=self.next_song)
        self.shuffle_btn = Button(self.controls_frame, image=self.shuffle_img, borderwidth=0, command=self.shuffle)

        self.play_btn.grid(row=0, column=2, padx=10)
        self.back_btn.grid(row=0, column=0, padx=10)
        self.pause_btn.grid(row=0, column=3, padx=10)
        self.forward_btn.grid(row=0, column=1, padx=10)
        self.shuffle_btn.grid(row=0, column=4, padx=10)

        # Add Songs Button
        self.add_songs_btn = Button(self.root, text="Add Songs", command=self.add_many_songs)
        self.add_songs_btn.pack()

        # Remove Songs Button
        self.remove_songs_btn = Button(self.root, text="Remove Songs", command=self.delete_songs)
        self.remove_songs_btn.pack()

        self.status_bar = Label(self.root, text='', bd=1, relief=GROOVE, anchor=E)
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=2)

        self.my_slider = ttk.Scale(self.root, from_=0, to=100, orient=HORIZONTAL,
                                   value=0, command=self.slide, length=380, cursor="hand2")
        self.my_slider.pack()
        self.slider_label = Label(self.root, text='00:00 / 00:00')
        self.slider_label.pack(pady=10)



    def play(self):
        self.stopped = False
        song = self.song_box.get(ACTIVE)
        song = f'{self.head}/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        self.my_slider.config(value=0)
        self.play_time()

    def add_many_songs(self):
        songs = filedialog.askopenfilenames(initialdir='audios/', title="Choose...",
                                            filetypes=(("mp3 Files", "*.mp3"),))
        for song in songs:
            self.head, self.tail = os.path.split(song)
            self.song_box.insert(END, self.tail[:-4])

    def delete_songs(self):
        self.stop()
        self.song_box.delete(0, END)
        pygame.mixer.music.stop()
    def toggle_pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def prev_song(self):
        self.slider_label.config(text='00:00 / 00:00')
        self.my_slider.config(value=0)
        prev_one = self.song_box.curselection()[0] - 1
        if prev_one == -1:
            prev_one = self.song_box.size() - 1
        self.play_song(prev_one)

    def next_song(self):
        self.slider_label.config(text='00:00 / 00:00')
        self.my_slider.config(value=0)
        next_one = self.song_box.curselection()[0] + 1
        if next_one == self.song_box.size():
            next_one = 0
        self.play_song(next_one)

    def play_song(self, song_index):
        song = self.song_box.get(song_index)
        song = f'{self.head}/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        self.song_box.selection_clear(0, END)
        self.song_box.selection_set(song_index)
        self.song_box.activate(song_index)

    def shuffle(self):
        active_song = self.song_box.get(ACTIVE)
        songs_list = list(self.song_box.get(0, END))
        self.song_box.delete(0, END)
        random.shuffle(songs_list)
        for i, song in enumerate(songs_list):
            self.song_box.insert(i, song)
            if song == active_song:
                self.song_box.selection_set(i)
                self.song_box.activate(i)
        self.song_box.update()

    def slide(self, val):
        self.my_slider.config(value=val)
        s_len = time.strftime('%M:%S', time.gmtime(self.song_length))
        new_time = time.strftime('%M:%S', time.gmtime(self.my_slider.get()))
        self.slider_label.config(text=f'{new_time} / {s_len}')
        pygame.mixer.music.play(-1, self.my_slider.get())



    def play_time(self):
        if self.stopped:
            return
        curr_time = pygame.mixer.music.get_pos() // 1000
        song = self.song_box.get(ACTIVE)
        song = f'{self.head}/{song}.mp3'
        song_mut = MP3(song)
        self.song_length = song_mut.info.length

        if int(self.my_slider.get()) == int(self.song_length):
            song_no = self.song_box.curselection()[0] + 1
            if song_no == self.song_box.size():
                song_no = 0
            self.play_song(song_no)
            self.slide(0)
        elif self.paused:
            pass
        elif int(self.my_slider.get()) == curr_time:
            slider_pos = int(self.song_length)
            self.my_slider.config(to=slider_pos, value=curr_time)
        else:
            slider_pos = int(self.song_length)
            self.my_slider.config(to=slider_pos, value=int(self.my_slider.get()))
            new_time = int(self.my_slider.get()) + 1
            self.my_slider.config(value=new_time)
        s_len = time.strftime('%M:%S', time.gmtime(self.song_length))
        new_time = time.strftime('%M:%S', time.gmtime(self.my_slider.get()))
        self.slider_label.config(text=f'{new_time} / {s_len}')
        self.status_bar.after(1000, self.play_time)

    def run(self):
        self.root.mainloop()

root = Tk()
music_player = MusicPlayer(root)
music_player.run()
