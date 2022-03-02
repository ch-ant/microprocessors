module heilstone_tb();
  
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
  /* conventions: */
  /* a. R15 = n */
  /* b. R0 = 8 (constant) */
  /* c. R1 = 1 (constant) */
  /* d. R9 used to store results */
  /* e. R14 used as temp reg in calculations */
  
  /* 2641 == 00001010 01010001 */
  
  /* load constants */
  i=0;   cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R0, 8'd8};   //0: R0 = 8;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R1, 8'd1};   //1: R1 = 1;
  
  /* load initial value n */
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R15, 8'b00001010}; //2: R15 = (first 8 bits of n);
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSL, R15, R15, R0};              //3: R15 = R15 << R0;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R14, 8'b01010001}; //4: R14 = (last 8 bits of n);
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_OR, R15, R15, R14};              //5: R15 = R15 or R14; (n)  
  
  /* while (n != 1) */ 
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_XOR, R9, R15, R1};      //6: R9 = R15 xor R1; (check if n == 1)                                                                       // (R9 will be 0 if n == 1)
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_BNZ, R9, 8'd9};         //7: branch to 9 if R9 != 0 (program start)
  
  /* if the code gets here it means n == 1 */
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_BNZ, R1, 8'd7};         //8: branch to 7 (program end)
  
  /* if (n mod2 == 1) */
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_AND, R9, R15, R1};        //9: R9 = R15 and R1; (mask to check if n is odd)
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_BNZ, R9, 8'd20};          //10: branch to 20 if R9 != 0 (n is odd)
  
  /* n = 3n + 1 */
  cpuinst.raminst.mem[20] = {cpuinst.OP_LSL, R14, R15, R1};           //20: R14 = R15 << R1; (n*2)
  cpuinst.raminst.mem[21] = {cpuinst.OP_ADD, R14, R14, R15};          //21: R14 = R14 + R15; (n*2 + n)
  cpuinst.raminst.mem[22] = {cpuinst.OP_ADD, R15, R14, R1};           //22: R15 = R14 + R1; (n*2 + n + 1)
  cpuinst.raminst.mem[23] = {cpuinst.OP_BNZ, R1, 8'd6};               //23: goto 6
  
  /* n = n/2 */
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LSR, R15, R15, R1};           //11: R15 = R15 >> R1;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_BNZ, R1, 8'd6};               //12: goto 6
  
end

endmodule



