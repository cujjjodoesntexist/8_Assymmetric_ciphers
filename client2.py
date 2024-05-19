import socket

HOST = '127.0.0.1'
PORT_KEY_EXCHANGE = 8080

def get_server_port():
    # Создаем сокет для обмена ключами
    key_exchange_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key_exchange_sock.connect((HOST, PORT_KEY_EXCHANGE))

    # Получаем порт для основного общения
    server_port = int(key_exchange_sock.recv(1024).decode())

    # Закрываем соединение для обмена ключами
    key_exchange_sock.close()

    return server_port

if __name__ == "__main__":
    server_port = get_server_port()

    # Теперь можно использовать server_port для основного общения с сервером
    print(f"Received server port for communication: {server_port}")