import socket

HOST = '192.168.0.21'  # IP do servidor
PORT = 8080

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Conectado ao servidor.\n")

        while True:
            data = s.recv(1024).decode('utf-8')
            print(data)

            if "Escolha uma posição" in data:
                inp = input()
                s.sendall(inp.encode('utf-8'))

            if "Fim" in data or "Empate" in data:
                break

if __name__ == "__main__":
    main()
