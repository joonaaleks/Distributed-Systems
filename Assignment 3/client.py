import socket
import threading

HEADER_LENGTH = 10


def send_message(client_socket, message):
    message_length = f"{len(message):<{HEADER_LENGTH}}"
    message_to_send = message_length + message
    client_socket.sendall(bytes(message_to_send, "utf-8"))


def receive_message(client_socket):
    message_length = client_socket.recv(HEADER_LENGTH).decode("utf-8")
    if message_length:
        message = client_socket.recv(int(message_length)).decode("utf-8")
        return message


def receive_messages_update(client_socket, current_channel):
    while True:
        message = receive_message(client_socket)
        if message:
            if message.startswith("[") and message.endswith("]"):
                channel_name = message[1:-1]
                if channel_name != current_channel:
                    continue
            print(f"{message}")


def connect_to_server(IP, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    return client_socket


def set_username(client_socket):
    username = input("Set your nickname: ")
    send_message(client_socket, username)


def join_channel(channel, client_socket):
    send_message(client_socket, f"/join {channel}")


def leave_channel(client_socket):
    send_message(client_socket, "/leave")


def send_channel_message(message, channel, client_socket):
    send_message(client_socket, f"[{channel}] {message}")


def send_direct_message(message, client_socket):
    send_message(client_socket, message)


def messaging_loop(client_socket):
    current_channel = ""
    while True:
        message = input()
        if message.startswith("/join "):
            channel = message.split("/join ")[1]
            join_channel(channel, client_socket)
            current_channel = channel
        elif message == "/leave":
            leave_channel(client_socket)
            current_channel = ""
        else:
            if current_channel:
                send_channel_message(message, current_channel, client_socket)
            else:
                send_direct_message(message, client_socket)
        if message == "/quit":
            break


if __name__ == "__main__":
    IP = input("Enter IP address: ")
    PORT = 3000
    client_socket = connect_to_server(IP, PORT)
    set_username(client_socket)
    receiving_thread = threading.Thread(
        target=receive_messages_update, args=(client_socket, ""), daemon=True)
    receiving_thread.start()
    messaging_loop(client_socket)
    client_socket.close()
