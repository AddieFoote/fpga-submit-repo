import pyparticleio as pp
import sys
from pyparticleio.ParticleCloud import ParticleCloud

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import secret

from controller import Joystick

access_token = secret.access_token

particle_cloud = ParticleCloud(username_or_access_token=access_token)

all_devices = particle_cloud.devices
for device in all_devices:
    print("Device: {0}".format(device))

robot = all_devices["FPGA_Robot"]
print(robot)