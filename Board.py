from Cell import Cell
import random 

class Board:
    def __init__(self, size_x = 6, size_y = 6, mines=6):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = [[Cell() for _ in range(size_y)] for _ in range(size_x)]
        self.mines = mines
        self.visited_dp = set()    # esto es para evitar repetir expansión
        self.place_mines()          # pone las minas altiro
        self.compute_adjacent_counts()  

    def valid(self, x: int, y: int) -> bool:
        """
        Entrega True si la ubicacion es valida en el tablero, caso contrario False
        """
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def place_mines(self) -> None:
        """
        Coloca las bombas en enl tablero aleatoriamente
        """
        all_positions = [(x, y) for x in range(self.size_x) for y in range(self.size_y)]
        mine_positions = random.sample(all_positions, self.mines)
        for x, y in mine_positions:
            self.grid[x][y].is_mine = True


    def compute_adjacent_counts(self) -> None:
        """
        Calcula para todas las celdas del tablero la cantidad de bombas adjacentes
        """
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.grid[x][y].is_mine:
                    self.grid[x][y].adjacent_mines = -1
                    continue
                count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if self.valid(nx, ny) and self.grid[nx][ny].is_mine:
                            count += 1
                self.grid[x][y].adjacent_mines = count

    def reveal_cell(self, x:int, y:int) -> bool:
        """
        Revela la celda, y en caso de que no haya minas cerca expande, y entrega False si revela una mina, caso contrario True
        """
        
        if not self.valid(x, y):     # chequea la coordenada
            print("Coordenada inválida.")
            return True

        cell = self.grid[x][y]

        if cell.is_flagged: 
            return True

        if cell.is_revealed:
            return True

        cell.is_revealed = True

        if cell.is_mine:
            return False

        if cell.adjacent_mines == 0: # si hace falta expanda la revelacion
            self.flood_fill(x, y)

        return True

    def flood_fill(self, x: int, y: int) -> None:
        """
        Expande de manera recursiva la expancion de las celdas
        """
        if (x, y) in self.visited_dp:   # si ya la visito se detiene para no repetir
            return
        self.visited_dp.add((x, y))     # se añade la ubicacion al Set donde se a expandido

        for dx in [-1, 0, 1]:   
            for dy in [-1, 0, 1]:   
                nx, ny = x + dx, y + dy # revisa las celdas adyacentes
                if not self.valid(nx, ny):
                    continue
                neighbor = self.grid[nx][ny]
                if not neighbor.is_revealed and not neighbor.is_mine and not neighbor.is_flagged:   # si la celda es segura revela la celda
                    neighbor.is_revealed = True
                    if neighbor.adjacent_mines == 0:    # si no tiene bombas adyacentes repite 
                        self.flood_fill(nx, ny)  # expansión recursiva

    def print_board(self, show_mines=False) -> None:
        """
        Muestra en terminal el estado del tablero actual
        """
        print("  y " + " ".join(str(i) for i in range(self.size_y)))
        print("x  " + "--" * self.size_x)


        for i in range(self.size_x):
            row = []
            space_x = ""
            if i < 10:
                space_x = " "       # No piesno generalizar esto
            for j in range(self.size_y):
                c = self.grid[i][j]
                if show_mines and c.is_mine:
                    row.append("*")
                else:
                    row.append(str(c))
            print(f"{i}" + space_x +  "| " + " ".join(row))
