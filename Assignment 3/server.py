import socket
import threading

# Constants
HEADER_LENGTH = 10
IP = 'localhost'
PORT = 3000

# Socket setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen()

# Global state
clients = {}
messages = []
client_channels = {}

# Functions


def close_connection(client_socket):
    print(f'{clients[client_socket]["username"]} has disconnected!')
    del clients[client_socket]
    del client_channels[client_socket]
    client_socket.close()


def send_message(socket, message):
    try:
        socket.send(bytes(f"{len(message):<{HEADER_LENGTH}}", "utf-8"))
        socket.send(bytes(message, "utf-8"))
    except:
        print(f'[ERROR] SENDING "{message}" to {clients[socket]["username"]}')


def receive_message(client_socket):
    message_length = client_socket.recv(HEADER_LENGTH).decode("utf-8")
    message = client_socket.recv(int(message_length)).decode("utf-8")
    return message


def send_to_all_clients(message, sender_socket):
    user_message = f'{clients[sender_socket]["username"]} > {message}'
    messages.append(user_message)
    print(user_message)
    for client_socket in clients:
        if client_socket != sender_socket and client_channels[client_socket] == client_channels[sender_socket]:
            send_message(client_socket, user_message)


def handle_client(client_socket, client_address):
    # Prompt for username
    username = receive_message(client_socket)
    clients[client_socket] = {'username': username, 'address': client_address}
    client_channels[client_socket] = ''

    print(f'{username} has connected to the chat room!')

    # Send welcome message to client and previous messages in server
    send_message(client_socket, f'{username} has joined the chat room!')
    send_message(client_socket, str(len(messages)))
    for i in range(len(messages)):
        send_message(client_socket, messages[i])

    # Receive and broadcast messages
    connected = True
    while connected:
        try:
            message = receive_message(client_socket)
            print(message)
            if message.startswith("/join "):
                channel = message.split("/join ")[1]
                client_channels[client_socket] = channel
                send_message(client_socket, f'Joined channel {channel}')
            elif message == "/leave":
                client_channels[client_socket] = ''
                send_message(client_socket, 'Left channel')
            elif message == "/quit":
                connected = False
            else:
                if client_channels[client_socket]:
                    send_to_all_clients(message, client_socket)
                else:
                    send_message(
                        client_socket, 'You are not currently in a channel')
        except:
            connected = False

    close_connection(client_socket)


# Main program loop
print('Chat room is now running!')
while True:
    client_socket, client_address = server_socket.accept()
    handling_thread = threading.Thread(target=handle_client, args=[
                                       client_socket, client_address])
    handling_thread.start()
