import socket
from Components.Authenticator import authenticate_client

def start_windows_server(window, initial_port, secret_key):
    while True:
        try:
            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind(('localhost', initial_port))
                server_socket.listen(5)
                window.text_edit.append(f"Server listening on:{initial_port}")

                while True:
                    client_socket, client_address = server_socket.accept()
                    authenticated = authenticate_client(client_socket, secret_key)
                    if not authenticated:
                        client_socket.close()
                        continue

                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break

                        received_data = data.decode()
                        window.text_edit.append(received_data)

                        client_socket.send(data)

                    client_socket.close()
            except OSError as e:
                if e.errno == 98:
                    initial_port += 1
                else:
                    raise
            finally:
                server_socket.close()
        except:
            initial_port += 1