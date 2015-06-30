#!/usr/bin/python
import os, sys, threading
import ConfigParser
from easygui import *
import PIL
from PIL import Image, ImageTk

#	pk-resizer
#   ----------
# 	Resizes images with JPG compression
#	
class pk_resizer():

	def __init__(self):
		# args = sys.argv[1:]
		self.start()

	def aspect( self, size ):
		return float( size[0] ) / float ( size[1] )

	def get_filenames( self ):
		types = ("*.jpg", "*.jpeg", "*.png")

		filenames = fileopenbox(
			msg=None, 
			title="Select Image(s)", 
			# default='*', 
			default=os.path.dirname(os.path.realpath(__file__)), 
			filetypes=types, 
			multiple=True
		)
		return filenames

	def resize_save( self, filename, image_versions ):
		im = Image.open(filename)
		my_aspect = self.aspect( im.size )

		for t in image_versions:
			x = image_versions[t]
			by_width = False
			by_height = False
			# resize based on width or height?
			if 'longest' in x:
				#resize based on longest size
				im_width = im.size[0]
				im_height = im.size[1]
				if im_width > im_height:
					# scale based on width
					my_width = int( x['longest'] )
					by_width = True
				else:
					# scale based on height
					my_height = int( x['longest'] )
					by_height = True
			elif 'width' in x and 'height' in x:
				# resize to width/height and ignore aspect ratio
				new_size = ( int( x['width'] ), int( x['height']) )
			elif 'width' in x:
				# resize based on width
				by_width = True
				my_width = int( x['width'] )
			elif 'height' in x:
				#resize based on height
				by_height = True
				my_height = int( x['height'] )
			else:
				new_size = im.size

			if by_width:
				# my_width = int( x['width'] )
				new_size = ( my_width , int( my_width / my_aspect ) )
			elif by_height:
				# my_height = int( x['height'] )
				new_size = ( int( my_aspect * my_height ), my_height )
			# other options
			subfolder = x['subfolder'] if 'subfolder' in x else 'resized'
			quality = int( x['quality'] ) if 'quality' in x else 100

			# file paths
			root_dir = os.path.split(filename)[0]
			new_filename = os.path.split(filename)[1]
			no_ext = os.path.splitext(new_filename)[0]
			new_filename = no_ext + ".jpg"
			if 'lowercase' in x and x['lowercase'] == 'true':
				new_filename = new_filename.lower()
			new_folder = os.path.join(root_dir, subfolder)
			if not os.path.exists( new_folder ):
				os.makedirs( new_folder )

			new_path = os.path.join(new_folder, new_filename)
			resized_image = im.resize( new_size, Image.ANTIALIAS )
			# the optimize flag causes IOError -2 in PIL
			# resized_image.save( new_path, 'JPEG', optimize=True, quality=quality )
			resized_image.save( new_path, 'JPEG', quality=quality )
		return

	def start(self):
		filenames = self.get_filenames()
		my_path = os.path.dirname(os.path.abspath(__file__))

		# read config file
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
		if filenames is not None:
			for filename in filenames:
				if filename != '' and filename != '.': 
					# start threading on each image
					t = threading.Thread(
						target=self.resize_save, 
						args=(filename, image_versions)
					)
					t.start()

if __name__ == '__main__':	
	pk_resizer()
