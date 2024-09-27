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
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid(column=2, columnspan=150, row=3, rowspan=150)
        self.user_input = tkinter.StringVar()
        self.chosen_player = tkinter.StringVar()
        self.count_down = tkinter.StringVar()
        self.__init_ui()
        self.root.mainloop()

    def __init_ui(self):
        ttk.Label(self.frm, text="Enter a Name").grid(column=0, row=0)
        ttk.Entry(self.frm, textvariable=self.user_input).grid(column=1, row=0)
        ttk.Button(self.frm, text="Add player", command=self.__add_player_command).grid(column=0, row=1)
        ttk.Button(self.frm, text="Start game", command=self.__start_timer).grid(column=1, row=1)
        ttk.Label(self.frm, textvariable=self.chosen_player).grid(column=0, row=2)
        ttk.Label(self.frm, textvariable=self.count_down).grid(column=1, row=2)

    def __add_player_command(self):
        name = self.user_input.get()
        if any(player.name == name for player in self.player):
            return
        player = Player(name)
        self.player.append(player)
        self.user_input.set("")

    def __start_timer(self):
        self.chosen_player.set("")
        time_to_wait = 5#45*60/len(self.player)
        timer_thread = threading.Thread(target=self.__time_based_action, args=(time_to_wait,))
        timer_thread.start()

    def __time_based_action(self, time_to_wait:int):
        self.count_down.set(f"{time_to_wait}s till next Trichter")
        count = time_to_wait
        while count > 0:
            time.sleep(1)
            count -= 1
            self.count_down.set(f"{count}s till next Trichter")
        player_number = randrange(0, len(self.player))
        chosen_player = self.player[player_number]
        self.chosen_player.set(f"{chosen_player.name} has to take a TRICHTER")
