from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.templatetags.static import static
from django.conf import settings
from django.utils import simplejson

from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from django.http import Http404  
import os 
import subprocess

from PIL import Image, ImageChops, ImageOps

import datetime

import uuid


from materials.movparser import MovParser
from PIL import Image, ImageChops

_SAN_PATH = 'F:'
_DROPBOX_PATH = 'Z:\DVD'

# create list of drives
_available_drives = [ ('SAN', 'F:'), ('DROPBOX', 'Z:\DVD')]  # NOT USED!!

# Create your views here.
def show_dir(request):
	
	if request.GET.get('path'):
		virtual_path = request.GET['path']	
		virtual_path = virtual_path.replace('/','\\')
		virtual_path = virtual_path.rstrip('\\')

		if virtual_path.upper().startswith('SAN'):
			virtual_path = virtual_path.replace('san', 'SAN', 1)
			path = virtual_path.replace('SAN', _SAN_PATH, 1)
		elif virtual_path.upper().startswith('DROPBOX'):
			virtual_path = virtual_path.replace('dropbox', 'DROPBOX', 1)
			path = virtual_path.replace('DROPBOX', _DROPBOX_PATH, 1)
		else:
			virtual_path = 'SAN'
			path = _SAN_PATH
	else:
		virtual_path = 'SAN'
		path = _SAN_PATH

	(path, dirs, files) = os.walk(path).next()

	if virtual_path == 'SAN' or virtual_path == 'DROPBOX':
		back_path = ""
	else:
		back_path = os.path.dirname(virtual_path)

	mov_files = []

	for item in files:
		if item.endswith('.mov') and not item.startswith('.'):
			mov_files.append(item) 

	listing = (virtual_path, path, back_path, dirs, mov_files)

	context = {'page_title': 'Directory listing', 'listing': listing}
	return render(request, 'materials/dir.html', context)

def show_file(request):
	if request.GET.get('file'):
		virtual_file = virtual_path = request.GET['file']

		if virtual_file.upper().startswith('SAN'):
			virtual_file = virtual_file.replace('san', 'SAN', 1)
			logical_file = virtual_file.replace('SAN', _SAN_PATH, 1)
		elif virtual_path.upper().startswith('DROPBOX'):
			virtual_file = virtual_file.replace('dropbox', 'DROPBOX', 1)
			logical_file = virtual_file.replace('DROPBOX', _DROPBOX_PATH, 1)

		path, filename = os.path.split(virtual_file)

		listing = (virtual_file, logical_file, filename)

		if os.path.isfile(logical_file):

			file_info = MovParser(logical_file)
			file_info.ParseIt()

			return_path = os.path.dirname(virtual_file)

			thumbnail_exists, thumbnail = get_thumbnail(virtual_file, logical_file, file_info.duration)

			context = {'page_title': 'File details', 'listing': listing, 'file_info': file_info, 'return_path': return_path, 'thumbnail_exists': thumbnail_exists, 'thumbnail': thumbnail, 'filename':virtual_file }
			return render(request, 'materials/file.html', context)
		else:
			return HttpResponseRedirect(reverse('show_dir'))

def get_thumbnail(virtual_file, logical_file, duration):
	ffmpegPath = 'C:\\ffmpeg\\bin\\ffmpeg.exe'

	slug_file = virtual_file.replace('\\', '-')
	slug_file = slug_file.replace('.', '-')
	slug_file = slugify(slug_file)
	slug_file = slug_file + '.jpg'

	slug_file_path = settings.STATICFILES_DIRS[0] + '/thumbnails/' + slug_file
	slug_file_url = settings.STATIC_URL + 'thumbnails/' + slug_file

	duration = duration / 4 

	if os.path.isfile(slug_file_path):
		return True, slug_file_url
	else:
		# create thumbnail
		startupinfo = None
		if os.name == 'nt':
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW

			exeString = ffmpegPath + ' -ss ' + str(duration) + ' -i \"' + logical_file + '\" -vframes 1 -f image2 -pix_fmt rgb24 -q:v 6 \"' + slug_file_path + '\"'		
			
			#print exeString
			subprocess.Popen(exeString) #, startupinfo=startupinfo))
		return False, slug_file_url

def return_aspect(request):
	filename = request.POST['filename']
	duration = request.POST['duration']
	if len(duration) == 7:
		duration = datetime.datetime.strptime(duration, '%H:%M:%S')
		delta = datetime.timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
	else:
		duration = datetime.datetime.strptime(duration, '%H:%M:%S.%f')
		delta = datetime.timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second, microseconds=duration.microsecond)
	print duration
	
	print delta
	width = int(request.POST['width'])
	height = int(request.POST['height'])

	if filename.upper().startswith('SAN'):
		filename = filename.replace('san', 'SAN', 1)
		filename = filename.replace('SAN', _SAN_PATH, 1)
	elif filename.upper().startswith('DROPBOX'):
		filename = filename.replace('dropbox', 'DROPBOX', 1)
		filename = filename.replace('DROPBOX', _DROPBOX_PATH, 1)

	return_dict = getAspectRatio(filename, delta, width, height)

	json = simplejson.dumps(return_dict)
	return HttpResponse(json, mimetype="application/x-javascript")

def getAspectRatio(filename, duration, width, height):  

	workingDir = 'F:\\Tools\\DVDTools\\Temp\\'
	ffmpegPath = 'C:\\ffmpeg\\bin\\ffmpeg.exe'

	numGrabs = 4
	uniqueID = uuid.uuid4()		
	#print uniqueID
	interval = duration / (numGrabs+1)
	imageW = width
	imageH = height
	currentTime = datetime.timedelta(seconds=0)
	aspectRatio = 0.00
	exeFiles = []
	processedFiles = []
	
	try:

		
		startupinfo = None
		if os.name == 'nt':
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW

		for x in range(0, numGrabs):				
			currentTime = currentTime + interval

			tempSourceFilename = filename.replace("/", "\\")
			tempImgFilename = workingDir + str(uniqueID) + '_' + str(x).zfill(3) + '.png'
			exeString = ffmpegPath + ' -ss ' + str(currentTime) + ' -i \"' + tempSourceFilename + '\" -vframes 1 -f image2 -pix_fmt rgb24 \"' + tempImgFilename + '\"'
			
			
			#print exeString
			exeFiles.append(subprocess.Popen(exeString, startupinfo=startupinfo))
			#wait = exeFFMPEG.wait()
			
			processedFiles.append(tempImgFilename)
			
		
		for index, item in enumerate(processedFiles):
			exeFiles[index].wait()
			if index == 0:
				baseImage = Image.open(item)
				
			else:
				img = Image.open(item)
				baseImage = ImageChops.add(baseImage, img, 2.0)
				os.remove(item)
		
		os.remove(processedFiles[0])
		
		
		bgImage = Image.new('RGB' , (imageW,imageH))
		baseImage = ImageOps.autocontrast(baseImage, 40)
		diff = ImageChops.difference(baseImage, bgImage)
		#diff = ImageChops.add(diff, diff, 0.5)

		bbox = diff.getbbox()
		#print bbox
		if bbox:
			cropImage = baseImage.crop(bbox)
			newW, newH = cropImage.size
		else:
			newH = imageH

		cropImage.save('c:\\Temp\\output.png', 'png')

		cropValues = ( bbox[0], bbox[1], imageW-bbox[2], imageH-bbox[3])

		crop = 'Left: ' + str(cropValues[0]) + '<br />'
		crop += 'Top: ' + str(cropValues[1]) + '<br />'
		crop += 'Right: ' + str(cropValues[2]) + '<br />'
		crop += 'Bottom: ' + str(cropValues[3])

		#SDHACK
		if imageW == 720:
			imageW = 1024
			
		aspectRatio = float(imageW) / float(newH)		
		aspectRatio = round(aspectRatio,2)

		if aspectRatio == 1.78 or aspectRatio == 1.85 or aspectRatio == 2.35 or aspectRatio == 2.40:
			css_class = 'green-tooltip'
		elif aspectRatio > 1.75 and aspectRatio < 1.79:
			aspectRatio = 1.78
			css_class = 'orange-tooltip'
		elif aspectRatio > 1.82 and aspectRatio < 1.87:
			aspectRatio = 1.85
			css_class = 'orange-tooltip'
		elif aspectRatio > 2.31 and aspectRatio < 2.36:
			aspectRatio = 2.35
			css_class = 'orange-tooltip'
		elif aspectRatio > 2.38 and aspectRatio < 2.42:
			aspectRatio = 2.40
			css_class = 'orange-tooltip'
		else:
			css_class = 'red-tooltip'

		aspectRatio = "{0:.2f}".format(aspectRatio) + ':1'

		aspect_info = { 'aspect': aspectRatio,
						'css_class': css_class,
						'crop' : crop,
						 }

		return aspect_info

	except Exception,e:
		error = "Error: " + str(e)
		print error
		#raise
		#continue 
				
