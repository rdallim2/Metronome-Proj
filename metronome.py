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
        self.root.geometry("900x1200")
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
            background="SpringGreen2")

        self.style.configure("Gray.TButton",
            background="mint cream")

        self.style.configure("Purple.TButton",
            background="MediumPurple3")


        # DEFAULT MET INFO
        self.bpm = 215  # Default BPM
        self.playing = False
        self.weak_audio_path = "/Users/ryandallimore/persprojects/metronome_proj/met_sound.mp3"
        self.strong_audio_path = "/Users/ryandallimore/persprojects/metronome_proj/strongbeat.mp3"
        
        self.selection = tk.StringVar(value="4/4")
        self.beat_count = 0
        self.beats_in_measure = 4
        self.numerator = 4
        self.denominator = 4
        self.sub_size = 4
        self.after_id = None  # To store the after event ID

        #-----------TIME-SIG TOGGLES

        self.accent_toggle = tk.IntVar(value=1)
        self.accent_toggle.set(1)

        self.quarter_toggle = tk.IntVar(value=1)
        self.quarter_toggle.set(1)

        self.eighth_toggle = tk.IntVar(value=1)
        self.eighth_toggle.set(0)

        self.sixteenth_e_toggle = tk.IntVar(value=1)
        self.sixteenth_e_toggle.set(0)

        self.sixteenth_a_toggle = tk.IntVar(value=1)
        self.sixteenth_a_toggle.set(0)



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
        

        self.four_four_button = ttk.Radiobutton(self.mainframe, text="4/4", command=lambda: self.button_clicked("4/4"), style="Gray.TButton")
        self.four_four_button.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E)

        self.three_four_button = ttk.Radiobutton(self.mainframe, text="3/4", command=lambda: self.button_clicked("3/4"), style="Gray.TButton")
        self.three_four_button.grid(row=2, column=3, columnspan=3, sticky=tk.W+tk.E)

        self.two_four_button = ttk.Radiobutton(self.mainframe, text="2/4", command=lambda: self.button_clicked("2/4"), style="Gray.TButton")
        self.two_four_button.grid(row=2, column=6, columnspan=3, sticky=tk.W+tk.E)

        self.five_four_button = ttk.Radiobutton(self.mainframe, text="5/4", command=lambda: self.button_clicked("5/4"), style="Gray.TButton")
        self.five_four_button.grid(row=2, column=9, columnspan=3, sticky=tk.W+tk.E)

        self.seven_four_button = ttk.Radiobutton(self.mainframe, text="7/4", command=lambda: self.button_clicked("7/4"), style="Gray.TButton")
        self.seven_four_button.grid(row=3, column=0, columnspan=3, sticky=tk.W+tk.E)

        self.two_two_button = ttk.Radiobutton(self.mainframe, text="2/2", command=lambda: self.button_clicked("2/2"), style="Gray.TButton")
        self.two_two_button.grid(row=3, column=3, columnspan=3, sticky=tk.W+tk.E)

        self.six_eight_button = ttk.Radiobutton(self.mainframe, text="6/8", command=lambda: self.button_clicked("6/8"), style="Gray.TButton")
        self.six_eight_button.grid(row=3, column=6, columnspan=3, sticky=tk.W+tk.E)

        self.nine_eight_button = ttk.Radiobutton(self.mainframe, text="9/8", command=lambda: self.button_clicked("9/8"), style="Gray.TButton")
        self.nine_eight_button.grid(row=3, column=9, columnspan=3, sticky=tk.W+tk.E)

        self.twelve_eight_button = ttk.Radiobutton(self.mainframe, text="12/8", command=lambda: self.button_clicked("12/8"), style="Gray.TButton")
        self.twelve_eight_button.grid(row=4, column=0, columnspan=3, sticky=tk.W+tk.E)

        self.three_eight_button = ttk.Radiobutton(self.mainframe, text="3/8", command=lambda: self.button_clicked("3/8"), style="Gray.TButton")
        self.three_eight_button.grid(row=4, column=3, columnspan=3, sticky=tk.W+tk.E)

        self.five_eight_button = ttk.Radiobutton(self.mainframe, text="5/8", command=lambda: self.button_clicked("5/8"), style="Gray.TButton")
        self.five_eight_button.grid(row=4, column=6, columnspan=3, sticky=tk.W+tk.E)

        self.seven_eight_button = ttk.Radiobutton(self.mainframe, text="7/8", command=lambda: self.button_clicked("7/8"), style="Gray.TButton")
        self.seven_eight_button.grid(row=4, column=9, columnspan=3, sticky=tk.W+tk.E)

        self.set_time_sig("4/4")
        self.toggle_time_sig_buttons("4/4")


        #-----------SUBDIVISION AND ACCENT BUTTONS

        self.accent_button = ttk.Button(self.mainframe, text=self.get_accent_button_text(), command=self.toggle_accent, style="Purple.TButton")
        self.accent_button.grid(row=5, column=2, sticky=tk.W+tk.E, columnspan=2)

        self.quarter_button = ttk.Button(self.mainframe, text=self.get_quarter_button_text(), command=self.toggle_quarter, style="Purple.TButton")
        self.quarter_button.grid(row=5, column=4, sticky=tk.W+tk.E, columnspan=2)

        self.eighth_button = ttk.Button(self.mainframe, text=self.get_eighth_button_text(), command=self.toggle_eighth, style="Purple.TButton")
        self.eighth_button.grid(row=5, column=6, sticky=tk.W+tk.E, columnspan=2)

        self.sixteenth_e_button = ttk.Button(self.mainframe, text=self.get_sixteenth_e_button_text(), command=self.toggle_sixteenth_e, style="Purple.TButton")
        self.sixteenth_e_button.grid(row=5, column=8, sticky=tk.W+tk.E, columnspan=2)

        self.sixteenth_a_button = ttk.Button(self.mainframe, text=self.get_sixteenth_a_button_text(), command=self.toggle_sixteenth_a, style="Purple.TButton")
        self.sixteenth_a_button.grid(row=5, column=10, sticky=tk.W+tk.E, columnspan=2)
        
        #-----------OTHER PAGE BUTTONS

        #SOUND OPTION BUTTON: ROW 1
        self.sound_options_button = ttk.Button(self.mainframe, text="Sound Options", style="SS.TButton", command=self.accent_toggle)
        self.sound_options_button.grid(row=1, column=3, pady=10, sticky=tk.W+tk.E, columnspan=2)

        # BUTTON TWO: ROW 1
        self.gap_creator_button = ttk.Button(self.mainframe, text="Gap Creator", style="SS.TButton")
        self.gap_creator_button.grid(row=1, column=7, pady=10, sticky=tk.W+tk.E, columnspan=2)


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
    
    #------------------- TIME-SIG BUTTON TEXT CHANGE FUNCTIONS
    
    def get_accent_button_text(self):
        return "Strong Accent" if self.accent_toggle.get() == 1 else "No Accent"

    def get_quarter_button_text(self):
        return "'1/4': ON " if self.quarter_toggle.get() == 1 else "'1/4': OFF"

    def get_eighth_button_text(self):
        return "'+': ON " if self.eighth_toggle.get() == 1 else "'+': OFF"

    def get_sixteenth_e_button_text(self):
        return "'e': ON " if self.sixteenth_e_toggle.get() == 1 else "'e': OFF"

    def get_sixteenth_a_button_text(self):
        return "'a': ON " if self.sixteenth_a_toggle.get() == 1 else "'a': OFF"
    


    def toggle_accent(self):
        if self.accent_toggle.get() == 0:
            self.accent_toggle.set(1)
            self.accent_button["text"] = "Strong Accent"
        else:
            self.accent_toggle.set(0)
            self.accent_button["text"] = "No Accent"

    def toggle_quarter(self):
        if self.quarter_toggle.get() == 0:
            self.quarter_toggle.set(1)
            self.quarter_button["text"] = "'1/4': ON"
        else:
            self.quarter_toggle.set(0)
            self.quarter_button["text"] = "'1/4: OFF"
        
    def toggle_eighth(self):
        if self.eighth_toggle.get() == 0:
            self.eighth_toggle.set(1)
            self.eighth_button["text"] = "'+': ON"
        else:
            self.eighth_toggle.set(0)
            self.eighth_button["text"] = "'+'': OFF"       

    def toggle_sixteenth_e(self):
        if self.sixteenth_e_toggle.get() == 0:
            self.sixteenth_e_toggle.set(1)
            self.sixteenth_e_button["text"] = "'e': ON"
        else:
            self.sixteenth_e_toggle.set(0)
            self.sixteenth_e_button["text"] = "'e'': OFF"    

    def toggle_sixteenth_a(self):
        if self.sixteenth_a_toggle.get() == 0:
            self.sixteenth_a_toggle.set(1)
            self.sixteenth_a_button["text"] = "'a': ON"
        else:
            self.sixteenth_a_toggle.set(0)
            self.sixteenth_a_button["text"] = "'a'': OFF"    

    #----------------TEMPO AND TIME SIG STUFF

    def button_clicked(self, button_text):
        self.stop_metronome()
        self.set_time_sig(button_text)
        self.toggle_time_sig_buttons(button_text)

    
    def set_tempo(self, value):
        try:
            new_bpm = int(self.tempo_slider.get())
            self.bpm = new_bpm
        except ValueError:
            pass

    def toggle_time_sig_buttons(self, selected_button):
        time_sig_buttons = {       
            "4/4": self.four_four_button,
            "3/4": self.three_four_button,
            "2/4": self.two_four_button,
            "5/4": self.five_four_button,
            "7/4": self.seven_four_button,
            "2/2": self.two_two_button,
            "6/8": self.six_eight_button,
            "9/8": self.nine_eight_button,
            "12/8": self.twelve_eight_button,
            "3/8": self.three_eight_button,
            "5/8": self.five_eight_button,
            "7/8": self.seven_eight_button,
        }


        # Disable all time signature buttons
        for button_text, button in time_sig_buttons.items():
            if button_text == selected_button:
                button.config(style="Green.TButton", state="normal")
            else:
                button.config(style="Gray.TButton", state="normal")



    def set_time_sig(self, value):
        try:
            time_sig = Fraction(value)

            numerator = time_sig.numerator
            denominator = time_sig.denominator

            if denominator == 2:
                self.beats_in_measure = 4
                self.beat_count = (self.beats_in_measure - 0.25)
            elif denominator == 4:
                self.beats_in_measure = numerator
                self.beat_count = (self.beats_in_measure - 0.25)
            elif denominator == 8:
                self.beats_in_measure = (numerator / 2)
                self.beat_count = (self.beats_in_measure - 0.25)
            else:
                pass
        except ValueError:
            pass


    def play_metronome(self):
        try:
            if self.playing:
                volume = 1.0
                sub_beats_per_beat = 4  # Adjust this based on your requirement

                if self.accent_toggle.get() == 1:
                    if (self.beat_count * sub_beats_per_beat) % (self.beats_in_measure * sub_beats_per_beat) == 0:
                        volume = 1.0
                        pygame.mixer.music.load(self.strong_audio_path)
                    else:
                        pygame.mixer.music.load(self.strong_audio_path)
                        volume = 0.0
                else:
                    pygame.mixer.music.load(self.strong_audio_path)
                    volume = 0.0
                
                if self.quarter_toggle.get() == 1 and not ((self.beat_count * sub_beats_per_beat) % (self.beats_in_measure * sub_beats_per_beat) == 0):
                    if (self.beat_count * sub_beats_per_beat) % sub_beats_per_beat == 0:
                        pygame.mixer.music.load(self.weak_audio_path)
                        volume = 1.0
                    else:
                        pygame.mixer.music.load(self.weak_audio_path)
                        volume = 0.0
                
                if self.eighth_toggle.get() == 1:
                    eighth_position = (self.beat_count * sub_beats_per_beat * 2) % (sub_beats_per_beat * 2)
                    if eighth_position == 4:  # Adjust as needed
                        pygame.mixer.music.load(self.weak_audio_path)
                        volume = 0.15
                    else:
                        pass

                if self.sixteenth_e_toggle.get() == 1:
                    sixteenth_e_position = (self.beat_count * sub_beats_per_beat * 2) % (sub_beats_per_beat * 2)
                    if sixteenth_e_position == 2:  # Adjust as needed
                        pygame.mixer.music.load(self.weak_audio_path)
                        volume = 0.15
                    else:
                        pass

                if self.sixteenth_a_toggle.get() == 1:
                    sixteenth_a_position = (self.beat_count * sub_beats_per_beat * 2) % (sub_beats_per_beat * 2)
                    if sixteenth_a_position == 6:  # Adjust as needed
                        pygame.mixer.music.load(self.weak_audio_path)
                        volume = 0.15
                    else:
                        pass

                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops=0)
                if self.beat_count < self.beats_in_measure:
                    self.beat_count += 0.25
                else:
                    self.beat_count = 0.25
                self.after_id = self.root.after(int(15000 / (self.bpm)), self.play_metronome)

        except Exception as e:
            print(f"An error occurred while playing the metronome: {e}")



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
