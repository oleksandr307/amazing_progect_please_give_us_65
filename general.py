class GeneralAbilities:
    warrior_ready = False
    def sacrifice(game: BattleshipGame):
        if game.demon_sacrifices_left <= 0:
            messagebox.showwarning("Піддані більше не хочуть помирати:(")
            return False
        own_ships = [s for s in game.player_board.ships if not s.is_sunk()]
        ship = random.choice(own_ships)
        n = ship.size
        for (r, c) in ship.coordinates:
            cell = game.player_board.grid[r][c]
            cell['hit'] = True
            cell['ship'].hits = ship.size
        for (r, c) in ship.coordinates:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < game.player_board.size and 0 <= nc < game.player_board.size:
                        game.player_board.grid[nr][nc]['hit'] = True
        game.player_board.refresh_board()
        game.demon_sacrifices_left -= 1
        shots = 4 * n
        enemy = game.computer_board
        available = [(r, c) for r in range(10) for c in range(10) if not enemy.grid[r][c]['hit']]
        chosen = random.sample(available, min(shots, len(available)))
        for (r, c) in chosen:
            enemy.grid[r][c]['hit'] = True
            if enemy.grid[r][c]['ship']:
                enemy.grid[r][c]['ship'].hits += 1
            enemy.update_cell(r, c)

        for ship in list(enemy.ships):
            if ship.is_sunk():
                game.check_ship_sunk(ship, is_computer_ship=True)

        game.status_label.config(
            text=f"Жертва!Ви зробили{len(chosen)} пострілів по випадкових клітинках. Ваш хід",
            fg='purple'
        )
        return True
    def pirates_revenge(self):
        if random.random() >= 0.5:
            return
        self.status_label.config(text="БАБАХ! Помста піратів спрацювала!", fg='orange')
        rr, cc = random.choice([
                    (r0,c0) for r0 in range(10) for c0 in range(10)
                if not self.computer_board.grid[r0][c0]['hit']
                ])
        cell2 = self.computer_board.grid[rr][cc]
        cell2['hit'] = True
        if cell2['ship']:
                    cell2['ship'].hits += 1
                    self.check_ship_sunk(cell2['ship'], is_computer_ship=True)
        self.computer_board.update_cell(rr, cc)
        self.status_label.after(2000, lambda: self.status_label.config(text="", fg='black'))
    def warrior_blust(self,r,c):
        targets = [(r, c)]
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < 10 and 0 <= cc < 10:
                targets.append((rr, cc))

        for rr, cc in targets:
            cell = self.computer_board.grid[rr][cc]
            if not cell['hit']:
                cell['hit'] = True
                if cell['ship']:
                    cell['ship'].hits += 1
                    self.check_ship_sunk(cell['ship'], is_computer_ship=True)
                self.computer_board.update_cell(rr, cc)

        self.status_label.config(text="ПОТУЖНИЙ ПОСТРІЛ ЗА ІМПЕРАТОРА!!!", fg='darkred')
        GeneralAbilities.warrior_ready = False
        return  