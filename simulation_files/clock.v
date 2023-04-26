/* clock */
`timescale 1ps/1ps
module clock(output wire clk);
    reg theClock = 1;

    assign clk = theClock;
    
    always begin
        #1;
        theClock = !theClock;
    end
endmodule
