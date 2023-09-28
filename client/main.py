import socket
import random

def scan_ports(target_ip, start_port, end_port):
    open_ports = []

    for port in range(start_port, end_port + 1):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1) 

        try:
            client_socket.connect((target_ip, port))
            open_ports.append(port)
            client_socket.close()
        except (ConnectionRefusedError, TimeoutError):
            pass

    return open_ports

def send_input_to_socket(target_ip, target_port, input_data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((target_ip, target_port))
        client_socket.send(input_data.encode())  
        client_socket.close()
    except (ConnectionRefusedError, TimeoutError):
        print(f"Failed to connect to port {target_port}")

def main():
    target_ip = '127.0.0.1'
    start_port = 7700
    end_port = 10000

    open_ports = scan_ports(target_ip, start_port, end_port)

    if open_ports:
        print(f"Open ports on {target_ip}:")
        for port in open_ports:
            print(f"{port} is open")

        while True:
            input_data = input("Enter number or enter 'exit' to quit ): ")
            if input_data.lower() == 'exit':
                break  

            target_port = random.choice(open_ports) 
            send_input_to_socket(target_ip, target_port, input_data)
    else:
        print(f"No open ports found on {target_ip}")

if __name__ == "__main__":
    main()
