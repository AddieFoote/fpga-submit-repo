import cv2
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pyparticleio as pp
from pyparticleio.ParticleCloud import ParticleCloud

import sys

access_token = "16c3743048694b2a1776e62169f6597a897ec6b4"

particle_cloud = ParticleCloud(username_or_access_token=access_token)

all_devices = particle_cloud.devices
for device in all_devices:
    print("Device: {0}".format(device))

robot = all_devices["FPGA_Robot"]

class ColorDetection:

    def __init__(self, color):
        self.color = color

    def find_obj(self, frame, chan_1, chan_2): 
        filtered = cv2.subtract(chan_1, chan_2) 

        ret, thresh = cv2.threshold(filtered, 60, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel1)

        # get all contours
        cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # find max contour and assume to be the object
        if len(cnts) > 0:
            x, y, w, h = cv2.boundingRect(cnts[0])
            
            x_coord = (x + w) / 2
            b_mask = np.zeros(frame.shape)
            b_mask = cv2.drawContours(b_mask, cnts, 0, 255, cv2.FILLED) #get biggest contour

            # return the mask of the object(demo display) and the x-coordinate of the middle of the object for bit-processing
            return x_coord, b_mask
        return 0, 0

    def detection(self):
        cap = cv2.VideoCapture('rgb_person.mp4') 
        while True: # allows you to click through frames
            ret, frame_og = cap.read()
            if not ret:
                break # not a normal frame
            dim = (64, 64)
            frame = cv2.resize(frame_og, dim)
            b,g,r = cv2.split(frame)

            chan1, chan2 = b, g
            if self.color == 'red':
                chan1 = g
                chan2 = r
            elif self.color == 'blue':
                chan1 = b
                chan2 = g
            else:
                chan1 = r
                chan2 = b

            x_coord, mask = self.find_obj(frame, chan1, chan2)
            x_6_bits = abs(x_coord)
            # convert to bitstring
            write_string_list = []
            for i in range(6):
                write_string_list.insert(1, "1" if x_6_bits % 2 == 1 else "0")
                x_6_bits //=2

            # print(write_string_list)

            write_string = ""
            for el in write_string_list:
                write_string += el
            
            print(write_string)

            '''
                this line is meant to pass information to the IOT board, comment out for simulation
            '''
            # robot.writeMotor(write_string)

            '''
                blue = b, g
                green = r, b
                red = g, r
            '''
            if (mask.any() == 0):
                cv2.imshow("img", frame)
            else:
                cv2.imshow("img", mask)

            # process into bits and send to particle

            key = cv2.waitKey(0) # key = cv2.waitKey(1) no clicks
            if key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

class Buttons(QWidget):
    def __init__(self):
        super().__init__()
 
        # setting title
        self.setWindowTitle("Color Select ")
 
        # setting geometry
        self.setGeometry(100, 100, 600, 400)
 
        # calling method
        self.UiComponents()
 
        # showing all the widgets
        self.show()
 
    # method for widgets
    def UiComponents(self):
 
        # creating a push button
        red = QPushButton("Red", self)
        blue = QPushButton("Blue", self)
        green = QPushButton("Green", self)
 
        # setting geometry of button
        red.setGeometry(200, 150, 100, 30)
        blue.setGeometry(200, 200, 100, 30)
        green.setGeometry(200, 250, 100, 30)
 
        # adding action to a button
        red.clicked.connect(lambda: self.clickme('red'))
        blue.clicked.connect(lambda: self.clickme('blue'))
        green.clicked.connect(lambda: self.clickme('green'))

        # button color
        red.setStyleSheet("background-color : red")
        blue.setStyleSheet("background-color : blue")
        green.setStyleSheet("background-color : green")
 
    # action methods
    def clickme(self, button):
        new_run = ColorDetection(button)
        new_run.detection()
        

if __name__ == '__main__':
    '''
        this line is meant to pass information to the IOT board, comment out for simulation
    '''
    # robot.mode('color')
    # Create main application window
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Cleanlooks"))
    mw = QMainWindow()
    mw.setWindowTitle('Buttons GUI')

    # Create and set widget layout
    # Main widget container
    cw = QWidget()
    ml = QGridLayout()
    cw.setLayout(ml)
    mw.setCentralWidget(cw)

    # Create button 
    button = Buttons()

    ml.addWidget(button,0,0)

    mw.show()

    ## Start Qt event loop unless running in interactive mode or using pyside.
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QApplication.instance().exec_()

# def find_all_obj() {
#     vector<cv::Vec4i> hierarchy;

#     Mat mask = cv::Mat::zeros(_frame.rows, _frame.cols, CV_8UC1);
#     bitwise_or(rMask, gMask, mask);
#     bitwise_or(mask, bMask, mask);

#     Mat allCups;
#     _frame.copyTo(allCups, mask);
#     // Problem 6: ALL THREE
#     imshow("VideoDisplay", allCups);
# }