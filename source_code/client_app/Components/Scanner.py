import socket
import platform

def scan_ports(target_ip, start_port, end_port, secret_key):
    open_ports = []

    if start_port == 0:
        start_port = 1
        
    for port in range(start_port, end_port + 1):
        if platform.system() == "Windows":
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(0.001)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
        else:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(0.1)

        try:
            client_socket.connect((target_ip, port))

            client_socket.send(secret_key.encode())
            auth_response = client_socket.recv(1024).decode()

            if auth_response == "Authentication successful":
                open_ports.append(port)
            else:
                print(f"Authentication failed for port {port}")

            client_socket.close()
        except ConnectionRefusedError:
            print(f"Connection to port {port} was refused.")
        except TimeoutError:
            print(f"Connection to port {port} timed out.")
        except Exception as e:
            print(f"An error occurred on port {port}: {str(e)}")

    return open_ports
