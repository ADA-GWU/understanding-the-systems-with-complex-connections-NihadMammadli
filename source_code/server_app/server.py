import sys
import platform
import threading
from PyQt5 import QtWidgets

from UI.KeyCollector import get_secret_key
from UI.ServerWindow import ServerWindow
from Components.Runner import start_server
from Components.Runner_Windows import start_windows_server

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ServerWindow()
    window.show()

    secret_key = get_secret_key()
    initial_port = 7777

    if platform.system() == "Windows":
        server_thread = threading.Thread(target=start_windows_server, args=(window, initial_port, secret_key))
        server_thread.daemon = True  
        server_thread.start()

    else: 
        server_thread = threading.Thread(target=start_server, args=(window, initial_port, secret_key))
        server_thread.daemon = True  
        server_thread.start()
        
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()