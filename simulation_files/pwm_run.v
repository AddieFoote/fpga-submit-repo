`timescale 1ns / 1ps
`define REG_LEN 20
`define MAX_DUTY 1000000

// fpga4student.com: FPGA Projects, Verilog projects, VHDL projects 
// Verilog project: Verilog testbench code for PWM Generator with variable duty cycle 
module tb_PWM_Generator_Verilog;
 // Inputs
 reg clk;
 reg val_en;
 reg [`REG_LEN:0]duty_val;
 reg increase_duty;
 reg decrease_duty;

 // Outputs
 wire PWM_OUT;
 // Instantiate the PWM Generator with variable duty cycle in Verilog
 PWM_Generator_Verilog PWM_Generator_Unit(
  .clk(clk), 
  .duty_val(duty_val),
  .val_en(val_en),
  .increase_duty(increase_duty), 
  .decrease_duty(decrease_duty), 
  .PWM_OUT(PWM_OUT)
 );

 // Create 100Mhz clock
 initial begin
    clk = 0;
    forever #5 clk = ~clk;
 end 

 initial begin
  increase_duty = 0;
  decrease_duty = 0;
  val_en = 0;

  #1000000; 
    increase_duty = 0;
  #1000000;// increase duty cycle by 10%
    increase_duty = 0;
  #1000000; 
    increase_duty = 1;
  #1000000;// increase duty cycle by 10%
    increase_duty = 0;
  #1000000; 
    increase_duty = 1;
  #1000000;// increase duty cycle by 10%
    increase_duty = 0;
  #1000000;
    val_en = 1;
    duty_val = 0.75 * `MAX_DUTY;
    decrease_duty = 1; 
  #1000000;//decrease duty cycle by 10%
    val_en = 0;
    decrease_duty = 0;
  #1000000; 
    decrease_duty = 1;
  #1000000;//decrease duty cycle by 10%
    val_en = 1;
    duty_val = 0.15 * `MAX_DUTY;
    decrease_duty = 1; 
  #1000000;
  val_en = 0;
    decrease_duty = 1;
  #1000000;//decrease duty cycle by 10%
    decrease_duty = 0;
 end
endmodule