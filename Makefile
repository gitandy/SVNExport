VERSION = $(shell git describe)

all: version.py wx_svnexport.py

.PHONY: version.py wx_svnexport.py

wx_svnexport.py:
	wxformbuilder --generate svnexport.fbp 

version.py:
	echo "VERSION = '$(VERSION)'" > $@

dist: all
ifeq ($(OS),Windows_NT)
	python setup_py2exe.py
	python setup_gui_py2exe.py	
endif
	echo "Target only available on windows"

clean:
	rm -rf build
	rm -rf dist
	rm -f version.py
	rm -f MANIFEST
	rm -f *.pyc
