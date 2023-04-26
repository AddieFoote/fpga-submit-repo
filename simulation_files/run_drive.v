module run_drive();

wire clk;
clock the_clock(clk);
wire[32'd5: 32'd0] input_0 = 6'd0; //change these to test different options
wire[32'd5: 32'd0] input_1 = 6'd0;
wire PWM_OUT_0;
wire PWM_OUT_1;

drive driver(clk, input_0, input_1, PWM_OUT_0, PWM_OUT_1);


/* UNCOMMENT FOR THIS FILE TO BE SIMULATED*/
initial begin
    $dumpfile("run_drive.vcd");
    $dumpvars(0, run_drive);
end

reg [31:0] counter = 0;

always @(posedge clk) begin
    counter <= counter + 1;
    //YOU CAN ADD STUFF IN HERE TO TEST CHANGING INPUTS AT CERTAIN TIMES
    if (counter >= 100000) begin //INCREASE OR DECREASE CYCLES IT RUNS FOR
        $finish;
    end
end 

 

endmodule