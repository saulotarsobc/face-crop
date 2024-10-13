#! bash
rm -rf build dist;
pyinstaller --onefile --nowindowed --hide-console=hide-early --name="face-crop" --icon=icon.png main.py;