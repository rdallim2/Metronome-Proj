import tkinter as tk
from tkinter import ttk
from fractions import Fraction 
import pygame
from tkinter import *
from PIL import ImageTk, Image
import customtkinter

class Metronome:
    def __init__(self):
        self.playing = False
        self.root = tk.Tk()
        #self.root = customtkinter.CTk()
        self.root.title('Metronome')
        self.root.geometry("450x600")
        self.root.configure() 
        self.mainframe = ttk.Frame(self.root, style="Main.TFrame")
        self.mainframe.pack(fill='both', expand=True)

        #ROWS AND COLUMNS
        for i in range(12):
            self.mainframe.columnconfigure(i, weight=1)

        for i in range(12):
            self.mainframe.rowconfigure(i, weight=1)


        #STYLE
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        self.style.configure("Main.TFrame", background="gray26", foreground="gray26", border="gray26")

        self.style.configure("SS.TButton",
            background="orange",
            foreground="gray26",
            border="gray26"
            ) 

        self.style.configure("Green.TButton", 
            background="SpringGreen3")

        self.style.configure("Purple.TButton",
            background="MediumPurple3")


        # DEFAULT MET INFO
        self.bpm = 215  # Default BPM
        self.playing = False
        self.weak_audio_path = "/Users/ryandallimore/persprojects/metronome_proj/met_sound.mp3"
        self.strong_audio_path = "/Users/ryandallimore/persprojects/metronome_proj/strongbeat.mp3"
        
        self.beat_count = 0
        self.beats_in_measure = 4 
        self.after_id = None  # To store the after event ID

        self.accent_toggle = tk.IntVar(value=1)
        self.accent_toggle.set(1)

        #METRONOME LABEL: ROW 0
        self.text = ttk.Label(self.mainframe, text='Metronome', foreground='orange', background="gray26", font=("Brass Mono", 30))
        self.text.grid(row=0, column=5, pady=10, columnspan=2)

        #TEMPO SLIDER
        self.tempo_slider = Scale(self.root, 
            from_=30,
            to=400,
            orient=HORIZONTAL,
            command=self.set_tempo,
            bd=0,  # Set border width to 0
            highlightthickness=0
            )
        self.tempo_slider.set(215)
        self.tempo_slider.pack(side='bottom', pady=10)

        #-----------TIME SIGNATURE BUTTONS
        

        self.four_four_button = ttk.Button(self.mainframe, text="4/4", command=lambda: self.set_time_sig("4/4"), style="Green.TButton")
        self.four_four_button.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E)

        self.three_four_button = ttk.Button(self.mainframe, text="3/4", command=lambda: self.set_time_sig("3/4"), style="Green.TButton")
        self.three_four_button.grid(row=2, column=3, columnspan=3, sticky=tk.W+tk.E)

        self.two_four_button = ttk.Button(self.mainframe, text="2/4", command=lambda: self.set_time_sig("2/4"), style="Green.TButton")
        self.two_four_button.grid(row=2, column=6, columnspan=3, sticky=tk.W+tk.E)

        self.five_four_button = ttk.Button(self.mainframe, text="5/4", command=lambda: self.set_time_sig("5/4"), style="Green.TButton")
        self.five_four_button.grid(row=2, column=9, columnspan=3, sticky=tk.W+tk.E)

        self.seven_four_button = ttk.Button(self.mainframe, text="7/4", command=lambda: self.set_time_sig("7/4"), style="Green.TButton")
        self.seven_four_button.grid(row=3, column=0, columnspan=3, sticky=tk.W+tk.E)

        self.two_two_button = ttk.Button(self.mainframe, text="2/2", command=lambda: self.set_time_sig("2/2"), style="Green.TButton")
        self.two_two_button.grid(row=3, column=3, columnspan=3, sticky=tk.W+tk.E)

        self.six_eight_button = ttk.Button(self.mainframe, text="6/8", command=lambda: self.set_time_sig("6/8"), style="Green.TButton")
        self.six_eight_button.grid(row=3, column=6, columnspan=3, sticky=tk.W+tk.E)

        self.nine_eight_button = ttk.Button(self.mainframe, text="9/8", command=lambda: self.set_time_sig("9/8"), style="Green.TButton")
        self.nine_eight_button.grid(row=3, column=9, columnspan=3, sticky=tk.W+tk.E)

        self.twelve_eight_button = ttk.Button(self.mainframe, text="12/8", command=lambda: self.set_time_sig("12/8"), style="Green.TButton")
        self.twelve_eight_button.grid(row=4, column=0, columnspan=3, sticky=tk.W+tk.E)

        self.three_eight_button = ttk.Button(self.mainframe, text="3/8", command=lambda: self.set_time_sig("3/8"), style="Green.TButton")
        self.three_eight_button.grid(row=4, column=3, columnspan=3, sticky=tk.W+tk.E)

        self.five_eight_button = ttk.Button(self.mainframe, text="5/8", command=lambda: self.set_time_sig("5/8"), style="Green.TButton")
        self.five_eight_button.grid(row=4, column=6, columnspan=3, sticky=tk.W+tk.E)

        self.seven_eight_button = ttk.Button(self.mainframe, text="7/8", command=lambda: self.set_time_sig("7/8"), style="Green.TButton")
        self.seven_eight_button.grid(row=4, column=9, columnspan=3, sticky=tk.W+tk.E)


        #-----------SUBDIVISION AND ACCENT BUTTONS

        self.accent_button = ttk.Button(self.mainframe, text=self.get_accent_button_text(), command=self.toggle_accent, style="Purple.TButton")
        self.accent_button.grid(row=5, column=0, sticky=tk.W+tk.E, columnspan=2)

        self.quarter_button = ttk.Button(self.mainframe, text="1/4", command=self.toggle_subdivisions("1/4"), style="Purple.TButton")
        self.quarter_button.grid(row=5, column=3, sticky=tk.W+tk.E, columnspan=2)

        self.sixteen_e_button = ttk.Button(self.mainframe, text="e", command=self.toggle_subdivisions("16e"), style="Purple.TButton")
        self.sixteen_e_button.grid(row=5, column=6, sticky=tk.W+tk.E)

        self.sixteen_and_button = ttk.Button(self.mainframe, text="+", command=self.toggle_subdivisions("16and"), style="Purple.TButton")
        self.sixteen_and_button.grid(row=5, column=7, sticky=tk.W+tk.E)

        self.sixteen_a_button = ttk.Button(self.mainframe, text="a", command=self.toggle_subdivisions("16a"), style="Purple.TButton")
        self.sixteen_a_button.grid(row=5, column=8, sticky=tk.W+tk.E)

        self.eighth_trip_and_button = ttk.Button(self.mainframe, text="+", command=self.toggle_subdivisions("8tripand"), style="Purple.TButton")
        self.eighth_trip_and_button.grid(row=5, column=10, sticky=tk.W+tk.E)

        self.eighth_trip_a_button = ttk.Button(self.mainframe, text="a", command=self.toggle_subdivisions("8tripa"), style="Purple.TButton")
        self.eighth_trip_a_button.grid(row=5, column=10, sticky=tk.W+tk.E)

        
        #-----------OTHER PAGE BUTTONS

        #SOUND OPTION BUTTON: ROW 1
        self.sound_options_button = ttk.Button(self.mainframe, text="Sound Options", style="SS.TButton", command=self.accent_toggle)
        self.sound_options_button.grid(row=1, column=2, pady=10, sticky=tk.W+tk.E, columnspan=2)

        # BUTTON TWO: ROW 1
        self.gap_creator_button = ttk.Button(self.mainframe, text="Gap Creator", style="SS.TButton")
        self.gap_creator_button.grid(row=1, column=5, pady=10, sticky=tk.W+tk.E, columnspan=2)

        # BUTTON THREE: ROW 1
        self.set_list_button = ttk.Button(self.mainframe, text="Set List", style="SS.TButton")
        self.set_list_button.grid(row=1, column=8, pady=10, sticky=tk.W+tk.E, columnspan=2)


        #-------------START-STOP BUTTONS
        #START BUTTON: ROW 6
        self.start_button = ttk.Button(self.mainframe, text="Start", command=self.start_metronome, style="SS.TButton")
        self.start_button.grid(row=6, column=3, pady=10, columnspan=2, sticky=tk.W+tk.E)

        #STOP BUTTON: ROW 6
        self.stop_button = ttk.Button(self.mainframe, text="Stop", command=self.stop_metronome, style="SS.TButton")
        self.stop_button.grid(row=6, column=7, pady=10, columnspan=2, sticky=tk.W+tk.E)
        #INITIALIZER
        pygame.mixer.init()




    #----------------------------------FUNCTIONS-----------------------------------------------------------------------
    def get_accent_button_text(self):
        return "Strong Accent" if self.accent_toggle.get() == 1 else "No Accent"

    def toggle_accent(self):
        if self.accent_toggle.get() == 0:
            self.accent_toggle.set(1)
            self.accent_button["text"] = "Strong Accent"
        else:
            self.accent_toggle.set(0)
            self.accent_button["text"] = "No Accent"
        

    def toggle_subdivisions(self, value):
        try:
            new_bpm = int(self.tempo_slider.get())
            self.bpm = new_bpm
        except ValueError:
            pass        #PLACEHOLDER
    
    def set_tempo(self, value):
        try:
            new_bpm = int(self.tempo_slider.get())
            self.bpm = new_bpm
        except ValueError:
            pass

    def set_time_sig(self, value):
        try:
            time_sig_input = int(self.time_sig_entry.get())
            time_sig = Fraction(time_sig_input)

            numerator = time_sig.numerator
            denominator = time_sig.denominator


            self.beats_in_measure = time_sig_input
        except ValueError:
            pass


    def play_metronome(self):
        try:
            if self.playing:
                if self.accent_toggle.get() == 1:
                    if (self.beat_count) % (self.beats_in_measure) == 0:
                        pygame.mixer.music.load(self.strong_audio_path)
                    else:
                        pygame.mixer.music.load(self.weak_audio_path)
                else:
                    pygame.mixer.music.load(self.weak_audio_path)

                pygame.mixer.music.play(loops=0)
                self.beat_count += 1
                self.after_id = self.root.after(int(60000 / self.bpm), self.play_metronome)

        except Exception as e:
            print(f"An error occurred while playing the metronome: {e}")
        

    def start_metronome(self):
        if not self.playing:
            self.playing = True
            self.play_metronome()
            self.metronome_thread = threading.Thread(target=self.play_metronome)
            self.metronome_thread.start()

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
