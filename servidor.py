import socket
import threading
from connect_4 import Connect4  

class GameServer:
    def __init__(self):
        self.players = []  # Lista para armazenar as conexões dos jogadores
        self.game = Connect4()  # Instância do jogo 
        self.lock = threading.Lock()  # Controle de acesso entre threads
        self.turn = 0  # Indica de quem é a vez
        self.wait = 0 # Para aparecer a mensagem de aguarde apenas uma vez

    def add_player(self, conn, addr):
        """Adiciona um jogador à lista."""
        with self.lock:
            self.players.append({'conn': conn, 'addr': addr, 'symbol': 'X' if len(self.players) == 0 else 'O'})
            return len(self.players) - 1

    def broadcast(self, message):
        """Envia uma mensagem para todos os jogadores."""
        for player in self.players:
            player['conn'].sendall(message.encode('utf-8'))

    def handle_player(self, player_id):
        """Gerencia as jogadas de um jogador."""
        conn = self.players[player_id]['conn']
        symbol = self.players[player_id]['symbol']
        conn.sendall(f"Bem-vindo! Você é o jogador {symbol}\n".encode('utf-8'))

        while True:
            with self.lock:
                if self.turn != player_id:
                    if self.wait == 0:
                        conn.sendall("Aguarde sua vez...\n".encode('utf-8'))
                        self.wait = 1 - self.wait
                    continue

                self.wait = 1 - self.wait
                conn.sendall(self.game.display_board().encode('utf-8'))
                conn.sendall(f"Sua vez! jogador {symbol} Escolha uma posição (0-6): ".encode('utf-8'))

                try:
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        break
                    move = int(data.strip())
                    if self.game.make_move(symbol, move):
                        self.turn = 1 - self.turn
                        winner = self.game.check_winner()
                        if winner:
                            conn.sendall(f"Fim de jogo! O vencedor é o jogador {winner}!\n")
                            break
                        elif self.game.is_full():
                            conn.sendall("Empate! O tabuleiro está cheio.\n")
                            break
                    else:
                        conn.sendall("Movimento inválido! Tente novamente.\n".encode('utf-8'))
                except (ValueError, IndexError):
                    conn.sendall("Entrada inválida! Escolha um número entre 0 e 6.\n".encode('utf-8'))

        conn.close()

def main():
    """Função principal para configurar e iniciar o servidor do jogo."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(2)
    print("Servidor Tic-Tac-Toe iniciado na porta 8080")

    game_server = GameServer()

    while len(game_server.players) < 2:
        conn, addr = server.accept()
        player_id = game_server.add_player(conn, addr)
        threading.Thread(target=game_server.handle_player, args=(player_id,)).start()

    print("Dois jogadores conectados, iniciando o jogo!")

if __name__ == "__main__":
    main()
