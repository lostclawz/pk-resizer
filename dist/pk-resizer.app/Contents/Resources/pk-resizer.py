#!/usr/bin/python
import os
import sys
import ConfigParser
from easygui import *
import PIL
from PIL import Image, ImageTk

###
#
#	pk-resizer
#   ----------
# 	Resizes images with JPG compression
#	
###

class pk_resizer():

	def aspect( self, size ):
		return float( size[0] ) / float ( size[1] )

	def start(self):
		args = sys.argv[1:]
		if len(args) > 0:
			# filenames are in the arguments
			filenames = args
		else:
			# ask for filenames
			types = ("*.jpg", "*.jpeg", "*.png")
			filenames = fileopenbox(
				msg=None, 
				title="Select Image(s)", 
				default='*', 
				filetypes=types, 
				multiple=True
			)

		my_path = os.path.dirname(os.path.abspath(__file__))
		config_file = os.path.join(my_path, "configuration.cfg")
		config = ConfigParser.ConfigParser()
		config.read(config_file)

		# turn config into a dict with set of images
		image_versions = {}
		sections = config.sections()
		for s in sections:
			options = config.options(s)
			my_options = {}
			for o in options:
				my_options[o] = config.get(s, o)
			image_versions[s] = my_options
			
		# don't do anything if cancelled
		for filename in filenames:
			if filename != '' and filename != '.': 
				im = Image.open(filename)
				my_aspect = self.aspect( im.size )

				for t in image_versions:
					x = image_versions[t]
					# resize based on width or height?
					if 'width' in x and 'height' in x:
						# resize to width/height and ignore aspect ratio
						new_size = ( int( x['width'] ), int( x['height']) )
					elif 'width' in x:
						# resize based on width
						my_width = int( x['width'] )
						new_size = ( my_width , int( my_width / my_aspect ) )
					elif 'height' in x:
						#resize based on height
						my_height = int( x['height'] )
						new_size = ( int( my_aspect * my_height ), my_height )
					else:
						new_size = im.size
					subfolder = x['subfolder'] if 'subfolder' in x else 'resized'
					quality = int( x['quality'] ) if 'quality' in x else 100

					# file paths
					root_dir = os.path.split(filename)[0]
					new_filename = os.path.split(filename)[1]
					no_ext = os.path.splitext(new_filename)[0]
					new_filename = no_ext + ".jpg"

					new_folder = os.path.join(root_dir, subfolder)
					if not os.path.exists( new_folder ):
						os.makedirs( new_folder )

					new_path = os.path.join(new_folder, new_filename)
					resized_image = im.resize( new_size, Image.ANTIALIAS )
					resized_image.save( new_path, 'JPEG', quality = quality )

if __name__ == '__main__':	
	pk_resizer().start()