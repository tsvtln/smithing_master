# Smithing Master
Automation tools 



* [Auto Trove Section](#auto-trove)
* [Event Clicker Section](#event-clicker)
* [Auto Scarlet Corridor Section](#auto-scarlet)



## Features of `event clicker`
<a name="event-clicker"></a>

- 3-day event to auto-detect icon type and click based on the amount specified bellow the icon.
#### Requirements
Requirements inside `requirements.txt`
```
pyautogui
scikit-image
numpy
pytesseract
Pillow
opencv-python
tesseract executable
```


## Features of `auto trove`
<a name="auto-trove"></a>
- Performs automatic mining operation based on provided input.
- Automatic submition of daily bounties.
- Takes note of collected gems and sundries and provides an output after the mining operation of what is collected.
- Detects if an upgrade gem is found and waits on user input to further continue mining operation.

#### Requirements
Requirements inside `requirements.txt`
```
pyautogui
scikit-image
numpy
pytesseract
Pillow
opencv-python
tesseract
```
Works on 1920x1080 resolution with bluestacks on windowed fullscreen mode.

- You need to install Tesseract as the AI uses it to see the images. Make sure to install it in the default path (C:\Program Files\Tesseract-OCR\tesseract.exe)

#### How to install/run
- Install python
- Run 'python -m pip install <package>'  where package is the name of the package from the requirements. e.g.: 'python -m pip install pillow'
- Install tesseract to default path
- Run the auto_trove.py

Example video:

https://github.com/tsvtln/smithing_master/assets/112159858/77c2f497-7035-46ea-a816-884a888b7858



## Features of `Auto Scarlet Corridor`
<a name="auto-scarlet"></a>
- Handles mid-level start and progresses through any level.
- Automatically clicks on tiles, engaging in battles with monsters and collecting rewards.
- Automatically interprets and solves riddles presented during the game.
- Facilitates level progression, moving from one level to the next seamlessly.
- Manages interactions with the in-game shop, making decisions such as buying chests for gold.
- Collects chests from designated tiles.
- If a pillar is available on the level, selects from unselected options in order.


#### Usage
○ Works on 1920x1080 resolution with bluestacks on windowed fullscreen mode.

○ You need to have the scarlet level opened.

○ Need 'Skip' to be selected.

○ Input your current level.


- You need to install Tesseract as the AI uses it to see the images. Make sure to install it in the default path (C:\Program Files\Tesseract-OCR\tesseract.exe)

#### Requirements
Requirements inside `requirements.txt`
```
pyautogui
scikit-image
numpy
pytesseract
Pillow
opencv-python
tesseract
```

#### How to install/run
- Install python
- Run 'python -m pip install <package>'  where package is the name of the package from the requirements. e.g.: 'python -m pip install pillow'
- Install tesseract to default path
- Run the auto_scarlet.py

Example video:


https://github.com/tsvtln/smithing_master/assets/112159858/702bb65d-83f2-40a8-bdfc-ab2f4dcb2573

