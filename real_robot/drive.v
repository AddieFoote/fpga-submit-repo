module drive(
	input wire clk,
	//input wire image_mode,
	input wire[32'd5: 32'd0] input_0,
	input wire[32'd5: 32'd0] input_1,
	//input wire power,
	output wire PWM_OUT_0,
	output wire PWM_OUT_1
	);

/* UNCOMMENT FOR SIMULATION
initial begin
    $dumpfile("drive.vcd");
    $dumpvars(0, drive);
end*/

wire power = 1'b0;
wire image_mode = 1'b0;

wire servo_0_speed_write_en;
wire servo_1_speed_write_en;
wire [32'd7: 32'd0]servo_0_speed;
wire [32'd7: 32'd0]servo_1_speed;
wire [32'd2: 32'd0]servo_0_step;
wire [32'd2: 32'd0]servo_1_step;
control robot(clk,
	servo_0_speed_write_en,
	servo_1_speed_write_en,
	servo_0_speed,
	servo_1_speed,
	servo_0_step,
	servo_1_step,
	PWM_OUT_0,
	PWM_OUT_1
);

reg reg_servo_0_speed_write_en;
reg reg_servo_1_speed_write_en;
reg [32'd7: 32'd0]reg_servo_0_speed;
reg [32'd7: 32'd0]reg_servo_1_speed;
reg [32'd2: 32'd0]reg_servo_0_step;
reg [32'd2: 32'd0]reg_servo_1_step;

assign servo_0_speed_write_en = reg_servo_0_speed_write_en;
assign servo_1_speed_write_en = reg_servo_1_speed_write_en;
assign servo_0_speed = reg_servo_0_speed;
assign servo_1_speed = reg_servo_1_speed;
assign servo_0_step = reg_servo_0_step;
assign servo_1_step = reg_servo_1_step;

initial begin
	reg_servo_0_speed_write_en <= 1'b1;
	reg_servo_1_speed_write_en <= 1'b1;
	reg_servo_0_speed <= 8'd140; 
	reg_servo_1_speed <= 8'd116; // rotate slowly
end

always @(posedge clk) begin
	if (image_mode) begin //image mode
		reg_servo_0_speed_write_en <= 1'b0; //no writing speed (only increment)
		reg_servo_1_speed_write_en <= 1'b0;
		
		if (input_0 !== 6'd0) begin // continue at current if there is no object
			reg_servo_0_step <= input_0[32'd5:32'd3]; //step based on the most significant bits of the x position in the frame
			reg_servo_1_step <= 3'd7 - input_0[32'd5:32'd3]; 
		end 
	end else begin //drive control mode
		reg_servo_0_speed_write_en <= 1'b1;
		reg_servo_1_speed_write_en <= 1'b1;
		reg_servo_0_speed <= (8'd4 * input_1) + (8'd1 * input_0 - 8'd31); 
		//if we think about it with negatives this means speed = 4x + y for one wheel
		// and 4x - y for the other. Ei at y = 100, x = 0 it will go full forward, 
		// at y = -100, x = 0, full back. y = 0, x = 100 full turn right etc
		reg_servo_1_speed <= (8'd4 * input_1) - (8'd1 * input_0 - 8'd31);
	end
	
	if (~power) begin //if power is off stop servos
		reg_servo_0_speed_write_en <= 1'b1;
		reg_servo_1_speed_write_en <= 1'b1;
		reg_servo_0_speed <= 8'd128;
		reg_servo_1_speed <= 8'd128;
		reg_servo_0_step <= 3'd0;
		reg_servo_1_step <= 3'd0;
		
	end
	
end

endmodule