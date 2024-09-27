import threading
import time
import tkinter
from random import randrange
from tkinter import *
from tkinter import ttk

from Player import Player

class Game:
    def __init__(self):
        self.player = []

    def start_game(self):
        # Create the root window and resize it to take more space
        self.root = Tk()
        self.root.geometry("800x600")  # Increase the window size
        self.root.title("Matzes Trichterspaß")

        # Create the main frame with padding and larger size
        self.frm = ttk.Frame(self.root, padding=20, width=800, height=600)
        self.frm.grid(column=0, row=0, padx=50, pady=50)  # Center with padding

        # Variables
        self.user_input = tkinter.StringVar()
        self.player_chosen_text = tkinter.StringVar()
        self.chosen_player = None
        self.count_down = tkinter.StringVar()

        # Larger labels and entry
        self.enter_name_label = ttk.Label(self.frm, text="Enter a Name", font=("Arial", 16, "bold"))
        self.enter_name_label.grid(column=0, row=0, columnspan=2, pady=10)  # Center horizontally

        self.enter_name_entry = ttk.Entry(self.frm, textvariable=self.user_input, font=("Arial", 16), width=30)
        self.enter_name_entry.grid(column=0, row=1, columnspan=2, pady=10)

        # Larger buttons
        self.add_player_button = ttk.Button(self.frm, text="Add player", command=self.__add_player_command, width=20)
        self.add_player_button.grid(column=0, row=2, pady=10, padx=10)

        self.start_game_button = ttk.Button(self.frm, text="Start game", command=self.__start_timer, width=20)
        self.start_game_button.grid(column=1, row=2, pady=10, padx=10)

        # Chosen player and countdown labels
        self.chosen_player_label = ttk.Label(self.frm, textvariable=self.player_chosen_text, font=("Arial", 16, "bold"), foreground="red")
        self.chosen_player_label.grid(column=0, row=3, pady=10,)

        self.count_down_label = ttk.Label(self.frm, textvariable=self.count_down, font=("Arial", 16, "bold"))
        self.count_down_label.grid(column=1, row=3, pady=10)

        # Larger action buttons and center them
        self.take_button = ttk.Button(self.frm, text="Take it!", command=self.__take_trichter, width=20)
        self.take_button.config(state="disabled")
        self.take_button.grid(column=0, row=4, pady=10, padx=10)

        self.dont_take_button = ttk.Button(self.frm, text="Don't take it!", command=self.__dont_take_trichter, width=20)
        self.dont_take_button.config(state="disabled")
        self.dont_take_button.grid(column=1, row=4, pady=10, padx=10)

        # Placeholder for player stats table, centered across both columns
        self.stats_frame = ttk.Frame(self.frm)
        self.stats_frame.grid(column=0, row=5, columnspan=2, pady=20)

        # Start the main loop
        self.root.mainloop()

    def __add_player_command(self):
        name = self.user_input.get()
        if any(player.name == name for player in self.player) or not name:
            return
        player = Player(name)
        self.player.append(player)
        self.user_input.set("")
        self.__update_stats_table()

    def __start_timer(self):
        self.player_chosen_text.set("")
        time_to_wait = 60 * 60 / len(self.player)
        timer_thread = threading.Thread(target=self.__time_based_action, args=(time_to_wait,))
        timer_thread.start()
        self.start_game_button.config(state="disabled")

    def __time_based_action(self, time_to_wait: int):
        count = int(time_to_wait)
        while count > 0:
            time.sleep(1)
            count -= 1
            minutes:int = int(count/60)
            seconds:int = int(count%60)
            self.count_down.set(f"{minutes}m{seconds}s left")

        player_number = randrange(0, len(self.player))
        self.chosen_player = self.player[player_number]
        self.chosen_player.selection_count += 1
        self.player_chosen_text.set(f"{self.chosen_player.name} was chosen")

        self.take_button.config(state="normal")
        self.dont_take_button.config(state="normal")
        self.start_game_button.config(state="normal")

    def __dont_take_trichter(self):
        self.take_button.config(state="disabled")
        self.dont_take_button.config(state="disabled")
        self.__update_stats_table()  # Update table after drinking

    def __take_trichter(self):
        self.chosen_player.drink_count += 1
        self.__update_stats_table()  # Update table after drinking
        self.take_button.config(state="disabled")
        self.dont_take_button.config(state="disabled")

    def __update_stats_table(self):
        # Clear existing widgets in the stats frame
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Create styles for alternating row colors and centering text
        style = ttk.Style()
        style.configure("Odd.TLabel", background="lightgrey", anchor="center")
        style.configure("Even.TLabel", background="white", anchor="center")

        # Add headers for the table
        ttk.Label(self.stats_frame, text="Player Name", font=("Arial", 10, "bold")).grid(column=0, row=0, padx=10)
        ttk.Label(self.stats_frame, text="Drink Count", font=("Arial", 10, "bold")).grid(column=1, row=0, padx=10)
        ttk.Label(self.stats_frame, text="Selection Count", font=("Arial", 10, "bold")).grid(column=2, row=0, padx=10)
        ttk.Label(self.stats_frame, text="Statistic", font=("Arial", 10, "bold")).grid(column=3, row=0, padx=10)

        self.player.sort(key= lambda p: p.drink_count, reverse=True)

        # Add each player's stats
        for index, player in enumerate(self.player):
            style_name = "Even.TLabel" if index%2 == 0 else "Odd.TLabel"
            ttk.Label(self.stats_frame, text=player.name, style=style_name).grid(column=0, row=index + 1, sticky="nsew")
            ttk.Label(self.stats_frame, text=str(player.drink_count), style=style_name).grid(column=1, row=index + 1, sticky="nsew")
            ttk.Label(self.stats_frame, text=str(player.selection_count), style=style_name).grid(column=2, row=index + 1, sticky="nsew")
            ttk.Label(self.stats_frame, text=str(player.get_statistic()), style=style_name).grid(column=3, row=index + 1, sticky="nsew")
