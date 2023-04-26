`include "../real_robot/drive.v"
`include "clock.v"

module run_drive();

wire clk;
clock = clock(clk);
wire[32'd5: 32'd0] input_0 = 6'd0; //change these to test different options
wire[32'd5: 32'd0] input_1 = 6'd0;
wire PWM_OUT_0;
wire PWM_OUT_1;

drive = drive(clk, input_0, input_1, PWM_OUT_0, PWM_OUT_1);


/* UNCOMMENT FOR THIS FILE TO BE SIMULATED
initial begin
    $dumpfile("drive.vcd");
    $dumpvars(0, run_drive);
end*/