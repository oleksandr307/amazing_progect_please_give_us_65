class Board:
    def __init__(self, master, x, y, title, is_player=False, game=None):
        self.master = master
        self.game = game
        self.is_player = is_player
        self.size = 10
        self.grid = [[{'ship': None, 'hit': False} for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []
        self.buttons = []

        tk.Label(master, text=title, font=('Arial', 12, 'bold')).grid(row=x - 1, column=y, columnspan=10)

        for row in range(self.size):
            row_buttons = []
            for col in range(self.size):
                btn = tk.Button(master, width=3, height=1, relief='solid', bg='lightblue')
                if is_player:
                    btn.config(command=lambda r=row, c=col: self.on_click(r, c))
                else:
                    btn.config(state='disabled')
                btn.grid(row=row + x, column=col + y, padx=1, pady=1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def on_click(self, row, col):
        if self.game and not self.game.game_started:
            self.game.start_placement(row, col)

    def update_cell(self, row, col):
        cell = self.grid[row][col]
        if cell['hit']:
            if cell['ship']:
                color = 'darkred' if cell['ship'].is_sunk() else 'red'
            else:
                color = 'white'
        else:
            color = 'gray' if cell['ship'] and self.is_player else 'lightblue'

        self.buttons[row][col].config(
            bg=color,
            state='disabled' if cell['hit'] else 'normal'
        )

    def place_ship(self, ship, row, col, orientation):
        if self.is_valid_placement(ship, row, col, orientation):
            coordinates = []
            for i in range(ship.size):
                r = row + (i if orientation else 0)
                c = col + (i if not orientation else 0)
                self.grid[r][c]['ship'] = ship
                coordinates.append((r, c))
            ship.coordinates = coordinates
            self.ships.append(ship)
            self.refresh_board()
            return True
        return False

    def is_valid_placement(self, ship, row, col, orientation):
        for i in range(ship.size):
            r = row + (i if orientation else 0)
            c = col + (i if not orientation else 0)
            if r >= self.size or c >= self.size:
                return False
            if self.grid[r][c]['ship'] is not None:
                return False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if self.grid[nr][nc]['ship'] is not None:
                            return False
        return True

    def refresh_board(self):
        for row in range(self.size):
            for col in range(self.size):
                self.update_cell(row, col)
