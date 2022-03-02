module shift_tb();
  
reg reset, clk;


MCPU cpuinst (clk, reset);


initial begin
  reset=1;
  #10  reset=0;
end

always begin
  #5 clk=0; 
  #5 clk=1; 
end
  
/* pseudo-assembler */
parameter  [cpuinst.OPERAND_SIZE-1:0]  R0  = 0; //4'b0000
parameter  [cpuinst.OPERAND_SIZE-1:0]  R1  = 1; //4'b0001
parameter  [cpuinst.OPERAND_SIZE-1:0]  R2  = 2; //4'b0010
parameter  [cpuinst.OPERAND_SIZE-1:0]  R3  = 3; //4'b0011
parameter  [cpuinst.OPERAND_SIZE-1:0]  R4  = 4; //4'b0100
parameter  [cpuinst.OPERAND_SIZE-1:0]  R5  = 5; //4'b0101
parameter  [cpuinst.OPERAND_SIZE-1:0]  R6  = 6; //4'b0110
parameter  [cpuinst.OPERAND_SIZE-1:0]  R7  = 7; //4'b0111
parameter  [cpuinst.OPERAND_SIZE-1:0]  R8  = 8; //4'b1000
parameter  [cpuinst.OPERAND_SIZE-1:0]  R9  = 9; //4'b1001
parameter  [cpuinst.OPERAND_SIZE-1:0]  R10  = 10; //4'b1010
parameter  [cpuinst.OPERAND_SIZE-1:0]  R11  = 11; //4'b1011
parameter  [cpuinst.OPERAND_SIZE-1:0]  R12  = 12; //4'b1100
parameter  [cpuinst.OPERAND_SIZE-1:0]  R13 = 13; //4'b1101
parameter  [cpuinst.OPERAND_SIZE-1:0]  R14 = 14; //4'b1110
parameter  [cpuinst.OPERAND_SIZE-1:0]  R15  = 15; //4'b1111

integer i;

initial begin
  /* initialize mem to 0 */
  for(i=0; i<cpuinst.raminst.RAM_SIZE; i=i+1) begin
    cpuinst.raminst.mem[i] = 0;
  end

  /* initialize regs to 0 */
  for(i=0; i<cpuinst.regfileinst.REGISTERS_NUMBER; i=i+1) begin
    cpuinst.regfileinst.R[i] = 0;
  end
    
    
  /* instructions */
  
  /* load AM */
  i=0;  cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R14, 8'b00011010};   //0: R14 = 26;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R15, 8'b00101001};  //1: R15 = 41;
  
  /* load constants 1,2,3,4 to regs */
  i=i+1;  cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R0, 8'd1};   //2: R0 = 1;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R1, 8'd2};    //3: R1 = 2;
  i=i+1;  cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R2, 8'd3};   //4: R2 = 3;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R3, 8'd4};    //5: R3 = 4;
  
  /* LSL 26 */
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSL, R13, R14, R0};           //6: R13 = R14 << R0;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSL, R13, R14, R1};           //7: R13 = R14 << R1;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSL, R13, R14, R2};           //8: R13 = R14 << R2;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSL, R13, R14, R3};           //9: R13 = R14 << R3;
  
  /* LSL 41 */
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSL, R12, R15, R0};           //10: R12 = R15 << R0;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSL, R12, R15, R1};           //11: R12 = R15 << R1;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSL, R12, R15, R2};           //12: R12 = R15 << R2;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSL, R12, R15, R3};           //13: R12 = R15 << R3;
  
  /* LSR 26 */
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSR, R11, R14, R0};           //14: R11 = R14 >> R0;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSR, R11, R14, R1};           //15: R11 = R14 >> R1;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSR, R11, R14, R2};           //16: R11 = R14 >> R2;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSR, R11, R14, R3};           //17: R11 = R14 >> R3;
  
  /* LSR 41 */
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSR, R10, R15, R0};           //18: R10 = R15 >> R0;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSR, R10, R15, R1};           //19: R10 = R15 >> R1;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSR, R10, R15, R2};           //20: R10 = R15 >> R2;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSR, R10, R15, R3};           //21: R10 = R15 >> R3;
  
end

endmodule

