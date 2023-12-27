@ECHO OFF

REM Install required Python packages
pip install pyautogui
pip install scikit-image
pip install numpy
pip install pytesseract Pillow
pip install opencv-python

REM Download and install Tesseract from https://github.com/tesseract-ocr/tesseract
REM Add the Tesseract executable directory to the system PATH
REM The installation typically includes adding Tesseract to the PATH automatically
REM You might need to restart your command prompt or IDE after installing Tesseract

ECHO.
ECHO Installation completed. Verify Tesseract installation:
tesseract --version

PAUSE
