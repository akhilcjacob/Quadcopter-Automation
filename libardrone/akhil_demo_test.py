#!/usr/bin/env python
minWid=40  #This is the min width of the tracked object(also helps remove bad data)
objSize=150 #target object size in pixels
Width,Height=1,1 # This is the width and height of the window
lower_threshold=230 #This is the lower threshold of a greyscaled image
upper_threshold=255 #this is the upper threshold of a greyscaled image
#higher the number lighter the color (255=White) (0=Black)
x,y,w,h=210,100,180,180 #This is the value for the "do nothing" zone
tolerance,ratTolerence=0.3,0.3 #tolerance-area of perfect square vs square blob
stringOrNot=False#controls whether or not the drone should actually takeoff
#true-for string only false-for string and actual drone movement
computer_camera_in_use=False #controls whether to use computer camera or drone camera
t=0  #time variable that controls how long the drone should move in each direction
#keep 0 unless drone doesn’t move enough.
circleObject=False #if square object to be tracked keep false else if circle obj make true
import pygame
import pygame.surfarray
import pygame.transform
print("PYGAME IMPORT: SUCCESSFUL")
from SimpleCV import *
import SimpleCV as sc
print("SIMPLECV IMPORT: SUCCESSFUL")
import libardrone
print("LIBARDRONE IMPORT: SUCCESSFUL")
import time
display = sc.Display()
drone = libardrone.ARDrone(True)
time.sleep(1)
drone.reset()
print("Hit 'esc' to exit")
if not(stringOrNot):
    time.sleep(1)
    drone.takeoff()
    drone.move_up()
    time.sleep(0.5)
if computer_camera_in_use:
    cam = Camera()
def main():
    while display.isNotDone():
        try:
            image = get_image()
            image = image_proc(image)
            image = blob_track(image)
            display_image(image)
        except Exception,e:
            print str(e)
            drone.land()
            drone.halt()
            pass
    print("Shutting down...")
    drone.land()
    drone.halt()
    print("Ok.")
    
    
########################################################################
def get_image():
    if computer_camera_in_use:
             return cam.getImage()
    else:
            return Image(drone.get_image()).rotate270().flipHorizontal()
            
def image_proc(img):
    img=img.colorDistance(sc.Color.BLACK).stretch(lower_threshold,upper_threshold)
    img.drawRectangle(x,y,w,h,(0, 255, 0), 0, alpha=120)
    img.drawText( (str(drone.navdata.get(0, dict()).get('battery', 0))+ '% Battery'), 0, 200, color=Color.BLUE) 
    return img

def blob_track(img):
    img.findBlobs()
    if blobs:
            if circleObject:
                objects=blobs.filter([b.isCircle(tolerance,ratTolerence) for b in blobs])
            else:
                objects= blobs.filter([b.isSquare(tolerance,ratTolerence) for b in blobs])
            if objects:
                if objects[-1].height()>minWid:
                    img.drawCircle((objects[-1].x,objects[-1].y),objects[-1].height()/2,SimpleCV.Color.BLUE,3)
                    drone_action(img,objects,stringOrNot)
                    img.drawText(str(objects[-1].height()), 0, 140, color=Color.BLUE)
            return img
            else:
                if not stringOrNot:
                    drone.hover()
                    img.drawText("SPIN", 0, 140, color=Color.BLUE) 
                else: 
                    img.drawText("SPIN", 0, 140, color=Color.BLUE) 

def drone_action(img,sq,string=True):
    try:
        
        if string:
            if(sq[-1].x>x & sq[-1].x<x+w  & sq[-1].y>y+h & sq[-1].y<y):
                img.drawText("HOVER", 0, 30, color=Color.RED) 
            if(sq[-1].x>x+h):
               img.drawText("RIGHT", 0, 50, color=Color.RED) 
            if(sq[-1].x<x):
                img.drawText("LEFT", 0, 70, color=Color.RED) 
            if(sq[-1].y<y):
                img.drawText("UP", 0, 90, color=Color.RED) 
            if(sq[-1].y>y+h):
                img.drawText("DOWN", 0, 110, color=Color.RED) 
            if(sq[-1].height()>objSize+15):
                img.drawText("BACKWARD", 0, 10, color=Color.GREEN) 
            if(sq[-1].height()<objSize-15):
                img.drawText("FORWARD", 0, 10, color=Color.GREEN) 
        else:
            if(sq[-1].x>x & sq[-1].x<x+w  & sq[-1].y>y+h & sq[-1].y<y):
                drone.hover()
                img.drawText("HOVER", 0, 30, color=Color.RED) 
            if(sq[-1].x>x+h):
                drone.move_right()
                time.sleep(t)
                img.drawText("RIGHT", 0, 50, color=Color.RED) 
            if(sq[-1].x<x):
                drone.move_left()
                time.sleep(t)
                img.drawText("LEFT", 0, 70, color=Color.RED) 
            if(sq[-1].y<y):
                drone.move_up()
                time.sleep(t)
                img.drawText("UP", 0, 90, color=Color.RED) 
            if(sq[-1].y>y+h):
                drone.move_down()
                time.sleep(t)
                img.drawText("DOWN", 0, 110, color=Color.RED) 
            if(sq[-1].height()>objSize+15):
                drone.move_backward()
                time.sleep(t)
                img.drawText("BACKWARD", 0, 10, color=Color.GREEN) 
            if(sq[-1].height()<objSize-15):
                drone.move_forward()
                time.sleep(t)
                img.drawText("FORWARD", 0, 10, color=Color.GREEN) 
    except Exception,e:
        drone.land()
        drone.halt()
        print str(e)
        pass
    
def display_image(img):
     normaldisplay=True
            if normaldisplay:
                img.show()
            else:
                segmented.show()
#######################################################################

if __name__ == '__main__':
    main()
