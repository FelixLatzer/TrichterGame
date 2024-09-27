class Player:
    def __init__(self, name:str):
        self.name = name
        self.selection_count:float = 0
        self.drink_count:float = 0

    def get_statistic(self):
        if self.selection_count == 0:
            return 0
        return round(self.drink_count/self.selection_count, 2)
