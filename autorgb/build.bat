@ECHO OFF
:: This batch file builds the Windows binary for AutoRGB
ECHO Building binary. Please wait...
pyinstaller --noconfirm --log-level=WARN ^
  --noconsole --onefile ^
  --icon icon.ico ^
  autorgb.py
