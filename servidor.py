import socket
import threading
from connect_4 import Connect4  
import time

class GameServer:
    def __init__(self):
        self.players = []  # Lista para armazenar as conexões dos jogadores
        self.game = Connect4()  # Instância do jogo 
        self.lock = threading.Lock()  # Controle de acesso entre threads
        self.turn = 0  # Indica de quem é a vez
        self.awaiting_message_sent = [False, False]  # Controle para "Aguarde sua vez"

    def clear_screen(self, conn):
        """Limpa o terminal do cliente usando escape sequences."""
        try:
            conn.sendall("\033[H\033[J".encode('utf-8'))
        except ConnectionResetError:
            pass

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

        try:
            while True:
                with self.lock:
                    if len(self.players) < 2:
                        if not self.awaiting_message_sent[player_id]:
                            conn.sendall("Aguardando o segundo jogador se conectar...\n".encode('utf-8'))
                            self.awaiting_message_sent[player_id] = True
                        continue

                    if self.turn != player_id:
                        if not self.awaiting_message_sent[player_id]:
                            self.clear_screen(conn)
                            conn.sendall(self.game.display_board().encode('utf-8'))
                            conn.sendall("Aguarde sua vez...\n".encode('utf-8'))
                            self.awaiting_message_sent[player_id] = True
                        continue

                    # É a vez do jogador
                    self.awaiting_message_sent[player_id] = False
                    self.clear_screen(conn)
                    conn.sendall(self.game.display_board().encode('utf-8'))
                    conn.sendall(f"Sua vez! jogador {symbol}, Escolha uma posição (0-6): ".encode('utf-8'))

                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        break
                    try:
                        move = int(data.strip())
                    except:
                        conn.sendall("Movimento inválido! Tente novamente.\n".encode('utf-8'))
                        time.sleep(3)
                        continue
                    
                    if self.game.make_move(symbol, move):
                        self.turn = 1 - self.turn
                        winner = self.game.check_winner()
                        if winner or self.game.is_full():
                            self.end_game(winner)
                            return
                    else:
                        conn.sendall("Movimento inválido! Tente novamente.\n".encode('utf-8'))
                        time.sleep(3)
        except ConnectionResetError:
            print(f"Conexão com {addr} foi resetada.")
            return
        finally:
            conn.close()
            return

    def end_game(self, winner):
        """Encerra o jogo e notifica todos os jogadores."""
        for player in self.players:
            try:
                self.clear_screen(player['conn'])
                player['conn'].sendall(self.game.display_board().encode('utf-8'))
                if winner:
                    player['conn'].sendall(f"Fim de jogo! O vencedor é o jogador {winner}!\n".encode('utf-8'))
                else:
                    player['conn'].sendall("Empate! O tabuleiro está cheio.\n".encode('utf-8'))
            except OSError:
                print(f"Erro ao enviar mensagem para o jogador {player['addr']}.")
            finally:
                player['conn'].close()
        print("Jogo encerrado. Conexões finalizadas.")

            
        

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