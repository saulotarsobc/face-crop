#! bash
rm -rf build dist;
pyinstaller --onefile --nowindowed --name="face-crop" --icon=icon.png --add-data "haarcascade_frontalface_default.xml;." main.py;