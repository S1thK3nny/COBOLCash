# pylint: disable=no-name-in-module

import sys
from GUI import BankingAdminGUI
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BankingAdminGUI()
    window.show()
    sys.exit(app.exec())
