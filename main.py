# importing libraries
import cv2
import numpy as np


import sys
import os
import os.path
from pygame.locals import *
import configparser
import QLabController
import ast
import time
import cv2
import numpy as np
#import serial
from omxplayer.player import OMXPlayer
from time import sleep

# Set the port name and the baud rate. This baud rate should match the
# baud rate set on the Arduino.
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)


class Induction:

    # Class constructor
    def __init__(self):
        
      # Load window info from config file (config.ini)
      config = configparser.ConfigParser()
      config.read('config.ini')

      self.window = "Induction"
      cv2.namedWindow(self.window, cv2.WND_PROP_AUTOSIZE)

      self.movie_path = config['assets']['movie']
      self.wallpaper_paper = config['assets']['wallpaper']
      self.wallpaper = cv2.imread("assets/wallpaper.jpeg")
      self.wallpaper = cv2.resize(self.wallpaper, dsize=(1920,1080))

      # Create a VideoCapture object and read from input file
      self.video = cv2.VideoCapture('assets/AUTOLEGEND.mp4')
      self.playing = False

      # QLAB Controller
      port = int(config['QLab']['port'])
      ip_qlab = config['QLab']['ip_qlab']
      ip_device = config['QLab']['ip_device']
      self.QLAB = QLabController.QLabController(ip_qlab, port, ip_device)

    def reset_video(self):
      self.playing = False
      self.display_wallpaper()
      self.QLAB.recv_msg = ""
    
    def play_video(self):
      self.playing = True

    def display_wallpaper(self):
      cv2.imshow(self.window, induction.wallpaper)
      while cv2.waitKey(1):
        if self.QLAB.recv_msg == "play_video":
          self.play_video()
          return
        elif induction.QLAB.recv_msg == "quit_video":
            exit()
                        
     


# start execution
if __name__ == '__main__':
  
  induction = Induction()

  # Check if camera opened successfully
  if (induction.video.isOpened()== False): 
    print("Error opening video  file")
  
  #cv2.imshow(induction.window, induction.wallpaper

  induction.display_wallpaper()
      

  # Read until video is completed
  while(True):
    
    #check for received QLab commands
    if induction.QLAB.recv_msg == "play_video":
        induction.play_video()
        player = OMXPlayer(induction.movie_path)
        while(True):
           try:
              stat = player.playback_status()
           except:
              break
        player.quit()
        induction.reset_video()
    elif induction.QLAB.recv_msg == "reset_video":
        induction.reset_video()
    elif induction.QLAB.recv_msg == "quit_video":
        exit()
                        


    # Capture frame-by-frame
#    ret, frame = induction.video.read()
#    if ret == True and induction.playing:
#      frame = cv2.resize(frame, dsize=(1920,1080))
      # Display the resulting frame
#      cv2.imshow(induction.window, frame)

      # Press Q on keyboard to  exit
#      if cv2.waitKey(25) & 0xFF == ord('q'):
#        exit()

      

    # frame rate limit
 # clock.tick(60)

  # When everything done, release 
  # the video capture object
  induction.video.release()


    


