# SnapTranslate

SnapTranslate is a simple desktop application that allows you to capture a portion of your screen and instantly translate the text within it. It uses Tesseract OCR for text recognition and the Google Translate API (via the `googletrans` library) for translation.

## Features

* **Screen Capture:** Easily select an area of your screen to capture.
* **Instant Translation:** Translate the captured text to English.
* **Language Support:** Currently supports translation from Russian and Swedish to English. More will added in future developments.
* **Configurable Tesseract Path:** Allows you to specify the path to your Tesseract installation via a `config.ini` file.

## Installation

### Prerequisites

* **Python 3.6 or higher** (3.13 recommended)
* **Tesseract OCR Engine:** SnapTranslate relies on Tesseract for text recognition. You need to have Tesseract installed on your system and the language data packs for Russian (`rus`) and Swedish (`swe`). You can download Tesseract from [https://github.com/tesseract-ocr/tesseract/wiki](https://github.com/tesseract-ocr/tesseract/wiki). Make sure to install the language packs as well.
* **pip (Python package installer)**

### Installation Steps

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/your-github-username/SnapTranslate.git](https://github.com/tousif47/SnapTranslate.git)
    cd SnapTranslate
    ```

2.  **Install the required Python packages:**

    ```bash
    pip install .
    ```

    (This command assumes you are in the root directory of the project where the `setup.py` file is located. It will install SnapTranslate and all its dependencies.)

## Usage

1.  **Run the application:**

    ```bash
    snaptranslate
    ```

    This command should launch the SnapTranslate GUI.

2.  **Capture Screen Area:** Click the "+ New" button. Your screen will become dimmed, and you can click and drag to select the area you want to capture. Release the mouse button to capture.

3.  **Translate:** After capturing, you will see two buttons: "Translate Russian" and "Translate Swedish". Click the button corresponding to the language of the text in your captured area.

4.  **View Translation:** The translated text will be displayed in the text area at the bottom of the window.

## Configuration

You can configure the path to your Tesseract installation by modifying the `config.ini` file located in the root directory of the project.

1.  **Locate `config.ini`:** This file should be in the same directory as your `setup.py` file.
2.  **Edit `config.ini`:** Open the file in a text editor. You should see a section like this:

    ```ini
    [Tesseract]
    TESSDATA_PATH = /path/to/your/tessdata
    ```

3.  **Update the path:** Replace `/path/to/your/tessdata` with the actual path to the `tessdata` directory of your Tesseract installation on your system. For example:

    ```ini
    [Tesseract]
    TESSDATA_PATH = C:\Program Files\Tesseract-OCR\tessdata
    ```

    or

    ```ini
    [Tesseract]
    TESSDATA_PATH = /usr/share/tesseract-ocr/tessdata
    ```

    Make sure to use the correct path for your operating system.

## Supported Languages

Currently, SnapTranslate supports translation from:

* Russian to English
* Swedish to English

## Contributing

TBA

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

googlepytrans

---

Thank you for using SnapTranslate!