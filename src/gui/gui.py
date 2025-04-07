# src/gui/gui.py
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget,
                             QVBoxLayout, QHBoxLayout, QFrame, QLabel)
from PyQt5.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PIL import Image
from PyQt5.QtGui import QImage
import asyncio
from src.core import processing

class ScreenCaptureWidget(QWidget):
    captured_image = pyqtSignal(QPixmap)

    def __init__(self):
        super().__init__()
        self.begin, self.end = QPoint(), QPoint()
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground) # Make the widget background transparent
        self.background_image = None # To store the initial screen capture

    def showFullScreen(self):
        screen = QApplication.primaryScreen()
        self.background_image = screen.grabWindow(0) # Capture the entire screen
        super().showFullScreen()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = self.begin
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            rect = QRect(self.begin, self.end).normalized()
            if rect.width() > 0 and rect.height() > 0:
                self.captured_image.emit(self.background_image.copy(rect)) # Copy from the background
            self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.background_image:
            painter.drawPixmap(self.rect(), self.background_image) # Draw the background

        painter.setPen(QColor(100, 149, 237, 200)) # Cornflower Blue with some transparency
        painter.setBrush(QColor(100, 149, 237, 50)) # Cornflower Blue with more transparency
        if self.begin != self.end:
            rect = QRect(self.begin, self.end).normalized()
            painter.drawRect(rect)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SnapTranslate")
        self.setGeometry(100, 100, 100, 50)  # Increased initial height

        app_icon = QIcon("src/gui/app_icon.jpg")
        self.setWindowIcon(app_icon)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        # Horizontal layout for buttons
        self.buttons_layout = QHBoxLayout()

        self.new_button = QPushButton("+ New")
        self.new_button.clicked.connect(self.start_screen_capture)
        self.buttons_layout.addWidget(self.new_button)

        self.translate_russian_button = QPushButton("Translate Russian")
        self.translate_russian_button.clicked.connect(lambda: self.translate("ru")) # Pass language code
        self.buttons_layout.addWidget(self.translate_russian_button)

        self.translate_swedish_button = QPushButton("Translate Swedish")
        self.translate_swedish_button.clicked.connect(lambda: self.translate("sv")) # Pass language code
        self.buttons_layout.addWidget(self.translate_swedish_button)

        self.main_layout.addLayout(self.buttons_layout)

        self.dark_theme_enabled = True
        if self.dark_theme_enabled:
            self.apply_dark_theme()

        self.capture_widget = None
        self.captured_image_data = None # Store the captured QPixmap
        self.captured_label = None
        self.translation_label = None

        # Initialize asyncio event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def apply_dark_theme(self):
        dark_stylesheet = """
            QMainWindow {
                background-color: #363636;
            }
            QWidget {
                background-color: #363636;
                color: #f0f0f0;
            }
            QLabel {
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #505050;
                color: #f0f0f0;
                border: 1px solid #606060;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
        """
        self.setStyleSheet(dark_stylesheet)

    def start_screen_capture(self):
        print("'+ New' button clicked. Starting screen capture.")
        self.showMinimized() # Minimize the main window
        QApplication.processEvents() # Ensure the window is minimized before capture

        self.capture_widget = ScreenCaptureWidget()
        screen_geometry = QApplication.desktop().screenGeometry()
        self.capture_widget.setGeometry(screen_geometry)
        self.capture_widget.showFullScreen()
        self.capture_widget.captured_image.connect(self.store_captured_image)

    def store_captured_image(self, image):
        print("Image captured!")
        self.captured_image_data = image
        if self.captured_label is None:
            self.captured_label = QLabel()
            self.main_layout.addWidget(self.captured_label)
        self.captured_label.setPixmap(self.captured_image_data.scaledToWidth(300))
        self.showNormal()

    def translate(self, source_language):
        if self.captured_image_data is not None:
            pil_image = self.qpixmap_to_pil_image(self.captured_image_data)
            async def translate_text():
                translated_text = await processing.process_image_and_translate(pil_image, target_language='en', source_language=source_language)
                self.display_translation(translated_text)
            asyncio.run(translate_text())

    def qpixmap_to_pil_image(self, pixmap):
        qimage = pixmap.toImage()
        temp_buffer = qimage.constBits().asstring(qimage.byteCount())
        pil_image = Image.frombuffer("RGBA", (qimage.width(), qimage.height()), temp_buffer, "raw", "RGBA", 0, 1)
        return pil_image

    def display_translation(self, text):
        print(f"Translated text: '{text}'")
        if self.translation_label is None:
            self.translation_label = QLabel()
            self.main_layout.addWidget(self.translation_label)
        self.translation_label.setText(f"{text}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())