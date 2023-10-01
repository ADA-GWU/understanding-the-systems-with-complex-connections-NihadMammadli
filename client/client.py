import socket
import random
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

SECRET_KEY = "Nihad"

def scan_ports(target_ip, start_port, end_port):
    open_ports = []

    for port in range(start_port, end_port + 1):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)

        try:
            client_socket.connect((target_ip, port))

            client_socket.send(SECRET_KEY.encode())
            auth_response = client_socket.recv(1024).decode()

            if auth_response == "Authentication successful":
                open_ports.append(port)
            else:
                print(f"Authentication failed for port {port}")
            
            client_socket.close()
        except (ConnectionRefusedError, TimeoutError):
            pass

    return open_ports


def send_input_to_socket(target_ip, target_port, input_data):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((target_ip, target_port))

        client_socket.send(SECRET_KEY.encode())
        auth_response = client_socket.recv(1024).decode()

        if auth_response == "Authentication successful":
            try:
                input_int = int(input_data)
                result = str(input_int * 2)
                client_socket.send(result.encode())

                response_data = client_socket.recv(1024).decode()
                print("Server response:", response_data)
            except ValueError:
                print("Invalid input data. Please enter an integer.")
        else:
            print("Authentication failed")
        
        client_socket.close()
        
    except (ConnectionRefusedError, TimeoutError):
        print(f"Failed to connect to port {target_port} or the server is not responding")



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

        self.input_field = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.input_field)

        self.enter_button = QtWidgets.QPushButton('Enter', self)
        self.enter_button.clicked.connect(self.handle_enter_button)
        self.layout.addWidget(self.enter_button)

        self.central_widget.setLayout(self.layout)

    def handle_enter_button(self):
        input_data = self.input_field.text()
        self.input_field.clear()

        if input_data.lower() == 'exit':
            self.close()
        else:
            target_port = random.choice(open_ports)
            send_input_to_socket(target_ip, target_port, input_data)

class ErrorWindow(QtWidgets.QMainWindow):
    def __init__(self, message):
        super().__init__()

        self.initUI(message)

    def initUI(self, message):
        self.setGeometry(200, 200, 400, 200)
        self.setWindowTitle('Error')

        self.message_label = QtWidgets.QLabel(message, self)
        
        font = QtGui.QFont()
        font.setPointSize(32)
        self.message_label.setFont(font)
        
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.message_label)
        self.central_widget.setLayout(self.layout)
        
def get_user_input():
    global target_ip, start_port, end_port
    target_ip, ok = QtWidgets.QInputDialog.getText(None, 'Target IP Address', 'Enter Target IP Address (or "localhost"):')
    if not ok:
        sys.exit()

    if target_ip.lower() == 'localhost':
        target_ip = '127.0.0.1'

    start_port, ok = QtWidgets.QInputDialog.getInt(None, 'Start Port', 'Enter Start Port:')
    if not ok:
        sys.exit()
    
    end_port, ok = QtWidgets.QInputDialog.getInt(None, 'End Port', 'Enter End Port:')
    if not ok:
        sys.exit()

def main():
    global open_ports, target_ip, start_port, end_port

    app = QtWidgets.QApplication(sys.argv)
    
    get_user_input()  

    open_ports = scan_ports(target_ip, start_port, end_port)

    if open_ports:
        print(f"Open ports on {target_ip}:")
        for port in open_ports:
            print(f"{port} is open")

        window = ServerWindow()
        window.text_edit.append(f"Open ports on {target_ip}:\n" + "\n".join([f"{port} is open" for port in open_ports]))
        window.show()
        sys.exit(app.exec_())

    else:
        if target_ip:
            error_message = f"No open ports were found on {target_ip}"
        else: 
            error_message = f"Please enter ip!"

        error_window = ErrorWindow(error_message)
        error_window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
