# Running the Code in Simulation

example command: `iverilog -o pwm <files.v> ` and `vvp pwm` OR you can use the make file from the top level directory(fpga-robot) 

top level drive: Make robot - Make run-robot
controller: Make drivecontrol - Make run-drivecontrol
drive: Make driver - Make run-driver


The results can be viewed in GTKwave by downloading the vcd file and opening it
*********the lines that must be commented out are already commented out in the submission files*********
For the image processing files, they're written in python, so you can just run it with python <name of file>
However, the pyparticle files and methods written to pass information to the IOT device must be commented out to run just the python code. To test the image processing on a video other than the default webcam, change the line `cap = cv2.VideoCapture(0)` to `cap=cv2.VideoCapture(<path to video in directory>)` so for example, I've included a video rgb_person.mp4 in the same directory so you could use `cap=cv2.VideoCapture('rgb_person.mp4)`
The same goes for the controller python file, lines `robot.writeMotor(write_string)` and any other lines with robot.writeMotor or robot.led must be commented out. I've included comments telling you exactly which lines.
 
# Running on Hardware
## Mechanical Stuff
3D print two of both of the stl files included, wheel.stl and servo.stl
Attach the hubs provided with the servos to wheels the with the provided screws
Cut a 12x12 piece of quarter inch plywood
Use wood screws to secure the 3D printed servo attachment in the corner with the square hole facing outwards 
use 8 1 inch 8-32 bolts and lock nuts to secure the servos to the attachment
Attach 2 small castor-type wheels to the front 
Secure the fpga board and electronics to the open space
## Electrical configuration
Connect the fpga to 12 V DC power
Power the particle photon board by connecting the 5 volt pin on the fpga to the VIN pin on the particle photon (on the fpga 6th down on the left side when the red button is oriented at the top left, on the photon the pin is labeled). Also connect ground to ground (right of 5V on fpga, labeled on photon)
Connect pins A0, A1, A2, A3, A4, A5 on the particle board to to 15, 17, 19, 21, 25 on the FPGA respectively. Also connect D0, D1, D2, D3, D4, D5 to 14, 16, 18, 20, 22.
Connect servos to 4.8-7 V power supply (red wire power, brown wire ground)
Connect GPIO pin 5 and 7 on the FPGA to left servo and right servo control signal (the orange wire) respectively
## Running code on the fpga
Install Quartus (Quartus Prime 22.1std)
Install the hardware driver for the usb blaster
On the off chance your computer has security restrictions like ours you may be able to download it on a different device, unzip it, change all the .dll files to .txt, rezip it, upload to one drive, download, unzip, change it back, rezip, and install
Open Quartus and click open project, select drive .qpf 
Double click compile design
Double click program device 
Select hardware setup and select USB blaster
Click auto detect
Click start
To run the pyparticle code
download the mobile app
Pip install pyparticleio
Create a particle account 
Create an access token
Add that in place of our access token
particle compile photon .
Plug photon into computer and press the button 
Run the following command substituting FPGA_Robot with the name given to your project and photon_firmware_1682006758610.bin with the result of compiling the .ino file
particle flash FPGA_Robot photon_firmware_1682006758610.bin

## Actually running it
Now the functions in the c++ code are on the photon so you can call them from python given you are connected, download other dependencies. For the GUI and vision 
Pip install PyQt5
Pip install numpy
Pip install opencv-python
Either run the controller or image file and use the GUI
python controller.py
python colorblob.py

NOTE: to switch between controller mode and image blob mode requires actual changes to the verilog. Change line 12 in drive.v to 1’b0 if it’s control mode and 1’b1 for image. To run, recompile and run it. The reason for this is because we intend to set a GPIO port on the Particle board and read it from the FPGA to control the mode so it is automatic, however the FPGA broke before we got to it, so we haven’t made this simple change yet.

