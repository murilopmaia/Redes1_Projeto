import socket
import threading
from connect_4 import Connect4  

class GameServer:
    def __init__(self):
        self.players = []  # Lista para armazenar as conexões dos jogadores
        self.game = Connect4()  # Instância do jogo 
        self.lock = threading.Lock()  # Controle de acesso entre threads
        self.turn = 0  # Indica de quem é a vez

    def add_player(self, conn, addr):
        """Adiciona um jogador à lista."""
        with self.lock:
            self.players.append({'conn': conn, 'addr': addr, 'symbol': 'X' if len(self.players) == 0 else 'O'})
            return len(self.players) - 1


    def handle_player(self, player_id):
        """Gerencia as jogadas de um jogador."""
        conn = self.players[player_id]['conn']
        addr = self.players[player_id]['addr']
        symbol = self.players[player_id]['symbol']
        conn.sendall(f"Bem-vindo! Você é o jogador {symbol}\n".encode('utf-8'))

        while True:
            with self.lock:
                if len(self.players) < 2:
                    try:
                        conn.sendall("Aguardando o segundo jogador se conectar...\n".encode('utf-8'))
                    except ConnectionResetError:
                        print(f"Conexão com {addr} foi resetada.")
                        return
                    continue
                 
                if self.turn != player_id:
                    try:
                        conn.sendall("Aguarde sua vez...\n".encode('utf-8'))
                    except ConnectionResetError:
                        print(f"Conexão com {addr} foi resetada.")
                        return
                    continue
    
                conn.sendall(self.game.display_board().encode('utf-8'))
                conn.sendall(f"Sua vez! jogador {symbol}, Escolha uma posição (0-6): ".encode('utf-8'))

                try:
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        break
                    move = int(data.strip())
                    if self.game.make_move(symbol, move):
                        self.turn = 1 - self.turn
                        winner = self.game.check_winner()
                        if winner:
                            for player in self.players: # Enviando a mensagem para todos os jogadores
                                try:
                                    player['conn'].sendall(f"Fim de jogo! O vencedor é o jogador {winner}!\n".encode('utf-8'))
                                except ConnectionResetError:
                                    print(f"Conexão com {player['addr']} foi resetada.")
                                    return
                            break
                        elif self.game.is_full():
                            for player in self.players:
                                try:
                                    player['conn'].sendall("Empate! O tabuleiro está cheio.\n".encode('utf-8'))
                                except ConnectionResetError:
                                    print(f"Conexão com {player['addr']} foi resetada.")
                                    return
                            break
                    else:
                        conn.sendall("Movimento inválido! Tente novamente.\n".encode('utf-8'))
                except (ValueError, IndexError):
                    conn.sendall("Entrada inválida! Escolha um número entre 0 e 6.\n".encode('utf-8'))
                except ConnectionResetError:
                    print(f"Conexão com {addr} foi resetada.")
                    return
            
        conn.close()

def main():
    """Função principal para configurar e iniciar o servidor do jogo."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(2)
    print("Servidor Connect 4 iniciado na porta 8080")

    game_server = GameServer()

    while len(game_server.players) < 2:
        conn, addr = server.accept()
        player_id = game_server.add_player(conn, addr)
        threading.Thread(target=game_server.handle_player, args=(player_id,)).start()

    print("Dois jogadores conectados, iniciando o jogo!")

if __name__ == "__main__":
    main()
