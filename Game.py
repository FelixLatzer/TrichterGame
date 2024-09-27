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
        self.root = Tk()
        self.root.geometry("400x400")
        self.frm = ttk.Frame(self.root, padding=10, width=400, height=400)
        self.frm.grid(column=3, row=4)
        self.user_input = tkinter.StringVar()
        self.player_chosen_text = tkinter.StringVar()
        self.chosen_player: Player = None
        self.count_down = tkinter.StringVar()

        # Initial UI
        self.enter_name_label = ttk.Label(self.frm, text="Enter a Name")
        self.enter_name_label.grid(column=0, row=0)

        self.enter_name_entry = ttk.Entry(self.frm, textvariable=self.user_input)
        self.enter_name_entry.grid(column=1, row=0)

        self.add_player_button = ttk.Button(self.frm, text="Add player", command=self.__add_player_command)
        self.add_player_button.grid(column=0, row=1)

        self.start_game_button = ttk.Button(self.frm, text="Start game", command=self.__start_timer)
        self.start_game_button.grid(column=1, row=1)

        self.chosen_player_label = ttk.Label(self.frm, textvariable=self.player_chosen_text)
        self.chosen_player_label.grid(column=0, row=2)

        self.count_down_label = ttk.Label(self.frm, textvariable=self.count_down)
        self.count_down_label.grid(column=1, row=2)

        self.take_button = ttk.Button(self.frm, text="Take it!", command=self.__take_trichter)
        self.take_button.config(state="disabled")
        self.take_button.grid(column=0, row=3)

        self.dont_take_button = ttk.Button(self.frm, text="Don't take it!", command=self.__dont_take_trichter)
        self.dont_take_button.config(state="disabled")
        self.dont_take_button.grid(column=1, row=3)

        # Placeholder for player stats table
        self.stats_frame = ttk.Frame(self.frm)
        self.stats_frame.grid(column=0, row=4, columnspan=2)

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
        time_to_wait = 5  # 45 * 60 / len(self.player)
        timer_thread = threading.Thread(target=self.__time_based_action, args=(time_to_wait,))
        timer_thread.start()
        self.start_game_button.config(state="disabled")

    def __time_based_action(self, time_to_wait: int):
        self.count_down.set(f"{time_to_wait}s till next Trichter")
        count = time_to_wait
        while count > 0:
            time.sleep(1)
            count -= 1
            self.count_down.set(f"{count}s till next Trichter")

        player_number = randrange(0, len(self.player))
        self.chosen_player = self.player[player_number]
        self.chosen_player.selection_count += 1
        self.player_chosen_text.set(f"{self.chosen_player.name} has to take a TRICHTER")

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

        # Add headers for the table
        ttk.Label(self.stats_frame, text="Player Name", font=("Arial", 10, "bold")).grid(column=0, row=0)
        ttk.Label(self.stats_frame, text="Drink Count", font=("Arial", 10, "bold")).grid(column=1, row=0)
        ttk.Label(self.stats_frame, text="Selection Count", font=("Arial", 10, "bold")).grid(column=2, row=0)
        ttk.Label(self.stats_frame, text="Statistic", font=("Arial", 10, "bold")).grid(column=3, row=0)

        self.player.sort(key= lambda p: p.drink_count, reverse=True)

        # Add each player's stats
        for index, player in enumerate(self.player):
            ttk.Label(self.stats_frame, text=player.name).grid(column=0, row=index + 1)
            ttk.Label(self.stats_frame, text=str(player.drink_count)).grid(column=1, row=index + 1)
            ttk.Label(self.stats_frame, text=str(player.selection_count)).grid(column=2, row=index + 1)
            ttk.Label(self.stats_frame, text=str(player.get_statistic())).grid(column=3, row=index + 1)
