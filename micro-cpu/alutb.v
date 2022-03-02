module MCPU_Alutb();

parameter CMD_SIZE=2;
parameter WORD_SIZE=2;

parameter  [CMD_SIZE-1:0]  CMD_AND  = 0; //2'b00
parameter  [CMD_SIZE-1:0]  CMD_OR   = 1; //2'b01
parameter  [CMD_SIZE-1:0]  CMD_XOR   = 2; //2'b10
parameter  [CMD_SIZE-1:0]  CMD_ADD   = 3; //2'b11

reg is_correct;

reg [CMD_SIZE-1:0] opcode;
reg [WORD_SIZE-1:0] r1;
reg [WORD_SIZE-1:0] r2;
wire [WORD_SIZE-1:0] out;
wire OVERFLOW;

MCPU_Alu #(.CMD_SIZE(CMD_SIZE), .WORD_SIZE(WORD_SIZE)) aluinst (opcode, r1, r2, out, OVERFLOW);

// Testbench code goes here
always #4 r1[0] = $random;
always #4 r2[0] = $random;
always #4 r1[1] = $random;
always #4 r2[1] = $random;

always #4 opcode[0] = $random;
always #4 opcode[1] = $random;

initial begin
  $display("@%0dns default is selected, opcode %b",$time,opcode);
end

always begin 
  #1
  case (opcode)
    CMD_AND : begin
      is_correct = ((r1&r2) == out);
    end
    CMD_OR : begin
      is_correct = ((r1|r2) == out);
    end
    CMD_XOR : begin
      is_correct = ((r1^r2) == out);
    end
    CMD_ADD : begin
      is_correct = ((r1+r2) == out);
    end
    default : begin
      is_correct = 1'bx;
    end
  endcase
end

endmodule
