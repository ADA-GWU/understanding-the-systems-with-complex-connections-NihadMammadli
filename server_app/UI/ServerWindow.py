from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget

class ServerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Socket Server')

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        self.central_widget.setLayout(self.layout)