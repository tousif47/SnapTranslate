# src/gui/gui.py

"""
This module defines the graphical user interface (GUI) for the SnapTranslate application
using the PyQt5 framework. It includes widgets for screen capturing and displaying
translation results.
"""

import sys
import asyncio

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PIL import Image
from PyQt5.QtGui import QImage
from core import processing

class ScreenCaptureWidget(QWidget):
    """
    A widget that allows the user to capture a portion of the screen.
    """

    # Signal emitted when a screen area is captured, carrying the captured image as a QPixmap
    captured_image = pyqtSignal(QPixmap)

    def __init__(self):
        """
        Initializes the ScreenCaptureWidget.
        """

        super().__init__()

        self.begin, self.end = QPoint(), QPoint()  # Store the starting and ending points of the selection rectangle
        self.setCursor(Qt.CrossCursor)  # Set the cursor to a crosshair for selection
        self.setMouseTracking(True)  # Enable mouse tracking to update selection in real-time
        self.setAttribute(Qt.WA_TranslucentBackground) # Make the widget background transparent
        self.background_image = None # To store the initial screen capture

    def showFullScreen(self):
        """
        Shows the widget in full-screen mode and captures the initial screen.
        """

        screen = QApplication.primaryScreen()
        self.background_image = screen.grabWindow(0) # Capture the entire screen
        super().showFullScreen()

    def mousePressEvent(self, event):
        """
        Handles the mouse press event to start the selection rectangle.
        """

        if event.button() == Qt.LeftButton:
            self.begin = event.pos()  # Record the starting position of the selection
            self.end = self.begin    # Initialize the end position to the start
            self.update()           # Trigger a repaint to show the initial point

    def mouseMoveEvent(self, event):
        """
        Handles the mouse move event to update the selection rectangle.
        """

        if event.buttons() & Qt.LeftButton:  # Check if the left button is pressed while moving
            self.end = event.pos()  # Update the end position of the selection
            self.update()           # Trigger a repaint to show the updated rectangle

    def mouseReleaseEvent(self, event):
        """
        Handles the mouse release event to finalize the selection and emit the captured image.
        """

        if event.button() == Qt.LeftButton:
            rect = QRect(self.begin, self.end).normalized()  # Create a rectangle from the start and end points and normalize it

            if rect.width() > 0 and rect.height() > 0:  # Ensure the selected area has a valid size
                self.captured_image.emit(self.background_image.copy(rect)) # Copy the selected area from the initial screen capture and emit the signal

            self.close()  # Close the screen capture widget

    def paintEvent(self, event):
        """
        Paints the widget, drawing the background and the selection rectangle.
        """

        painter = QPainter(self)
        if self.background_image:
            painter.drawPixmap(self.rect(), self.background_image) # Draw the captured background image

        painter.setPen(QColor(100, 149, 237, 200)) # Set the pen color for the rectangle (Cornflower Blue with some transparency)
        painter.setBrush(QColor(100, 149, 237, 50))  # Set the brush color for the rectangle (Cornflower Blue with more transparency)

        if self.begin != self.end:
            rect = QRect(self.begin, self.end).normalized()  # Normalize the rectangle
            painter.drawRect(rect)  # Draw the selection rectangle

class MainWindow(QMainWindow):
    """
    The main window of the SnapTranslate application.
    """

    def __init__(self):
        """
        Initializes the main window.
        """

        super().__init__()

        self.setWindowTitle("SnapTranslate")  # Set the title of the main window
        self.setGeometry(100, 100, 100, 50)   # Set the initial position and size of the window (increased initial height)

        app_icon = QIcon("src/gui/app_icon.jpg")  # Load the application icon
        self.setWindowIcon(app_icon)  # Set the application icon
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint) # Disable the maximize button

        self.central_widget = QWidget()  # Create a central widget to hold the layout
        self.setCentralWidget(self.central_widget)  # Set the central widget of the main window

        self.main_layout = QVBoxLayout(self.central_widget)  # Create a vertical layout for the central widget

        # Horizontal layout for buttons
        self.buttons_layout = QHBoxLayout()

        self.new_button = QPushButton("+ New")  # Create the "New" button
        self.new_button.clicked.connect(self.start_screen_capture)  # Connect the button's clicked signal to the start_screen_capture method
        self.buttons_layout.addWidget(self.new_button)  # Add the "New" button to the buttons layout

        self.translate_russian_button = QPushButton("Translate Russian")  # Create the "Translate Russian" button
        self.translate_russian_button.clicked.connect(lambda: self.translate("ru")) # Connect the button's clicked signal to the translate method, passing the Russian language code ("ru")
        self.buttons_layout.addWidget(self.translate_russian_button)  # Add the "Translate Russian" button to the buttons layout

        self.translate_swedish_button = QPushButton("Translate Swedish")  # Create the "Translate Swedish" button
        self.translate_swedish_button.clicked.connect(lambda: self.translate("sv")) # Connect the button's clicked signal to the translate method, passing the Swedish language code ("sv")
        self.buttons_layout.addWidget(self.translate_swedish_button)  # Add the "Translate Swedish" button to the buttons layout

        self.main_layout.addLayout(self.buttons_layout)  # Add the buttons layout to the main layout

        self.dark_theme_enabled = True  # Flag to enable or disable dark theme       
        if self.dark_theme_enabled:
            self.apply_dark_theme()  # Apply the dark theme if enabled

        self.capture_widget = None  # Instance of the screen capture widget, initialized to None
        self.captured_image_data = None # Store the captured QPixmap
        self.captured_label = None  # Label to display the captured image
        self.translation_label = None # Label to display the translated text

        # Initialize asyncio event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def apply_dark_theme(self):
        """
        Applies a dark theme to the application.
        """

        dark_stylesheet = """
            QMainWindow
            {
                background-color: #363636;
            }
            QWidget
            {
                background-color: #363636;
                color: #f0f0f0;
            }
            QLabel
            {
                color: #f0f0f0;
            }
            QPushButton
            {
                background-color: #505050;
                color: #f0f0f0;
                border: 1px solid #606060;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover
            {
                background-color: #606060;
            }
        """

        self.setStyleSheet(dark_stylesheet)  # Set the stylesheet for the main window

    def start_screen_capture(self):
        """
        Initiates the screen capture process.
        """

        print("'+ New' button clicked. Starting screen capture.")

        self.showMinimized() # Minimize the main window
        QApplication.processEvents() # Ensure the window is minimized before capture

        self.capture_widget = ScreenCaptureWidget()  # Create an instance of the screen capture widget
        screen_geometry = QApplication.desktop().screenGeometry()  # Get the geometry of the primary screen
        self.capture_widget.setGeometry(screen_geometry)  # Set the geometry of the capture widget to cover the entire screen
        self.capture_widget.showFullScreen()  # Show the capture widget in full-screen mode
        self.capture_widget.captured_image.connect(self.store_captured_image) # Connect the captured_image signal of the capture widget to the store_captured_image method

    def store_captured_image(self, image):
        """
        Stores the captured image and displays a thumbnail in the main window.
        """

        print("Image captured!")
        self.captured_image_data = image  # Store the captured QPixmap

        if self.captured_label is None:
            self.captured_label = QLabel()  # Create a label to display the captured image if it doesn't exist
            self.main_layout.addWidget(self.captured_label)  # Add the label to the main layout

        self.captured_label.setPixmap(self.captured_image_data.scaledToWidth(300)) # Scale the captured image to a width of 300 and set it as the label's pixmap
        self.showNormal() # Restore the main window

    def translate(self, source_language):
        """
        Initiates the translation process for the captured image.
        """

        if self.captured_image_data is not None:
            pil_image = self.qpixmap_to_pil_image(self.captured_image_data) # Convert the captured QPixmap to a PIL Image

            async def translate_text():
                """
                An inner asynchronous function to perform the translation.
                """

                try:
                    translated_text = await processing.process_image_and_translate(pil_image, target_language='en', source_language=source_language) # Call the processing module to perform OCR and translation
                    self.display_translation(translated_text) # Display the translated text in the GUI

                except Exception as e:
                    error_message = f"An error occurred during translation: {str(e)}"
                    print(error_message)
                    self.display_translation(f"Translation Error: {error_message}") # Display a user-friendly error message

            asyncio.run(translate_text()) # Run the asynchronous translation function in the event loop
        else:
            self.display_translation("Please capture an image first.") # Display a message if no image has been captured

    def qpixmap_to_pil_image(self, pixmap):
        """
        Converts a PyQt QPixmap to a PIL Image.
        """

        qimage = pixmap.toImage() # Convert QPixmap to QImage
        temp_buffer = qimage.constBits().asstring(qimage.byteCount()) # Get the raw bytes of the QImage
        pil_image = Image.frombuffer("RGBA", (qimage.width(), qimage.height()), temp_buffer, "raw", "RGBA", 0, 1) # Create a PIL Image from the buffer

        return pil_image

    def display_translation(self, text):
        """
        Displays the translated text in the main window.
        """

        print(f"Translated text: '{text}'")

        if self.translation_label is None:
            self.translation_label = QLabel() # Create a label to display the translation if it doesn't exist
            self.main_layout.addWidget(self.translation_label) # Add the label to the main layout

        self.translation_label.setText(f"{text}") # Set the translated text to the label