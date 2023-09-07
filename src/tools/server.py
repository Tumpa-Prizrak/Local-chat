import socket
import threading
from src import config


def handle_client(connection, address):
    print("Установлено соединение с клиентом:", address)

    while True:
        try:
            data = connection.recv(1024).decode()
            if not data:
                break
            print("Получено сообщение от клиента", address, ":", data)
            connection.send(data.encode())
        except:
            break

    print("Соединение с клиентом", address, "закрыто.")
    connection.close()

# Основная функция сервера
def main():
    # Ввод IP-адреса и порта для прослушивания
    ip = "0.0.0.0"
    port = config.PORT

    # Создание сокета сервера
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print("Сервер запущен и прослушивает", ip, ":", port)

    while True:
        # Принятие входящего соединения от клиента
        connection, address = server_socket.accept()

        # Запуск потока для обработки клиента
        threading.Thread(target=handle_client, args=(connection, address)).start()


if __name__ == '__main__':
    main()