def authenticate_client(client_socket, secret_key):
    try:
        auth_message = client_socket.recv(1024).decode()
        if auth_message == secret_key:
            client_socket.send("Authentication successful".encode())
            return True
        else:
            client_socket.send("Authentication failed".encode())
            return False
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return False