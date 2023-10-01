import sys
from PyQt5 import QtWidgets

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
