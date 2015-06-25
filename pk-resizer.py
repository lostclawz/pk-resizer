#!/usr/bin/python
import os
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

class sw_thumbs():

	def aspect( self, size ):
		# if you have width: aspect * image_width
		# if you have height: image_width / aspect
		return float( size[0] ) / float ( size[1] )

	def start(self):

		my_path = os.path.dirname(os.path.abspath(__file__))
		config_file = os.path.join(my_path, "configuration.cfg")
		config = ConfigParser.ConfigParser()
		config.read(config_file)

		# read settings from config
		full_width 		 = int(config.get('SIZES', 'full_size_width'))
		thumb_width 	 = int(config.get('SIZES', 'thumb_width'))

		subfolder 		 = str(config.get('FOLDERS', 'subfolder'))
		thumbs_subfolder = str(config.get('FOLDERS', 'thumbs_subfolder'))

		jpg_quality_full = int(config.get('QUALITY', 'jpg_quality_full'))
		jpg_quality_thumbs = int(config.get('QUALITY', 'jpg_quality_thumbs'))

		types = ("*.jpg", "*.jpeg", "*.png")
		filenames = fileopenbox(
			msg=None, 
			title="Select Image(s)", 
			default='*', 
			filetypes=types, 
			multiple=True
		)

		# don't do anything if cancelled
		for filename in filenames:
			if filename == '' or filename == '.': 
				return
			
			im = Image.open(filename)
			my_aspect = self.aspect( im.size )
			
			# resizing based on width
			thumb_new_size = ( thumb_width, int( thumb_width / my_aspect ) )
			full_new_size = ( full_width, int( full_width / my_aspect ) )

			# file paths
			root_dir = os.path.split(filename)[0]
			new_filename = os.path.split(filename)[1]
			no_ext = os.path.splitext(new_filename)[0]
			new_filename = no_ext + ".jpg"

			full_folder = os.path.join(root_dir, subfolder)
			thumbs_folder = os.path.join(root_dir, thumbs_subfolder)
			
			# create directories if they don't exist
			if not os.path.exists(full_folder):
				os.makedirs(full_folder)
			if not os.path.exists(thumbs_folder):
				os.makedirs(thumbs_folder)

			thumb_path = os.path.join(thumbs_folder, new_filename)
			full_path = os.path.join(full_folder, new_filename)

			if (full_new_size[0] < im.size[0] or full_new_size[1] < im.size[1]):
				image_full = im.resize( full_new_size, Image.ANTIALIAS )
			else:
				image_full = im
				print ("Not necessary to resize, image is too small: " + str(im.size[0]) + " x " + str(im.size[1]))

			image_full.save( full_path, 'JPEG', quality = jpg_quality_full )

			image_thumb = im.resize( thumb_new_size, Image.ANTIALIAS )
			image_thumb.save( thumb_path, 'JPEG', quality = jpg_quality_thumbs )
		

if __name__ == '__main__':	
	sw_thumbs().start()