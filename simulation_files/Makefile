pwm:
	iverilog -o pwm pwm.v pwm_run.v
run:
	vvp pwm

driver:
	iverilog -o drive run_drive.v clock.v ../real_robot/drive.v ../real_robot/control.v ../real_robot/pwm.v

run-driver:
	vvp drive

clean:
	rm pwm control drive
