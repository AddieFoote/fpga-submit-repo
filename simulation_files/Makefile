driver:
	iverilog -o drive run_drive.v clock.v ../real_robot/drive.v ../real_robot/control.v ../real_robot/pwm.v

run:
	vvp drive

clean:
	rm drive
