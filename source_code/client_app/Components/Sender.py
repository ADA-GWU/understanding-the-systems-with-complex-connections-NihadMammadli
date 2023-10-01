import socket

def send_input_to_socket(target_ip, target_port, input_data, secret_key):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((target_ip, target_port))

        client_socket.send(secret_key.encode())
        auth_response = client_socket.recv(1024).decode()

        if auth_response == "Authentication successful":
            try:
                input_int = int(input_data)
                result = input_int * 2
                client_socket.send(str(result).encode())

                response_data = client_socket.recv(1024).decode()
                return response_data
            except ValueError:
                print("Invalid input data. Please enter an integer.")
        else:
            print("Authentication failed")

        client_socket.close()

    except (ConnectionRefusedError, TimeoutError):
        print(f"Failed to connect to port {target_port} or the server is not responding")

    return None
