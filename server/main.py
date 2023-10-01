import socket
import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit

class ServerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Socket Server')

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.setCentralWidget(self.text_edit)

def start_server(window, initial_port):
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('localhost', initial_port))
            server_socket.listen(5)
            window.text_edit.append(f"Server listening on:{initial_port}")

            while True:
                client_socket, client_address = server_socket.accept()
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

def main():
    app = QApplication(sys.argv)
    window = ServerWindow()
    window.show()

    initial_port = 7777

    server_thread = threading.Thread(target=start_server, args=(window, initial_port))
    server_thread.daemon = True  
    server_thread.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
