import socket

initial_port = 7777

while True:
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', initial_port))
        server_socket.listen(5)
        print(f"Server listening on localhost:{initial_port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"--------------------------------------")

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break  

                print(f"{data.decode()}")  

                client_socket.send(data)  

            client_socket.close()
    except OSError as e:
        if e.errno == 98:
            print(f"{initial_port} is taken")
            initial_port += 1
        else:
            raise

    server_socket.close()
