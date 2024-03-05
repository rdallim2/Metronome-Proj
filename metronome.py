import tkinter as tk
from tkinter import ttk
import pygame

class Metronome:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Metronome')
        self.root.geometry("300x300")
        self.root.configure(bg="white") 
        self.mainframe = tk.Frame(self.root)
        self.mainframe.pack(fill='both', expand=True)

        self.bpm = 120  # Default BPM
        self.playing = False
        self.audio_path = "/Users/ryandallimore/persprojects/met_sound.mp3"
        self.after_id = None  # To store the after event ID

        self.text = ttk.Label(self.mainframe, text='Metronome', background='white', font=("Brass Mono", 20))
        self.text.grid(row=0, column=0, pady=10)

        self.set_text_field = ttk.Entry(self.mainframe)
        self.set_text_field.grid(row=1, column=0, pady=10, sticky='NWES')
        set_text_button = ttk.Button(self.mainframe, text='Set Tempo', command=self.set_tempo)
        set_text_button.grid(row=2, column=0, pady=10)

        self.start_button = ttk.Button(self.mainframe, text="Start", command=self.start_metronome)
        self.start_button.grid(row=3, column=0, pady=10)

        self.stop_button = ttk.Button(self.mainframe, text="Stop", command=self.stop_metronome)
        self.stop_button.grid(row=4, column=0, pady=10)

        pygame.mixer.init()

    def set_tempo(self):
        try:
            new_bpm = int(self.set_text_field.get())
            if new_bpm > 0:
                self.bpm = new_bpm
        except ValueError:
            pass

    def play_metronome(self):
        pygame.mixer.music.load(self.audio_path)
        pygame.mixer.music.play(loops=0)
        self.after_id = self.root.after(int(60000 / self.bpm), self.play_metronome)

    def start_metronome(self):
        if not self.playing:
            self.playing = True
            self.play_metronome()

    def stop_metronome(self):
        if self.playing:
            self.playing = False
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    metronome = Metronome()
    metronome.run()
