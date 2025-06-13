# TextArea
TextArea Application using PyQt6

## Description
- This application provides a simple TextArea with customizable themes and fonts.
- It also saves settings and restores them on startup.

> [!NOTE]
> Require Python 3.9 or above.

## Requirements

You can install them by using `requirements.txt` file:

Press `Win + R`, Then type `cmd`, And hit Enter
```
pip install -r requirements.txt
```
Or Do It Manual via command prompt `cmd`:

Press `Win + R`, Then type `cmd`, And hit Enter
```
pip install pyinstaller pyqt6
```

## Create EXE File

Press `Win + R`, Then type `cmd`, And hit Enter
```
pyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.ico;." --name "TextArea" TextArea.py
```
