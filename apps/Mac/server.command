import sys
import threading
from PyQt5 import QtWidgets
import socket

def start_server(window, initial_port, secret_key):
    while True:
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

        server_socket.close()

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
    
def get_secret_key():
    secret_key, ok = QtWidgets.QInputDialog.getText(None, 'Secret Key', 'Enter Secret Key:')
    if ok:
        return secret_key
    else:
        sys.exit()

class ServerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Socket Server')

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout()

        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        self.central_widget.setLayout(self.layout)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ServerWindow()
    window.show()

    secret_key = get_secret_key()
    initial_port = 7777

    server_thread = threading.Thread(target=start_server, args=(window, initial_port, secret_key))
    server_thread.daemon = True  
    server_thread.start()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()