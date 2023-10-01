import socket

def scan_ports(target_ip, start_port, end_port, secret_key):
    open_ports = []

    for port in range(start_port, end_port + 1):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)

        try:
            client_socket.connect((target_ip, port))

            client_socket.send(secret_key.encode())
            auth_response = client_socket.recv(1024).decode()

            if auth_response == "Authentication successful":
                open_ports.append(port)
            else:
                print(f"Authentication failed for port {port}")

            client_socket.close()
        except (ConnectionRefusedError, TimeoutError):
            pass

    return open_ports
