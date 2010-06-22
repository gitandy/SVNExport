VERSION = $(shell git describe)

all: version.py wx_svnexport.py

.PHONY: version.py wx_svnexport.py version.iss

wx_svnexport.py:
	wxformbuilder --generate svnexport.fbp 

version.py:
	echo "VERSION = '$(VERSION)'" > $@

version.iss:
	echo "#define MyAppVersion \"$(VERSION)\"" > $@

dist: all version.iss
ifeq ($(OS),Windows_NT)
	python setup_py2exe.py
	python setup_gui_py2exe.py
	iscc /Q installer.iss	
endif
	@echo "Target only available on windows"

clean:
	rm -rf build
	rm -rf dist
	rm -f version.py
	rm -f MANIFEST
	rm -f *.pyc
	rm -f version.*
	rm -f wx_*.py
