#code used and modified from https://stackoverflow.com/questions/55876713/how-to-create-a-joystick-controller-widget-in-pyqt

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pyparticleio as pp
from pyparticleio.ParticleCloud import ParticleCloud

import sys
from enum import Enum
import secret

access_token = secret.access_token

particle_cloud = ParticleCloud(username_or_access_token=access_token)

all_devices = particle_cloud.devices
for device in all_devices:
    print("Device: {0}".format(device))

robot = all_devices["FPGA_Robot"]
print(robot)

class Direction(Enum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3

class Joystick(QWidget):
    def __init__(self, parent=None):
        super(Joystick, self).__init__(parent)
        self.setMinimumSize(200, 200)
        self.movingOffset = QPointF(0, 0)
        self.grabCenter = False
        self.__maxDistance = 100

    def paintEvent(self, event):
        painter = QPainter(self)
        bounds = QRectF(-self.__maxDistance, -self.__maxDistance, self.__maxDistance * 2, self.__maxDistance * 2).translated(self._center())
        painter.drawEllipse(bounds)
        painter.setBrush(Qt.black)
        painter.drawEllipse(self._centerEllipse())

    def _centerEllipse(self):
        if self.grabCenter:
            return QRectF(-20, -20, 40, 40).translated(self.movingOffset)
        return QRectF(-20, -20, 40, 40).translated(self._center())

    def _center(self):
        return QPointF(self.width()/2, self.height()/2)

    def _boundJoystick(self, point):
        limitLine = QLineF(self._center(), point)
        if (limitLine.length() > self.__maxDistance):
            limitLine.setLength(self.__maxDistance)
        return limitLine.p2()

    def joystickDirection(self):
        if not self.grabCenter:
            return 0
        normVector = QLineF(self._center(), self.movingOffset)
        xpos = self.movingOffset.x() - self._center().x()
        ypos = self._center().y() - self.movingOffset.y()
        x_6_bits = int((xpos + 100) * 63 / 200)
        y_6_bits = int((ypos + 100) * 63 / 200)
        #process bits to be writen to the particle board
        write_string_list = []
        for i in range(6):
            write_string_list.insert(0, "1" if x_6_bits % 2 == 1 else "0")
            x_6_bits //=2
        for i in range(6):
            write_string_list.insert(6, "1" if y_6_bits % 2 == 1 else "0")
            y_6_bits //=2
        write_string = ""
        for el in write_string_list:
            write_string += el
        robot.writeMotor(write_string)
        currentDistance = normVector.length()
        angle = normVector.angle()
        #HERE IS XPOS, YPOS, CURENT DISTANCE, AND ANGLE - we can use these to control our robot

        distance = min(currentDistance / self.__maxDistance, 1.0)
        if 45 <= angle < 135:
            return (Direction.Up, distance, angle)
        elif 135 <= angle < 225:
            return (Direction.Left, distance, angle)
        elif 225 <= angle < 315:
            return (Direction.Down, distance, angle)
        return (Direction.Right, distance, angle)


    def mousePressEvent(self, ev):
        self.grabCenter = self._centerEllipse().contains(ev.pos())
        return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, event):
        self.grabCenter = False
        self.movingOffset = QPointF(0, 0)
        self.update()

    def mouseMoveEvent(self, event):
        if self.grabCenter:
            self.movingOffset = self._boundJoystick(event.pos())
            self.update()
        self.joystickDirection() #gets the direction and writes it to the board

    def processMovement(self):
        values = self.joystickDirection()
        direction = values[0]
        speed = values[1]
        angle = values[2]

        left = direction == Direction.Left
        right = direction == Direction.Right

        finalSpeed = speed * 240
        leftMotor = 0
        rightMotor = 0

        if angle > 80 and angle <= 100:
            leftMotor = finalSpeed
            rightMotor = finalSpeed
        elif angle > 100 and angle <= 170:
            leftMotor = (1 - (angle - 90) / 80) * finalSpeed
            rightMotor = finalSpeed
        elif angle > 170 and angle <= 190:
            leftMotor = -0.5 * finalSpeed
            rightMotor = finalSpeed
        elif angle > 190 and angle <= 260:
            leftMotor = -1 * ((angle - 180) / 80) * finalSpeed
            rightMotor = -1 * finalSpeed
        elif angle > 260 and angle <= 280:
            leftMotor = -1 * finalSpeed
            rightMotor = -1 * finalSpeed
        elif angle > 280 and angle <= 350:
            leftMotor = -1 * finalSpeed
            rightMotor = -1 * (1 - ((angle - 270) / 80)) * finalSpeed
        elif angle > 350 or angle <= 10:
            leftMotor = finalSpeed
            rightMotor = -0.5 * finalSpeed
        else: # angle > 10 and angle <= 80
            leftMotor = finalSpeed
            rightMotor = (angle / 80) * finalSpeed
        return (leftMotor, rightMotor)

    def parse(self, values):
        left = int(values[0])
        right = int(values[1])

        leftSign = 0 if left > 0 else 1;
        rightSign = 0 if right > 0 else 1;
        leftBin = bin(abs(left)).replace("0b", "")
        rightBin = bin(abs(right)).replace("0b", "")

        leftBin = leftBin[0:-1]
        rightBin = rightBin[0:-1]
        while (len(leftBin) < 7):
            leftBin = "0" + leftBin

        while (len(rightBin) < 7):
            rightBin = "0" + rightBin

        leftBin = str(leftSign) + leftBin
        rightBin = str(rightSign) + rightBin

        return leftBin + rightBin


if __name__ == '__main__':
    # Create main application window
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Cleanlooks"))
    mw = QMainWindow()
    mw.setWindowTitle('Joystick example')

    # Create and set widget layout
    # Main widget container
    cw = QWidget()
    ml = QGridLayout()
    cw.setLayout(ml)
    mw.setCentralWidget(cw)

    # Create joystick 
    joystick = Joystick()
    ml.addWidget(joystick,0,0)

    mw.show()

    ## Start Qt event loop unless running in interactive mode or using pyside.
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QApplication.instance().exec_()
