# src/main.py

"""
Start the app from this file.
"""

import sys

from PyQt5.QtWidgets import QApplication
from gui.gui import MainWindow

def main():
    """
    The main function that initializes and runs the SnapTranslate application.
    """

    # Create an instance of the QApplication. This is necessary for any PyQt application.
    app = QApplication(sys.argv)
    # Create an instance of the main window of the application.
    main_window = MainWindow()
    # Show the main window to the user.
    main_window.show()
    # Start the PyQt event loop. This will keep the application running until it is closed.
    # sys.exit(app.exec_()) ensures a clean exit and returns the application's exit code.
    sys.exit(app.exec_())

if __name__ == '__main__':
    """
    This block ensures that the main function is called only when this script
    is executed directly (not when it's imported as a module).
    """
    
    main()