module MCPU_RAMControllertb2();
parameter WORD_SIZE=8;
parameter ADDR_WIDTH=8;
parameter RAM_SIZE=1<<ADDR_WIDTH;

reg write_correct;
reg rd_correct;
reg ri_correct;

reg we, re;

reg [WORD_SIZE-1:0] datawr;

reg [ADDR_WIDTH-1:0] addr;
reg [ADDR_WIDTH-1:0] instraddr;

wire [WORD_SIZE-1:0] datard;
wire [WORD_SIZE-1:0] instrrd;

reg [WORD_SIZE-1:0] mem_copy[RAM_SIZE-1:0];


MCPU_RAMController raminst (we, datawr, re, addr, datard, instraddr, instrrd);


integer i, load_finished;

initial begin
  load_finished = 0;
  write_correct = 0;
  rd_correct = 0;
  ri_correct = 0;
  re = 0;
  we = 0;
  addr = 0;
  instraddr = 0;
  
  for(i=0; i<RAM_SIZE; i=i+1) begin
    addr = i;
    if (i % 2 == 0)
      datawr = 26;
    else
      datawr = 41;
    #1 we <= 1;
    #1 we <= 0;
    
    mem_copy[i] = datawr;
      
    $display("mem[%0d] = 0x%0h = 0x%0h", i, mem_copy[i], raminst.mem[i]);
    write_correct = (mem_copy[i] == raminst.mem[i]);
  end
  load_finished = 1;
end

always begin
  #1 re <= 0;
  if (load_finished) begin
  
    if (addr >= RAM_SIZE)
      addr = 0;
    else
      addr = addr + 1;
    
    if (instraddr >= RAM_SIZE)
      instraddr = 0;
    else
      instraddr = instraddr + 1;
    
    #1 re <= 1;
  
    rd_correct = (datard == mem_copy[addr]);
    ri_correct = (instrrd == mem_copy[instraddr]);
  end
end





endmodule
