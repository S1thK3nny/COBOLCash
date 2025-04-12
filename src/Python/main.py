"""
Main entry point for the Banking Admin GUI application.
This script initializes the GUI and compiles the COBOL program if necessary.
It also handles the command-line arguments and starts the application.
Usage:
    python main.py
"""

# pylint: disable=no-name-in-module

import sys
from GUI import BankingAdminGUI
from PyQt6.QtWidgets import QApplication
from COBOLInterface import COBOL_compile

if __name__ == "__main__":
    # Compile the COBOL program before running the GUI
    if not COBOL_compile():
        print("Failed to compile COBOL program. Exiting.")
        sys.exit(1)
    print("COBOL program compiled successfully.")

    # Initialize the GUI application
    app = QApplication(sys.argv)
    window = BankingAdminGUI()
    window.show()
    sys.exit(app.exec())
