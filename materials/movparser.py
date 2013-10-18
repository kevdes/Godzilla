import os
from videoparser import *
import datetime
import time
import re

_warning_icon = 'icon-warning-sign red-tooltip'
_ok_icon = 'icon-ok-sign green-tooltip'
_query_icon = 'icon-question-sign orange-tooltip'


class MovParser():

	def __init__(self, filename):
		self.filename = filename
		
		self.path, self.name = os.path.split(self.filename)
		self.baseFilename = os.path.splitext(self.name)[0] 
		if self.baseFilename.endswith('_HD'):
			self.baseFilename = self.baseFilename[:-3]
		
		self.file_size = None
		self.checksum_filename = os.path.splitext(self.filename)[0] + '.md5'

		self.trackID = 0
		self.audioTrackID = 0
		
		self.resolution = ''
		self.resWidth = ''
		self.resHeight = ''
		self.aspectRatio = 0.00
		
		self.actualFramerate = 0
		self.adjustedFramerate = 0
		self.txtFramerate = ''
		
		
		self.duration = 0

		self.txtDuration = ''
		self.sourceTC = 0
		self.newSourceTC = 0
		self.dropFrame = 0
		self.codec = ''
		self.videoInfo = ''
		
		
		#audio
		self.audioTrack = 0
		self.audioCodec = ''
		self.audioInfo = ''
		self.audioChannels = 1
		self.mainAudioCodec = ''
		self.sampleRate = 1
		self.totalAudioChannels = 0
		self.trackAssignemnt = ''
		self.audioList = []
		
	def ParseIt(self):
	
		self.file_size = os.path.getsize(self.filename)
		self.file_created = datetime.datetime.fromtimestamp(os.path.getctime(self.filename))
		self.file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(self.filename))

		vidParser = VideoParser()
		#print self.filename + '\n'
		details = vidParser.parse_file(self.filename)
		# details = repr(vidParser.parse_file(filename))
		#print details.duration

		for video_stream in details.video_streams:
			self.resWidth = video_stream._width
			self.resHeight = video_stream._height
			self.resolution = str(self.resWidth) + ' x ' + str(self.resHeight)
			self.trackID = video_stream._trackID
			
			self.actualFramerate = video_stream._framerate
			self.setFramerate()

			self.field_type = video_stream._field_type
			self.field_order = video_stream._field_order
			self.color_space = video_stream._color_space 
			self.pasp = video_stream._pasp
			self.clap = video_stream._clap
			self.gamma = video_stream._gamma 
			self.clean_aperture = video_stream._clean_aperture
			self.prod_aperture = video_stream._prod_aperture
			self.enc_aperture = video_stream._enc_aperture


			self.duration = video_stream._duration
			self.dropFrame = details.dropFrame
			self.codec = video_stream._codec
			#self.sourceTC = pytimecode.PyTimeCode(self.actualFramerate, None, video_stream._sourceTC)
			self.sourceTC = self.framestoTC(self.adjustedFramerate, video_stream._sourceTC)
			self.newSourceTC = self.sourceTC
			
			decPoint = str(self.duration).rfind('.')


			if decPoint > 0:			
				self.txtDuration = str(self.duration)[:len(str(self.duration))-decPoint].zfill(8) + ':' + str(int(self.actualFramerate * float(str(self.duration)[-(decPoint):]))).zfill(2)
			else:	
				self.txtDuration = str(self.duration)[:len(str(self.duration))-decPoint].zfill(8) + ':00'
			
			self.updateVideoInfo()
			
			"""
			if self.actualFramerate > 23.900 and self.framerate < 23.999:
				self.actualFramerate = 23.976
			
			self.txtFramerate = "{0:.3f}".format(self.actualFramerate)
			if str(self.txtFramerate)[2:] == ".000" :
				self.txtFramerate = self.txtFramerate[:2]
			#print self.resolution  #video_stream.codec
			"""


		self.audio_tracks = []

		for audio_stream in details.audio_streams:
			self.audioTrack = self.audioTrack + 1
			self.audioChannels = audio_stream._channels
			self.totalAudioChannels = self.totalAudioChannels + self.audioChannels
			self.audioCodec = audio_stream._codec
			if self.mainAudioCodec == '':
				self.mainAudioCodec = self.audioCodec
			self.sampleRate = audio_stream._sample_rate
			self.trackAssignemnt = audio_stream._track_assignemnt
			self.audioTrackID = audio_stream._trackID
			
			self.audioInfo = self.audioInfo + str('Track #' + str(self.audioTrack) + ': ')
			self.audioInfo = self.audioInfo + ' ' + str(self.trackAssignemnt) + ' '	
			self.audioInfo = self.audioInfo + '\nChannels: ' + str(self.audioChannels) + '  '
			self.audioInfo = self.audioInfo + 'Bitrate: ' + str(self.audioCodec) + '  '
			self.audioInfo = self.audioInfo + 'Sample Rate: ' + str(self.sampleRate/1000) + 'kHz  '			
			self.audioInfo = self.audioInfo + 'TID: ' + str(self.audioTrackID) + '\n\n'			
			
			self.audioList.append({'channels': self.audioChannels, 'assignment': self.trackAssignemnt, 'streamID': self.audioTrackID})
			self.audio_tracks.append(
				{'track_num': self.audioChannels,
				 'channels': self.audioChannels,
				 'codec': self.audioCodec,
				 'sample_rate': str(self.sampleRate/1000) + 'kHz',
				 'track_assignment': self.trackAssignemnt,
				 'validate': '',
				}
			)
		
		self.validate_audio_tracks()

		self.audioInfo = self.audioInfo + 'Total audio channels: ' + str(self.totalAudioChannels) + '\n'
		#print self.audioInfo
		#print repr(details)
		
		"""
			if not metadata:
				self.statusBar().showMessage("Unable to extract metadata")
				exit(1)
		"""
		"""
		
				
		for i in range(10):
			self.ui.fileItems.addItem('Item %s' % (i + 1))
		"""
	
	def updateVideoInfo(self):
		self.videoInfo = ''
		self.videoInfo = self.videoInfo + str('Codec: \t' + str(self.codec) + '\n')
		self.videoInfo = self.videoInfo + str('Resolution: \t' + str(self.resolution) + '\n')
		if self.dropFrame == 1:
			self.videoInfo = self.videoInfo + str('Frame Rate: \t' + str(self.txtFramerate) + ' Drop frame\n')
		else:
			self.videoInfo = self.videoInfo + str('Frame Rate: \t' + str(self.txtFramerate) + '\n')
			
		self.videoInfo = self.videoInfo + str('Duration: \t' + str(self.txtDuration) + '\n')

		if self.newSourceTC == self.sourceTC:
			self.videoInfo = self.videoInfo + str('Start timecode: \t' + str(self.newSourceTC) + '\n')
		else:
			self.videoInfo = self.videoInfo + str('Start timecode: \t' + str(self.newSourceTC) + ' (!)\n')
			
		if not self.aspectRatio == 0.00:
			
			self.videoInfo = self.videoInfo + str('Aspect ratio: \t' + str("{0:.2f}".format(self.aspectRatio)) + ':1\n')
				
		self.videoInfo = self.videoInfo + str('\nTID: ' + str(self.trackID) + '\n')
		
		nameTemp = os.path.splitext(self.name)[0] 
		if nameTemp.endswith('_HD'):
			nameTemp = nameTemp[:-3]
			
		if not self.baseFilename == nameTemp:
			self.videoInfo = self.videoInfo + str('\nBase filename: \t' + str(self.baseFilename) + '\n')
	
	
	def setFramerate(self):
		print self.actualFramerate
		if self.actualFramerate == 23.976 or self.actualFramerate == 24 or self.actualFramerate == 25  or self.actualFramerate == 29.97:
			self.adjustedFramerate = self.actualFramerate
			if self.actualFramerate == 24.0:
				self.txtFramerate = '24'
			elif self.actualFramerate == 25.0:
				self.txtFramerate = '25'
			else:
				self.txtFramerate = str(self.actualFramerate)
		elif self.actualFramerate > 23.90 and self.actualFramerate < 23.99:
			self.adjustedFramerate = 23.976
			self.txtFramerate = '23.976 ('+str(self.actualFramerate)+')'
		elif self.actualFramerate > 23.99 and self.actualFramerate < 24.2:
			self.adjustedFramerate = 24
			self.txtFramerate = '24 ('+str(self.actualFramerate)+')'
		elif self.actualFramerate > 24.8 and self.actualFramerate < 25.6:
			self.adjustedFramerate = 25
			self.txtFramerate = '25 ('+str(self.actualFramerate)+')'
		elif self.actualFramerate > 29.8 and self.actualFramerate < 29.99:
			self.adjustedFramerate = 29.97
			self.txtFramerate = '29.97 ('+str(self.actualFramerate)+')'
		else:
			self.adjustedFramerate = self.actualFramerate
			self.txtFramerate = str(self.actualFramerate) + ' <--'
			
		
	
	def framestoTC(self, framerate, frames):
		if frames == -1:
			return 'Unknown'
				
		#print frames
		if self.dropFrame == 0:			
			hours = frames/(3600*framerate)
			mins = (frames%(3600*framerate))/(60*framerate)
			if mins%10: #if the minutes is not a multiple of 10, there needs to be one more drop frame unit, 2 or 4
				extra = 1
			else:
				extra = 0
			if framerate == 29.97:
				frames = frames - (hours * 6 * 18) + ((mins/10) *18) + (mins%10 * 2) + (extra * 2) # - 2  ??
			elif framerate == 23.976:
				framerate = 24
				#frames = frames - (hours * 6 * 18) + ((mins/10) *18) + (mins%10 * 2) - 2
				
		#if self.framerate == '59.94':
		#		return (hours * 6 * 36) + ((mins/10) *36) + (mins%10 * 4) + (extra * 4)
		
		
		seconds = (float(frames) / framerate)
		duration = datetime.timedelta(seconds=seconds)

		#print duration
		
		decPoint = str(duration).rfind('.')

		if decPoint > 0:
			#always 7 characters
			decPoint = 7
			timecode = str(duration)[:len(str(duration))-(decPoint)].zfill(8) + ':' + str(int(framerate * float(str(duration)[-(decPoint):]))).zfill(2)
		else:	
			timecode = str(duration)[:len(str(duration))-decPoint].zfill(8) + ':00'
			
		return timecode
		
	def calc_drop_frames(self):
		#print 'hi'
		return (self.hrs * 6 * 18) + ((self.mins/10) *18) + (self.mins%10 * 2)
        
		
			
	def getResolution(self):
		return self.resolution
	
	def writeAVS(self, parent, outputFileName):
		buffer = ''
		buffer = buffer + 'QTInput("' + self.name + '")\n'
		
		if self.adjustedFramerate == 23.976:
			buffer = buffer + 'AssumeFPS(24000, 1001, true)\n'
		elif self.adjustedFramerate == 24:
			buffer = buffer + 'AssumeFPS(24, 1, true)\n'
		elif self.adjustedFramerate == 25:
			buffer = buffer + 'AssumeFPS(25, 1, true)\n'
		elif self.adjustedFramerate == 29.97:
			buffer = buffer + 'AssumeFPS(30000, 1001, true)\n'
			
		buffer = buffer + 'ConvertToYUY2()\n'
		
		
		# Write mode creates a new file or overwrites the existing content of the file. 
		# Write mode will _always_ destroy the existing contents of a file.
		try:
			# This will create a new file or **overwrite an existing file**.
			parent.statusBar().showMessage('Writing ' + outputFileName + '...')
			f = open(outputFileName, "w")
			try:
				# f.write('blah') # Write a string to a file
				f.writelines(buffer) # Write a sequence of strings to a file
			finally:
				f.close()
				parent.statusBar().showMessage('Ready...')
		except IOError:
			pass
			
		#print buffer

	def validate_codec(self):
		if not self.codec == 'Apple ProRes 422 (HQ)':
			return (_warning_icon, 'Codec is not <b>Apple ProRes 422 (HQ)</b>')
		else:
			return (_ok_icon, '')

	def validate_resolution(self):
		if self.resolution == '1920 x 1080':
			return (_ok_icon, '')
		elif self.resolution == '720 x 576' and self.adjustedFramerate == 25:
			return (_ok_icon, '')
		else:
			return (_query_icon, 'Incorrect resolution?')

	def validate_tapt(self):
		if self.clean_aperture == (1888,1062):
			return (_warning_icon, 'Clean aperture not correct')
		elif self.clean_aperture == (1920,1080) and self.prod_aperture == (1920,1080) and self.prod_aperture == (1920,1080):
			return (_ok_icon, '')
		elif self.resolution == '1920 x 1080' and self.clean_aperture == None and self.prod_aperture == None and self.prod_aperture == None:
			return (_ok_icon, '')
		elif self.resolution == '720 x 576' and self.adjustedFramerate == 25:
			if self.clean_aperture == (1024,576) and self.prod_aperture == (1024,576) and self.enc_aperture ==(720,576):
				return (_ok_icon, '')
			else:
				return (_warning_icon, 'TAPT info not correct')
		else:
			return (_query_icon, 'TAPT info not correct')
			

	def validate_fields(self):
		if self.field_type == 'Progressive' :
			return (_ok_icon, '')	
		else:
			return (_warning_icon, 'Video should be <b>Progressive</b>.')

	def validate_color_space(self):
		if not self.gamma == None:
			return (_warning_icon, 'Gamma should not be set.')
		else:
			if self.resolution == '1920 x 1080' and self.color_space == 'HD':
				return (_ok_icon, '')
			elif self.resolution == '720 x 576' and self.adjustedFramerate == 25 and self.color_space == 'PAL':
				return (_ok_icon, '')
			elif self.color_space == None:
				return (_warning_icon, 'Colorspace not set.')
			else:
				return (_query_icon, 'Colorspace incorrect.')

	def validate_pasp(self):
		if self.resolution == '1920 x 1080' and self.pasp == None:
			return (_ok_icon, '')
		elif self.resolution == '1920 x 1080' and self.pasp == '1:1':
			return (_ok_icon, '')
		elif self.resolution == '720 x 576' and self.adjustedFramerate == 25:
			if self.pasp == 'PAL 16x9':
				return (_ok_icon, '')
			elif self.pasp == 'PAL 4x3':
				return (_query_icon, 'Should video aspect be 16x9?')
		else:
			return (_query_icon, '')

	def validate_clap(self):
		if self.clap == None :
			return (_ok_icon, '')	
		else:
			return (_warning_icon, 'Clap should not be set.')

	def validate_checksum(self):
		if not os.path.isfile(self.checksum_filename):
			if os.path.isfile(self.path + '\checksums.md5'):
				self.checksum_filename = self.path + '\checksums.md5'
			elif os.path.isfile(self.path + '\md5sum.lst'):
				self.checksum_filename = self.path + '\md5sum.lst'
			else:
				return (_warning_icon, 'Checksum not created or<br />checksum filename does not<br />match video filename.', '')

		checksum_value = self.read_checksum()

		if datetime.datetime.fromtimestamp(os.path.getmtime(self.filename)) > datetime.datetime.fromtimestamp(os.path.getmtime(self.checksum_filename)):
			return (_query_icon, 'Movie file has been modified after checksum was created.', checksum_value)
		elif checksum_value == '':			
			return (_warning_icon, 'Checksum value not contained in checksum file.', '')			
		else:
			return (_ok_icon, '', checksum_value)
		
	def read_checksum(self):

		checksum_file = open(self.checksum_filename, "r") #'B483338DBCADFB00782BDF00055893EF *LuckyMiles-Feature-HD-185-24-en-8ch.mov\nAA83338DBCADFB00782BDF00055893EF *LuckyMiles-Feature-HD-185-24-en-8ch.mov'
		checksum_text = checksum_file.read()
		checksum_file.close()

		if not checksum_text == '':
			matches = re.finditer(r'(?=([A-F0-9]{32})( \*' + self.name + '))', checksum_text)
			results = [match.group(1) for match in matches]

			if len(results) > 0:
				return results[0]
		
		return ''

	def validate_num_audio_tracks(self):			
		if len(self.audio_tracks) == 6:
			return (_warning_icon, 'Incorrect number of audio tracks.<br />Stereo mix missing.')
		elif not ((self.audioTrack == 1 and self.totalAudioChannels == 2) or (self.audioTrack == 7 and self.totalAudioChannels == 8) ):
			return (_warning_icon, 'Incorrect number of audio tracks.')

	def validate_audio_tracks(self):
		for index, audio_track in enumerate(self.audio_tracks):
			warning_icon = _ok_icon
			warning = ''
			if len(self.audio_tracks) == 1:
				if audio_track['channels'] == 2:
					if not audio_track['track_assignment'] == 'Left Total  Right Total  ':
						warning_icon = _warning_icon
						warning += 'Correct track names not assigned.<br />'
				else:
					warning_icon = _warning_icon
					warning += 'Should be stereo mix.<br />'
			elif len(self.audio_tracks) == 2 and ((index+1 == 1 and audio_track['channels'] == 1) or (index+1 == 2 and audio_track['channels'] == 1)):
				warning_icon = _warning_icon
				warning += 'Stereo mix should not be dual mono.<br />'				
			elif len(self.audio_tracks) == 8 and ((index+1 == 7 and audio_track['channels'] == 1) or (index+1 == 8 and audio_track['channels'] == 1)):
				warning_icon = _warning_icon
				warning += 'Stereo mix should not be dual mono.<br />'
			else:
				if (index+1 < 7 and audio_track['channels'] == 1) or (index+1 == 7 and audio_track['channels'] == 2):
					if ((index+1 == 1 and audio_track['track_assignment'] == 'Left  ') or 
						(index+1 == 2 and audio_track['track_assignment'] == 'Right  ') or 
						(index+1 == 3 and audio_track['track_assignment'] == 'Center  ') or 
						(index+1 == 4 and audio_track['track_assignment'] == 'LFE  ') or 
						(index+1 == 5 and audio_track['track_assignment'] == 'Ls  ') or 
						(index+1 == 6 and audio_track['track_assignment'] == 'Rs  ') or
						(index+1 == 7 and audio_track['track_assignment'] == 'Left Total  Right Total  ')):
						pass
					else:
						warning_icon = _warning_icon
						warning += 'Correct track name not assigned.<br />'
				elif (index+1 < 7 and audio_track['channels'] == 2):
					warning_icon = _warning_icon
					warning += 'Track ' + str(index+1) + ' should be Mono channel.<br />'
				elif (index+1 == 7 and audio_track['channels'] == 1):
					warning_icon = _warning_icon
					warning += 'Track 7 should be Stereo Mix.<br />'
				else:
					warning_icon = _query_icon
					warning += 'Unknown audio setup.<br />'

			if not (audio_track['codec'] == '16' or audio_track['codec'] == '24'):
				warning_icon = _warning_icon
				warning += '16 or 24 bit audio required.<br />'
			if not audio_track['sample_rate'] == '48.0kHz':
				warning_icon = _warning_icon
				warning += 'Sample rate should be 48.0kHz.<br />'

			audio_track['validate'] = (warning_icon, warning)
