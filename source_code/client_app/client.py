import sys
from PyQt5 import QtWidgets

from UI.UI import ErrorWindow, ServerWindow
from Components.Scanner import scan_ports
from Components.DataCollector import get_user_input

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
