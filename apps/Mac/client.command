#!/usr/bin/env python

import sys
import socket 
import platform
import random
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

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

class ServerWindow(QtWidgets.QMainWindow):
    def __init__(self, open_ports, target_ip, secret_key):
        super().__init__()

        self.open_ports = open_ports
        self.target_ip = target_ip
        self.secret_key = secret_key

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 500, 600)
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

        enter_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self)  
        enter_shortcut.activated.connect(self.handle_enter_button)

        self.central_widget.setLayout(self.layout)

    def handle_enter_button(self):
        input_data = self.input_field.text()
        self.input_field.clear()

        if input_data.lower() == 'exit':
            self.close()
        else:
            target_port = random.choice(self.open_ports)
            response = send_input_to_socket(self.target_ip, target_port, input_data, self.secret_key)

            if response is not None:
                response_text = f"Port {target_port}: {response}"
                self.text_edit.append(response_text)
                print(response_text)

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

def get_user_input():
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

    secret_key, ok = QtWidgets.QInputDialog.getText(None, 'Secret Key', 'Enter Secret Key:')
    if not ok:
        sys.exit()

    return target_ip, start_port, end_port, secret_key


def main():
    app = QtWidgets.QApplication(sys.argv)

    target_ip, start_port, end_port, secret_key = get_user_input()

    open_ports = scan_ports(target_ip, start_port, end_port, secret_key)

    if open_ports:
        print(f"Open ports on {target_ip}:")
        for port in open_ports:
            print(f"{port} is open")

        window = ServerWindow(open_ports, target_ip, secret_key)
        window.text_edit.append(f"Open ports on {target_ip}:\n" + "\n".join([f"{port} is open" for port in open_ports]))
        window.show()
        sys.exit(app.exec_())

    else:
        if target_ip:
            error_message = f"No open ports were found on {target_ip}"
        else:
            error_message = f"Please enter IP!"

        error_window = ErrorWindow(error_message)
        error_window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
