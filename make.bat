@echo off
set PATH=.\bin;C:\Python27;C:\Programme\git\bin;C:\Programme\wxFormbuilder;C:\Programme\Inno Setup 5;C:\Programme\POEdit\bin
set TOOL_PATH=C:/Python27/Tools/i18n/
set PYGETTEXT=PYGETTEXT=%TOOL_PATH%pygettext.py
set MSGFMT=MSGFMT=%TOOL_PATH%msgfmt.py

bin\make dist %MSGFMT% %PYGETTEXT%
pause