VERSION = $(shell git describe)
TRANSLATIONS = de
PYGETTEXT = pygettext
MSGFMT = msgfmt

all: version.py wx_svnexport.py i18n

i18n: svnexport.pot SVNExportGUI.pot
	for transl in $(TRANSLATIONS); do \
		msgmerge -U --force-po locale/svnexport-$$transl.po svnexport.pot;\
		msgmerge -U --force-po locale/SVNExportGUI-$$transl.po SVNExportGUI.pot;\
		mkdir -p locale/$$transl/LC_MESSAGES;\
		$(MSGFMT) -o locale/$$transl/LC_MESSAGES/svnexport.mo locale/svnexport-$$transl.po;\
		$(MSGFMT) -o locale/$$transl/LC_MESSAGES/SVNExportGUI.mo locale/SVNExportGUI-$$transl.po;\
	done

.PHONY: version.py wx_svnexport.py version.iss svnexport.pot SVNExportGUI.pot

svnexport.pot:
	$(PYGETTEXT) -o $@ svnexport.py

SVNExportGUI.pot: wx_svnexport.py
	$(PYGETTEXT) -o $@ SVNExportGUI.py wx_svnexport.py

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
else
	@echo "Target only available on windows"
endif

clean:
	rm -rf build
	rm -rf dist
	rm -f version.py
	rm -f MANIFEST
	rm -f *.pyc
	rm -f version.*
	rm -f wx_*.py
