#! bash
rm -rf build dist;
# pyinstaller --onefile --name="face-crop" --icon=icon.ico main.py;
pyinstaller --name="face-crop" --icon=icon.ico main.py;