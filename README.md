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

1.  **Clone the repository (optional, if you are installing from PyPI directly you can skip this):**

    ```bash
    git clone [https://github.com/tousif47/SnapTranslate](https://github.com/tousif47/SnapTranslate.git)
    cd SnapTranslate
    ```

2.  **Install SnapTranslate from PyPI:**

    ```bash
    pip install snaptranslate
    ```

    (This command will download and install SnapTranslate and all its dependencies.)

### Running the Application

Once the installation is complete, you can run SnapTranslate from your command prompt or terminal.

1.  **Open a new command prompt (on Windows) or terminal (on macOS/Linux).**

2.  **Type the following command and press Enter:**

    ```bash
    snaptranslate
    ```

    This command should launch the SnapTranslate GUI.

    **Note:** If you get an error like "'snaptranslate' is not recognized...", it means your system's PATH environment variable is not set up to include the directory where `pip` installed the `snaptranslate` script. Here's how you might resolve this:

    * **Windows:** The script is likely in your Python installation's `Scripts` folder (e.g., `C:\Python3x\Scripts` or within your virtual environment's `Scripts` folder if you used one). You might need to add this directory to your system's PATH. You can search online for "how to add Python to PATH on Windows" for detailed instructions.

    * **macOS/Linux:** If you installed globally, the script might be in `/usr/local/bin` or `/usr/bin`, which are usually in the PATH. If you used a virtual environment, make sure it is activated before running the command.

### Configuration

You can configure the path to your Tesseract installation by modifying the `config.ini` file located in the root directory of the project.

1.  **Locate `config.ini`:** This file should be in the same directory as your `setup.py` file (if you cloned the repository) or in the location where the application is installed (you might need to create it if it doesn't exist).
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