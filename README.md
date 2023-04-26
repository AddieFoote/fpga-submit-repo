# Running the Code in Simulation

## Verilog
### Simulate entire control
1. uncomment import statements and vcd dump statements from verilog code in simulation_files and real_robot
2. from the simulation_files directory, run `make driver` then `make run` in simulation_files directory
3. open the vcd file in GTKwave
4. if desired, change the inputs in the run_drive.v file, also can change them based on the clock to see dynamic change
5. additionally, change the mode in drive.v


## Control/Image Processing Files
For the image processing files, they're written in python, so you can just run it with `python <name of file>`. However, the pyparticle files and methods written to pass information to the IOT device must be commented out to run just the python code. To test the image processing on a video other than the default webcam, change the line `cap = cv2.VideoCapture(0)` to `cap=cv2.VideoCapture(<path to video in directory>)` so for example, I've included a video rgb_person.mp4 in the same directory so you could use `cap=cv2.VideoCapture('rgb_person.mp4)`
The same goes for the controller python file, lines `robot.writeMotor(write_string)` and any other lines with `robot.writeMotor`, `robot.led`, or any addtional pyparticle functions using the `robot` object must be commented out. I've included comments telling you exactly which lines.
 
# Running on Hardware
## Mechanical Stuff
1. 3D print two of the stl files in STL_files, wheel.stl and servo_mount.stl
2. Attach the hubs provided with the servos to wheels the with the provided screws
3. Cut a 12x12 piece of quarter inch plywood
4. Use wood screws to secure the 3D printed servo attachment in the corner with the square hole facing outwards 
5. use 8 1 inch 8-32 bolts and lock nuts to secure the servos to the attachment
6. attach wheels to servo: pressfit with the hubs and servos and add the provided bolt
7. Attach 2 small castor-type wheels to the front 
8. Secure the fpga board and electronics to the open space

## Electrical configuration
1. Connect the fpga to 12 V DC power
2. Power the particle photon board by connecting the 5 volt pin on the fpga to the VIN pin on the particle photon (on the fpga 6th down on the left side when the red button is oriented at the top left, on the photon the pin is labeled). Also connect ground to ground (right of 5V on fpga, labeled on photon)
3. Connect pins A0, A1, A2, A3, A4, A5 on the particle board to to 15, 17, 19, 21, 25 on the FPGA respectively. Also connect D0, D1, D2, D3, D4, D5 to 14, 16, 18, 20, 22.
4. Connect servos to 4.8-7 V power supply (red wire power, brown wire ground)
5. Connect GPIO pin 5 and 7 on the FPGA to left servo and right servo control signal (the orange wire) respectively

## Particle Photon Board Setup
1. download the mobile app
2. run `Pip install pyparticleio`
3. Create a particle account 
4. Create an access token
5. Create a file for the access token: image_prc/secret.py and write 1 line `access_token = "put your access token here"`
6. run `particle compile photon .`
7. Plug photon into computer and press the button 
8. Run `particle flash FPGA_Robot photon_firmware_1682006758610.bin` substituting FPGA_Robot with the name given to your project and photon_firmware_1682006758610.bin with the result of compiling the .ino file 

## FPGA setup
1. Install Quartus (Quartus Prime 22.1std)
2. Install the hardware driver for the usb blaster
   * On the off chance your computer has security restrictions like ours you may be able to download it on a different device, unzip it, change all the .dll files to .txt, rezip it, upload to one drive, download, unzip, change it back, rezip, and install
3. Open Quartus and click open project, select drive .qpf 
4. Double click compile design
5. Double click program device 
6. Select hardware setup and select USB blaster
7. Click auto detect
8. Click start

## Putting it all together
1. Now the functions in the c++ code are on the photon so you can call them from python given you are connected, download other dependencies. For the GUI and vision 
2. `Pip install PyQt5`
3. `Pip install numpy`
4. `Pip install opencv-python`
5. Either run the controller or image file and use the GUI
   1. `python controller.py`
   2. `python colorblob.py`

NOTE: to switch between controller mode and image blob mode requires actual changes to the verilog. Change line 12 in drive.v to 1’b0 if it’s control mode and 1’b1 for image. To run, recompile and run it. The reason for this is because we intend to set a GPIO port on the Particle board and read it from the FPGA to control the mode so it is automatic, however the FPGA broke before we got to it, so we haven’t made this simple change yet.

