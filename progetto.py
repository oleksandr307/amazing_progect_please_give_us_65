import tkinter as tk
from tkinter import messagebox
import random

class Ship:
    def __init__(self, size):
        self.size = size
        self.hits = 0
        self.coordinates = []
        self.orientation = 0

    def is_sunk(self):
        return self.hits == self.size

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

class BattleshipGame:
    def __init__(self, master):
        self.master = master
        self.master.game = self

        self.player_board = Board(master, x=2, y=0, title=" Ваше поле", is_player=True, game=self)
        tk.Frame(master, width=50, bg='gray').grid(row=0, column=10, rowspan=15)
        self.computer_board = Board(master, x=2, y=11, title="Поле комп'ютера", game=self)

        self.current_turn = 'player'
        self.game_started = False
        self.last_computer_hit = None

        self.status_label = tk.Label(master, text="Розмістіть ваші кораблі!", font=('Arial', 14, 'bold'))
        self.status_label.grid(row=0, column=0, columnspan=21, pady=10)

        self.ships_to_place = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.current_ship = None
        self.placement_orientation = 0
        self.create_controls()
        self.setup_computer_ships()

    def create_controls(self):
        control_frame = tk.Frame(self.master)
        control_frame.grid(row=13, column=0, columnspan=21, pady=10)

        self.ship_listbox = tk.Listbox(control_frame, height=5, width=20, font=('Arial', 10))
        for size in self.ships_to_place:
            self.ship_listbox.insert(tk.END, f"{size}-палубний")
        self.ship_listbox.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text=" Вибрати корабель", command=self.select_ship, bg='lightgreen').pack(
            side=tk.LEFT, padx=5)
        tk.Button(control_frame, text=" Змінити орієнтацію", command=self.toggle_orientation, bg='lightblue').pack(
            side=tk.LEFT, padx=5)
        tk.Button(control_frame, text=" Почати гру!", command=self.start_game, bg='orange').pack(side=tk.LEFT, padx=5)

        self.selected_label = tk.Label(control_frame, text="Обрано: ---", font=('Arial', 10))
        self.selected_label.pack(side=tk.LEFT, padx=10)

    def select_ship(self):
        if not self.game_started:
            selection = self.ship_listbox.curselection()
            if selection:
                size = self.ships_to_place[selection[0]]
                self.current_ship = Ship(size)
                self.selected_label.config(text=f"Обрано:  {size}-палубний")
                self.status_label.config(text="Клікніть на своєму полі для розміщення")

    def toggle_orientation(self):
        self.placement_orientation = 1 - self.placement_orientation
        orient = "ВЕРТИКАЛЬНО ⬇" if self.placement_orientation else "ГОРИЗОНТАЛЬНО ➡"
        self.status_label.config(text=f"Орієнтація: {orient}")

    def start_placement(self, row, col):
        if self.current_ship and not self.game_started:
            if self.player_board.place_ship(self.current_ship, row, col, self.placement_orientation):
                self.ships_to_place.remove(self.current_ship.size)
                self.ship_listbox.delete(0)
                self.current_ship = None
                self.selected_label.config(text="Обрано: ---")
                if not self.ships_to_place:
                    self.status_label.config(text=" Усі кораблі розміщено! Натисніть 'Почати гру'!")
            else:
                messagebox.showerror("Помилка", " Неможливо розмістити корабель тут!")

    def start_game(self):
        if not self.ships_to_place:
            self.game_started = True
            self.status_label.config(text="⚔ Гра розпочата! Ваш хід!", fg='darkgreen')
            for row in range(10):
                for col in range(10):
                    btn = self.computer_board.buttons[row][col]
                    btn.config(state='normal', command=lambda r=row, c=col: self.handle_attack(r, c))
        else:
            messagebox.showwarning("Увага", "❗ Спочатку розмістіть усі кораблі!")

    def setup_computer_ships(self):
        ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for size in ship_sizes:
            placed = False
            while not placed:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                orientation = random.choice([0, 1])
                ship = Ship(size)
                placed = self.computer_board.place_ship(ship, row, col, orientation)
        self.computer_board.refresh_board()

    def handle_attack(self, row, col):
        if self.game_started and self.current_turn == 'player':
            cell = self.computer_board.grid[row][col]
            if not cell['hit']:
                cell['hit'] = True
                if cell['ship']:
                    cell['ship'].hits += 1
                    self.status_label.config(text=" ВЛУЧАННЯ! Стріляйте ще!", fg='red')
                    self.check_ship_sunk(cell['ship'], is_computer_ship=True)
                else:
                    self.current_turn = 'computer'
                    self.status_label.config(text=" Промах! Хід комп'ютера...", fg='blue')
                    self.master.after(1000, self.computer_turn)
                self.computer_board.update_cell(row, col)
                self.check_game_over()

    def computer_turn(self):
        available = [(r, c) for r in range(10) for c in range(10)
                     if not self.player_board.grid[r][c]['hit']]
        if not available:
            self.check_game_over()
            return

        target = self.find_target_around_hit() if self.last_computer_hit else None
        if not target:
            target = random.choice(available)

        row, col = target
        cell = self.player_board.grid[row][col]
        if not cell['hit']:
            cell['hit'] = True
            if cell['ship']:
                cell['ship'].hits += 1
                self.last_computer_hit = (row, col)
                self.check_ship_sunk(cell['ship'])
                self.computer_turn()
            else:
                self.current_turn = 'player'
                self.status_label.config(text="🎮 Ваш хід!", fg='darkgreen')
            self.player_board.update_cell(row, col)
            self.check_game_over()

    def find_target_around_hit(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr = self.last_computer_hit[0] + dr
            nc = self.last_computer_hit[1] + dc
            if 0 <= nr < 10 and 0 <= nc < 10:
                if not self.player_board.grid[nr][nc]['hit']:
                    return (nr, nc)
        return None

    def check_ship_sunk(self, ship, is_computer_ship=False):
        if ship.is_sunk():
            target_board = self.computer_board if is_computer_ship else self.player_board
            for (r, c) in ship.coordinates:
                self.mark_around_sunk(r, c, target_board)
            target_board.refresh_board()

    def mark_around_sunk(self, row, col, board):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < 10 and 0 <= nc < 10:
                    if not board.grid[nr][nc]['hit']:
                        board.grid[nr][nc]['hit'] = True
                        board.update_cell(nr, nc)

    def check_game_over(self):
        if all(cell['hit'] for row in self.player_board.grid for cell in row):
            messagebox.showinfo("Гра завершена!", "Всі клітинки обстріляні!")
            self.master.quit()
            return

        if all(ship.is_sunk() for ship in self.computer_board.ships):
            messagebox.showinfo("Перемога!", " Ви знищили всі кораблі противника!")
            self.master.quit()
        elif all(ship.is_sunk() for ship in self.player_board.ships):
            messagebox.showinfo("Поразка!", " Комп'ютер знищив ваші кораблі!")
            self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Морський бій")
    game = BattleshipGame(root)
    root.mainloop()