#! bash
rm -rf build dist face-crop.exe;
pyinstaller --onefile --nowindowed --name="face-crop" --icon=icon.png --add-data "haarcascade_frontalface_default.xml;." main.py;
cp dist/face-crop.exe face-crop.exe