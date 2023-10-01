import sys
from PyQt5.QtWidgets import QInputDialog

def get_secret_key():
    secret_key, ok = QInputDialog.getText(None, 'Secret Key', 'Enter Secret Key:')
    if ok:
        return secret_key
    else:
        sys.exit()