#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wakeup2.py
#  
#  Copyright 2018 Thomas Breitbach <tbeitbach@Thomass-MacBook-Pro.local>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys
import getopt
import time
import pigpio

# START CONFIG

MAX_BRIGHTNESS = 255.0

# The Color
DESIRED_COLORS = [255, 70, 0]	# order: RGB

# The Pins. Use Broadcom numbers.
RED_PIN   	= 17
GREEN_PIN 	= 22
BLUE_PIN 	= 24
PINS = [RED_PIN, GREEN_PIN, BLUE_PIN]	# order: RGB

WAKE_UP_DURATION_IN_SECS 	= 30 * 60 	# 30 minutes

# END CONFIG

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hd:r:g:b:")
	except getopt.GetoptError:
		print 'usage: wakeup2.py -d <durationInSeconds> -r <red> -g <green> -b <blue>'
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print 'usage: wakeup2.py -d <durationInSeconds> -r <red> -g <green> -b <blue>'
			sys.exit(2)
		elif opt in ("-d"):
			WAKE_UP_DURATION_IN_SECS = int(arg)
		elif opt in ("-r"):
			DESIRED_COLORS[0] = float(arg)
		elif opt in ("-g"):
			DESIRED_COLORS[1] = float(arg)
		elif opt in ("-b"):
			DESIRED_COLORS[2] = float(arg)
			
	INCREMENT = MAX_BRIGHTNESS / WAKE_UP_DURATION_IN_SECS	
		
	pi = pigpio.pi()
	curColors = [0, 0, 0] # order: rgb
	curBrightness = 0

	print '\n---- START ----'
	print 'Desired Color [RGB]:\t' , (DESIRED_COLORS)
	print 'Duration [s]:\t\t' , WAKE_UP_DURATION_IN_SECS
	print 'Calc. Increment:\t' , INCREMENT
	print 'Current Brightness [%]: ' , curBrightness * 100.0 / MAX_BRIGHTNESS
	print '\n'

	# reset brightness for each color/pin
	for index in range(len(curColors)) :
		curColors[index] = curBrightness
        pi.set_PWM_dutycycle(PINS[index], curColors[index])
        
	desiredColorsFraction = [0.0, 0.0, 0.0];        
	for index in range(len(DESIRED_COLORS)) :      
		desiredColorsFraction[index] = DESIRED_COLORS[index] / MAX_BRIGHTNESS    
        
	# start sunrise simulation       
	while (curBrightness < MAX_BRIGHTNESS) :
		curBrightness += INCREMENT
	
		# set new brightness for each color/pin
		for index in range(len(curColors)) :
			curColors[index] = curBrightness * desiredColorsFraction[index]
			pi.set_PWM_dutycycle(PINS[index], curColors[index])
		
		print 'Current Brightness [%]: ' , curBrightness * 100.0 / MAX_BRIGHTNESS
		# print 'Current Colors: ' , (curColors)
		
		time.sleep(1)
	return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
