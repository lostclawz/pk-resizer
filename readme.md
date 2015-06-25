pk-resizer
----------
	Image resizing utility
	Options available in configuration.cfg

Steps for distribution...

	Build setup.py file:
		py2applet --make-setup sw-resizer.py
	Clean up folders:
		rm -rf build dist
	Create app:
		python setup.py py2app