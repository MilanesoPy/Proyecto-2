class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def __str__(self) -> str:
        if not self.is_revealed:
            return "P" if self.is_flagged else "□"
        if self.is_mine:
            return "*"
        return str(self.adjacent_mines) if self.adjacent_mines > 0 else " "