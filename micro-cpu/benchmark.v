module benchmark();
  
reg reset, clk;
reg correct;


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
  i=0;  cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R14, 8'b00011010};   //0: R14 = 26;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R15, 8'b00101001};  //1: R15 = 41;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_STORE_TO_MEM, R14, 8'd100};       //2: mem[100] = R14;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_STORE_TO_MEM, R15, 8'd101};       //3: mem[101] = R15;
  
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LOAD_FROM_MEM, R12, 8'd100};      //4: R12 = mem[100];
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LOAD_FROM_MEM, R13, 8'd101};      //5: R13 = mem[101];
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_ADD, R10, R12, R13};              //6: R10 = R12 + R13;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_XOR, R11, R12, R13};              //7: R11 = R12 xor R13;

  
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R8, 8'd99};         //8: R8 = 99;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_SHORT_TO_REG, R9, 8'd11};         //9: R9 = 11;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_STORE_TO_MEM, R8, 8'd200};        //10: mem[200] = R8;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_STORE_TO_MEM, R9, 8'd201};        //11: mem[201] = R9;
  
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LOAD_FROM_MEM, R6, 8'd200};       //12: R6 = mem[200];
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_LOAD_FROM_MEM, R7, 8'd201};       //13: R7 = mem[201];
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_AND, R4, R6, R7};                 //14: R4 = R6 and R7;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_OR, R5, R6, R7};                  //15: R5 = R6 or R7;
  
  
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_MOV, R2, R4, 4'b0000};            //16: R2 = R4;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_MOV, R3, R5, 4'b0000};            //17: R3 = R5;
  i=i+1; cpuinst.raminst.mem[i] = {cpuinst.OP_BNZ, R2, 8'b00000000};         	  //18: pc = 0
  
  
  /* assert expected reg contents */
  #570 correct = 
    (cpuinst.regfileinst.R[14] == 8'b00011010) &&
    (cpuinst.regfileinst.R[15] == 8'b00101001) &&
    (cpuinst.raminst.mem[100] == cpuinst.regfileinst.R[14]) &&
    (cpuinst.raminst.mem[101] == cpuinst.regfileinst.R[15]) &&
    
    (cpuinst.regfileinst.R[12] == cpuinst.raminst.mem[100]) &&
    (cpuinst.regfileinst.R[13] == cpuinst.raminst.mem[101]) &&
    (cpuinst.regfileinst.R[10] == (cpuinst.regfileinst.R[12] + cpuinst.regfileinst.R[13])) &&
    (cpuinst.regfileinst.R[11] == (cpuinst.regfileinst.R[12] ^ cpuinst.regfileinst.R[13])) &&
    
    (cpuinst.regfileinst.R[8] == 8'd99) &&
    (cpuinst.regfileinst.R[9] == 8'd11) &&
    (cpuinst.raminst.mem[200] == cpuinst.regfileinst.R[8]) &&
    (cpuinst.raminst.mem[201] == cpuinst.regfileinst.R[9]) &&
    
    (cpuinst.regfileinst.R[6] == cpuinst.raminst.mem[200]) &&
    (cpuinst.regfileinst.R[7] == cpuinst.raminst.mem[201]) &&
    (cpuinst.regfileinst.R[4] == (cpuinst.regfileinst.R[6] & cpuinst.regfileinst.R[7])) &&
    (cpuinst.regfileinst.R[5] == (cpuinst.regfileinst.R[6] | cpuinst.regfileinst.R[7])) &&
    
    (cpuinst.regfileinst.R[2] == cpuinst.regfileinst.R[4]) &&
    (cpuinst.regfileinst.R[3] == cpuinst.regfileinst.R[5]) &&
    (cpuinst.pc == 8'b00000000);
end

endmodule