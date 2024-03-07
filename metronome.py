import tkinter as tk
from tkinter import ttk
from fractions import Fraction 
import pygame
from tkinter import *
from PIL import ImageTk, Image
import customtkinter

class Metronome:
    def __init__(self):
        self.root = tk.Tk()
        #self.root = customtkinter.CTk()
        self.root.title('Metronome')
        self.root.geometry("450x600")
        self.root.resizable(0,0)
        self.root.configure() 
        self.mainframe = ttk.Frame(self.root, style="Main.TFrame")
        self.mainframe.pack(fill='both', expand=True)

        #ROWS AND COLUMNS
        self.mainframe.columnconfigure((0, 1), weight=1)
        self.mainframe.rowconfigure(0)
        self.mainframe.rowconfigure(1, weight=1)


        #STYLE
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        self.style.configure("Main.TFrame", background="gray20")

        self.style.configure("SS.TButton",
            background="orange",
            foreground="gray25"
            ) 

        # DEFAULT MET INFO
        self.bpm = 215  # Default BPM
        self.playing = False
        self.weak_audio_path = "/Users/ryandallimore/persprojects/metronome_proj/met_sound.mp3"
        self.strong_audio_path = "/Users/ryandallimore/persprojects/metronome_proj/strongbeat.mp3"
        
        self.beat_count = 0
        self.beats_in_measure = 4 
        self.after_id = None  # To store the after event ID

        #METRONOME LABEL: ROW 0
        self.text = ttk.Label(self.mainframe, text='Metronome', foreground='orange', font=("Brass Mono", 30))
        self.text.grid(row=0, column=0, pady=10, columnspan=3)

        #TEMPO SLIDER
        self.tempo_slider = Scale(self.root, 
            from_=30,
            to=400,
            orient=HORIZONTAL,
            command=self.set_tempo,
            )
        self.tempo_slider.set(215)
        self.tempo_slider.pack(side='bottom', pady=10)


        #START BUTTON: ROW 5
        self.start_button = ttk.Button(self.mainframe, text="Start", command=self.start_metronome, width=10, style="SS.TButton")
        self.start_button.grid(row=6, column=0, pady=10, sticky='ew')

        #STOP BUTTON: ROW 6
        self.stop_button = ttk.Button(self.mainframe, text="Stop", command=self.stop_metronome, width=10, style="SS.TButton")
        self.stop_button.grid(row=6, column=1, pady=10, sticky='ew')

        #INITIALIZER
        pygame.mixer.init()




    #----------------------------------FUNCTIONS-----------------------------------------------------------------------

    def set_tempo(self, value):
        try:
            new_bpm = int(self.tempo_slider.get())
            self.bpm = new_bpm
        except ValueError:
            pass

    def set_time_sig(self):
        try:
            time_sig_input = int(self.time_sig_entry.get())
            time_sig = Fraction(time_sig_input)

            numerator = time_sig.numerator
            denominator = time_sig.denominator


            self.beats_in_measure = time_sig_input
        except ValueError:
            pass


    def play_metronome(self):
        if (self.beat_count) % (self.beats_in_measure) == 0:
            pygame.mixer.music.load(self.strong_audio_path)
        else:
            pygame.mixer.music.load(self.weak_audio_path)
        
        pygame.mixer.music.play(loops=0)
        self.beat_count += 1
        self.after_id = self.root.after(int(60000 / self.bpm), self.play_metronome)

    def start_metronome(self):
        if not self.playing:
            self.playing = True
            self.play_metronome()

    def stop_metronome(self):
        if self.playing:
            self.playing = False
            self.beat_count = 0
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    metronome = Metronome()
    metronome.run()
