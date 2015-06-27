## pk-resizer ##
by Philip Kuperberg

Configurable image resizing utility 

# configuration.cfg:

	each section makes a new resized image
	the title of the section doesn't matter

	quality: 		jpg quality of resultant image (100 is default)
	width: 			scale image by width (maintain aspect ratio)
	height: 		scale image by height (maintain aspect ratio)
	(note- if BOTH width and height are specified, image will stretch)
	subfolder: 		the subfolder to place the images (relative to original directory)


Steps for distribution...

	Build setup.py file:
		py2applet --make-setup sw-resizer.py
	Clean up folders:
		rm -rf build dist
	Create app:
		python setup.py py2app