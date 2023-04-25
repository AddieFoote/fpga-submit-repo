`define MIN_DUTY 32'd1
`define REG_LEN 32'd31

module PWM_Generator
 (
    input wire clk, // 50MHz clock input 
    input wire [32'd31:32'd0] duty_val, //out will be 1 this amount of clock cycles
    input wire val_en, // write duty value enable
	 input wire[31:0] MAX_DUTY, //cycle will last this many clock cycles
    output wire PWM_OUT //out wire
);

 reg[`REG_LEN:0] counter_PWM;
 reg[`REG_LEN:0] reg_duty;
  
initial begin 
	counter_PWM = 32'd0;
end
   
reg reg_PMW_OUT;
assign PWM_OUT = reg_PMW_OUT;

always @(posedge clk) begin
   if (val_en)
       reg_duty <= duty_val; //update duty_val - corresponding to the duty cycle
	reg_PMW_OUT <= counter_PWM < reg_duty; //PWM_OUT is on for the portion of the cycle
//	that the counter is less than duty value and off for the rest

   counter_PWM <= counter_PWM + 32'b1; //increment counter
   if(counter_PWM >= MAX_DUTY) 
       counter_PWM <= 32'b0; //cycle starts over once it gets to the max
end

endmodule
