//import pwm.v
`define MAX_DUTY 32'd9999985 

module control(
	input wire clk,
	input wire servo_0_speed_write_en,
	input wire servo_1_speed_write_en,
	input wire[32'd7: 32'd0] servo_0_speed,
	input wire[32'd7: 32'd0] servo_1_speed,
	input wire[32'd2: 32'd0] servo_0_step,
	input wire[32'd2: 32'd0] servo_1_step,
	output wire PWM_OUT_0,
	output wire PWM_OUT_1
);

wire[32'd31: 32'd0] servo_0_duty_val;
wire[32'd31: 32'd0] servo_1_duty_val;
wire servo_0_val_en;
wire servo_1_val_en;
PWM_Generator servo_0 (clk, servo_0_duty_val, servo_0_val_en, 32'd999985, PWM_OUT_0); //PWM Generator for servos
PWM_Generator servo_1 (clk, servo_1_duty_val, servo_1_val_en, 32'd999980, PWM_OUT_1);
wire[32'd7: 32'd0] neg_servo_1_speed = 8'd255 - servo_1_speed;

reg [32'd31: 32'd0]counter = 0;

reg reg_servo_1_en;
reg reg_servo_0_en;
assign servo_0_val_en = reg_servo_0_en;
assign servo_1_val_en = reg_servo_1_en;

initial begin
	reg_servo_0_en <= 1'b1;
	reg_servo_1_en <= 1'b1;
end

reg[32'd31: 32'd0] reg_servo_0_duty;
reg[32'd31: 32'd0] reg_servo_1_duty;
assign servo_0_duty_val = reg_servo_0_duty;
assign servo_1_duty_val = reg_servo_1_duty;

always @(posedge clk) begin
		reg_servo_0_duty <= 
								servo_0_speed_write_en ? 
				32'd50000 + (servo_0_speed * 32'd50000/32'd256) : 
				(reg_servo_0_duty - 32'd781 + ((servo_0_step * 32'd50000)/32'd256)  > `MAX_DUTY/32'd10) ? 
								`MAX_DUTY/32'd10 :
								(servo_0_speed_write_en ?
				32'd50000 + ((servo_0_speed * 32'd50000)/32'd256) :
				(reg_servo_0_duty - 32'd781 + ((servo_0_step * 32'd50000)/32'd256) ) < `MAX_DUTY/32'd20) ? 
								`MAX_DUTY/32'd20 : 
								(servo_0_speed_write_en ?
				32'd50000 + ((servo_0_speed * 32'd50000)/32'd256) : counter == 1'b0 ?
				reg_servo_0_duty - 32'd781 + ((servo_0_step * 32'd50000)/32'd256) :
				reg_servo_0_duty);
				//set servo based on write enable, specified speed, or step size if not write enable
		
		reg_servo_1_duty <= 
								servo_1_speed_write_en ? 
				32'd50000 + (neg_servo_1_speed * 32'd50000/256) : 
				(reg_servo_1_duty - 32'd781 + ((servo_1_step * 32'd50000)/256)  > `MAX_DUTY/32'd10) ? 
								`MAX_DUTY/32'd10 :
								(servo_1_speed_write_en ?
				32'd50000 + ((neg_servo_1_speed * 32'd50000)/256) :
				(reg_servo_1_duty - 32'd781 + ((servo_1_step * 32'd50000)/256) ) < `MAX_DUTY/32'd20) ? 
								`MAX_DUTY/32'd20 : 
								(servo_1_speed_write_en ?
				32'd50000 + ((neg_servo_1_speed * 32'd50000)/256) : counter == 1'b0 ?
				reg_servo_1_duty - 32'd781 + ((servo_1_step * 32'd50000)/256) :
				reg_servo_1_duty);

	
	
	counter <= counter + 32'd1;
	
	if (counter >= `MAX_DUTY) begin
		counter <= 1'b0;
	end
end

endmodule