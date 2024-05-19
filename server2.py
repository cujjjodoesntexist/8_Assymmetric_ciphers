import socket
import rsa

HOST = '127.0.0.1'
PORT_KEY_EXCHANGE = 8080
PORTS_POOL = [8081, 8082, 8083]  # Пул портов для основного общения

def get_available_port():
    for port in PORTS_POOL:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((HOST, port))
            sock.close()
            return port
        except OSError:
            pass
    return None

def handle_client(client_sock, private_key, client_public_key):
    # Принимаем и дешифруем сообщение от клиента
    encrypted_message = client_sock.recv(1024)
    decrypted_message = rsa.decrypt(encrypted_message, private_key).decode()
    print("Received message:", decrypted_message)

    # Отправляем ответ клиенту
    response = "Hello, client!"
    encrypted_response = rsa.encrypt(response.encode(), client_public_key)
    client_sock.send(encrypted_response)

if __name__ == "__main__":
    server_public_key, private_key = rsa.newkeys(1024)
    client_public_key = None  # Здесь должен быть публичный ключ клиента

    # Получаем доступный порт из пула для основного общения
    server_port = get_available_port()
    if server_port is None:
        print("Нет доступных портов для основного общения.")
        exit()

    # Начинаем слушать соединения на выбранном порту для обмена ключами
    with socket.socket() as key_exchange_sock:
        key_exchange_sock.bind((HOST, PORT_KEY_EXCHANGE))
        key_exchange_sock.listen(1)
        print(f"Сервер запущен на порту обмена ключами {PORT_KEY_EXCHANGE}.")

        # Ожидаем подключения клиента для обмена ключами
        client_sock, client_addr = key_exchange_sock.accept()
        print(f"Установлено соединение для обмена ключами с клиентом {client_addr}.")

        # Отправляем порт для основного общения
        client_sock.send(str(server_port).encode())

        # Закрываем соединение для обмена ключами
        client_sock.close()

    # Начинаем слушать соединения на выбранном порту для основного общения
    with socket.socket() as server_sock:
        server_sock.bind((HOST, server_port))
        server_sock.listen(1)
        print(f"Сервер запущен на порту основного общения {server_port}.")

        # Ожидаем подключения клиента для основного общения
        client_sock, client_addr = server_sock.accept()
        print(f"Установлено соединение для основного общения с клиентом {client_addr}.")

        # Обрабатываем сообщения от клиента
        handle_client(client_sock, private_key, client_public_key)

        # Закрываем соединение для основного общения
        client_sock.close()