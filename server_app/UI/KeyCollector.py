import sys
from PyQt5 import QtWidgets

def get_secret_key():
    secret_key, ok = QtWidgets.QInputDialog.getText(None, 'Secret Key', 'Enter Secret Key:')
    if ok:
        return secret_key
    else:
        sys.exit()