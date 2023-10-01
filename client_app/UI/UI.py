import random

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from Components.Sender import send_input_to_socket

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
