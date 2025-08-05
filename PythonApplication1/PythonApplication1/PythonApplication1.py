import random

class Minesweeper:
    def __init__(self, size=8, num_mines=10):
        self.size = size
        self.num_mines = num_mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.visible = [[False for _ in range(size)] for _ in range(size)]
        self.mines = set()
        self.generate_mines()

    def generate_mines(self):
        while len(self.mines) < self.num_mines:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            self.mines.add((row, col))

    def count_adjacent_mines(self, row, col):
        directions = [(-1,-1), (-1,0), (-1,1),
                      (0,-1),         (0,1),
                      (1,-1), (1,0), (1,1)]
        count = 0
        for dr, dc in directions:
            r, c = row+dr, col+dc
            if 0 <= r < self.size and 0 <= c < self.size:
                if (r, c) in self.mines:
                    count += 1
        return count

    def reveal(self, row, col):
        if self.visible[row][col]:
            return

        self.visible[row][col] = True

        if (row, col) in self.mines:
            self.board[row][col] = '*'
            return

        count = self.count_adjacent_mines(row, col)
        self.board[row][col] = str(count) if count > 0 else ' '

        if count == 0:
            # Auto reveal surrounding cells
            directions = [(-1,-1), (-1,0), (-1,1),
                          (0,-1),         (0,1),
                          (1,-1), (1,0), (1,1)]
            for dr, dc in directions:
                r, c = row+dr, col+dc
                if 0 <= r < self.size and 0 <= c < self.size:
                    self.reveal(r, c)

    def print_board(self, reveal_all=False):
        print("\n   " + ' '.join(str(i) for i in range(self.size)))
        print("  +" + '--' * self.size + '+')

        for i in range(self.size):
            row = []
            for j in range(self.size):
                if reveal_all or self.visible[i][j]:
                    row.append(self.board[i][j])
                else:
                    row.append('#')
            print(f"{i} |{' '.join(row)}|")
        print("  +" + '--' * self.size + '+')

    def play(self):
        print("=== Minesweeper ===")
        while True:
            self.print_board()
            try:
                move = input("Enter row and column (e.g. 3 4): ")
                if move.lower() in ['exit', 'quit']:
                    print("Game exited.")
                    break
                row, col = map(int, move.strip().split())
                if not (0 <= row < self.size and 0 <= col < self.size):
                    print("Invalid coordinates. Try again.")
                    continue

                if (row, col) in self.mines:
                    print("💥 You hit a mine! Game Over.")
                    self.reveal(row, col)
                    self.print_board(reveal_all=True)
                    break

                self.reveal(row, col)

                # Check win condition
                all_safe_revealed = all(
                    self.visible[r][c] or (r, c) in self.mines
                    for r in range(self.size)
                    for c in range(self.size)
                )
                if all_safe_revealed:
                    print("🎉 Congratulations! You cleared the minefield!")
                    self.print_board(reveal_all=True)
                    break
            except Exception as e:
                print("Invalid input. Please enter row and column numbers.")

if __name__ == "__main__":
    game = Minesweeper(size=8, num_mines=10)
    game.play()