#! bash
rm -rf build dist;
pyinstaller --onefile --nowindowed --name="face-crop" --icon=icon.png main.py;
# pyinstaller --name="face-crop" --icon=icon.png main.py;
cp dist/face-crop.exe face-crop.exe