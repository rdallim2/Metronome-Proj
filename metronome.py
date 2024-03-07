import tkinter as tk
from tkinter import ttk
from fractions import Fraction 
import pygame
from tkinter import *
import customtkinter

class Metronome:
    def __init__(self):
        self.root = tk.Tk()
        self.custom_root = customtkinter.CTk()
        self.root.title('Metronome')
        self.root.geometry("300x500")
        self.root.configure(bg="white") 
        self.mainframe = tk.Frame(self.root)
        self.mainframe.pack(fill='both', expand=True)

        # DEFAULT MET INFO
        self.bpm = 120  # Default BPM
        self.playing = False
        self.weak_audio_path = "/Users/ryandallimore/persprojects/metronome_proj/met_sound.mp3"
        self.strong_audio_path = "/Users/ryandallimore/persprojects/metronome_proj/strongbeat.mp3"
        
        self.beat_count = 0
        self.beats_in_measure = 4 
        self.after_id = None  # To store the after event ID

        #METRONOME LABEL: ROW 0
        self.text = ttk.Label(self.mainframe, text='Metronome', background='white', font=("Brass Mono", 30))
        self.text.grid(row=0, column=0, pady=10)

        #TEMPO BUTTON: ROWS 1/2
        #self.set_tempo_button = ttk.Button(self.mainframe, text='Set Tempo', command=self.set_tempo)
        #self.set_tempo_button.grid(row=1, column=0, pady=10)
        #self.tempo_entry= ttk.Entry(self.mainframe)
        #self.tempo_entry.grid(row=2, column=0, pady=10, sticky='NWES')

        #TEMPO SLIDER
        self.tempo_slider = customtkinter.CTkSlider(self.custom_root, 
            from_=30,
            to=400,
            command=self.sliding
            )

        self.tempo_slider.grid(row=10, column=0, pady=10)

        #TIMESIG ENTRY: ROWS 3/4
        self.set_time_sig_button = ttk.Button(self.mainframe, text="Set Time Signature: ex-(a/b)", command=self.set_time_sig)
        self.set_time_sig_button.grid(row=3, column=0, pady=10)
        self.time_sig_entry = ttk.Entry(self.mainframe)
        self.time_sig_entry.grid(row=4, column=0, pady=10, sticky='NWES')

        #START BUTTON: ROW 5
        self.start_button = ttk.Button(self.mainframe, text="Start", command=self.start_metronome)
        self.start_button.grid(row=5, column=0, pady=10)

        #STOP BUTTON: ROW 6
        self.stop_button = ttk.Button(self.mainframe, text="Stop", command=self.stop_metronome)
        self.stop_button.grid(row=6, column=0, pady=10)

        


        #INITIALIZER
        pygame.mixer.init()

    def sliding(value):
        pass

    def set_tempo(self):
        try:
            new_bpm = int(self.tempo_entry.get())
            if new_bpm > 0:
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
