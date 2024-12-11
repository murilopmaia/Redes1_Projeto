class Connect4:
    def __init__(self):
        self.rows = 6  # Número de linhas
        self.cols = 7  # Número de colunas
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]  # Tabuleiro vazio

    def display_board(self):
        """Exibe o tabuleiro para os jogadores."""
        display = "\n"
        for row in self.board:
            display += " | ".join(row) + "\n"
            display += "-" * (4 * self.cols - 1) + "\n"
        display += "0   1   2   3   4   5   6\n"
        return display

    def make_move(self, player, col):
        """Faz a jogada na coluna escolhida pelo jogador."""
        if col < 0 or col >= self.cols:
            return False

        for row in range(self.rows - 1, -1, -1):  # Começa de baixo para cima
            if self.board[row][col] == ' ':
                self.board[row][col] = player
                return True
        return False

    def check_winner(self):
        """Verifica se há um vencedor."""
        # Verificar horizontal
        for row in self.board:
            for i in range(self.cols - 3):
                if row[i] != ' ' and all(row[i] == row[i + j] for j in range(4)):
                    return row[i]

        # Verificar vertical
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if self.board[row][col] != ' ' and all(self.board[row + j][col] == self.board[row][col] for j in range(4)):
                    return self.board[row][col]

        # Verificar diagonal principal
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if self.board[row][col] != ' ' and all(self.board[row + j][col + j] == self.board[row][col] for j in range(4)):
                    return self.board[row][col]

        # Verificar diagonal secundária
        for row in range(self.rows - 3):
            for col in range(3, self.cols):
                if self.board[row][col] != ' ' and all(self.board[row + j][col - j] == self.board[row][col] for j in range(4)):
                    return self.board[row][col]

        return None

    def is_full(self):
        """Verifica se o tabuleiro está cheio."""
        return all(self.board[row][col] != ' ' for row in range(self.rows) for col in range(self.cols))