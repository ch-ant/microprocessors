# ANTONIOU CHRISTODOULOS
# AM 2641
# MICROPROCESSORS ΜΥE021
#
# Contents:
# (a) function that computes the signal probability of NOT logic gate
# (b) functions that compute the signal probabilities of 2 input 
#       AND, OR, XOR, NAND, NOR logic gates
# (c) functions that compute the signal probabilities of 3 input
#       AND, OR, XOR, NAND, NOR logic gates
# (d) functions that compute the signal probabilities of N input
#       AND, OR, XOR, NAND, NOR, XNOR logic gates
# (e) function that computes the switching activity of a signal for given
#       signal probability
# run command:
# python3 signalprobs.py <args>
#   <args>: list of input values
#
# example:
# python3 signalprobs.py 0.5 0.5 0.5 0.5

import sys


# demo function
def signalprobs(args):

    # convert str list to float list
    input = [ float(i) for i in args ]
    inputSize = len(args)

    if inputSize == 1:
        sp_NOT = spNOT(input[0])
        switch_act_NOT = switchingActivity(sp_NOT)

        print("NOT Gate for input probabilities:", input, 
            "\nsignal probability =", sp_NOT, 
            "\ncheck  =", 1 / 2, 
            "\nswitching activity =", switch_act_NOT, "\n")
        return

    elif inputSize == 2:
        sp_AND = sp2AND(input[0], input[1])
        sp_OR = sp2OR(input[0], input[1])
        sp_XOR = sp2XOR(input[0], input[1])
        sp_NAND = sp2NAND(input[0], input[1])
        sp_NOR = sp2NOR(input[0], input[1])

    elif inputSize == 3:
        sp_AND = sp3AND(input[0], input[1], input[2])
        sp_OR = sp3OR(input[0], input[1], input[2])
        sp_XOR = sp3XOR(input[0], input[1], input[2])
        sp_NAND = sp3NAND(input[0], input[1], input[2])
        sp_NOR = sp3NOR(input[0], input[1], input[2])

    elif inputSize > 3:
        sp_AND = spAND(input)
        sp_OR = spOR(input)
        sp_XOR = spXOR(input)
        sp_NAND = spNAND(input)
        sp_NOR = spNOR(input)


    check_AND = checkAND(input)
    check_OR = checkOR(input)
    check_XOR = checkXOR(input)
    check_NAND = checkNAND(input)
    check_NOR = checkNOR(input)

    switch_act_AND = switchingActivity(sp_AND)
    switch_act_OR = switchingActivity(sp_OR)
    switch_act_XOR = switchingActivity(sp_XOR)
    switch_act_NAND = switchingActivity(sp_NAND)
    switch_act_NOR = switchingActivity(sp_NOR)

    print("\n***********  SIGNALPROBS DEMO  ************\n")

    print("AND Gate for input probabilities:", input, 
        "\nsignal probability =", sp_AND, 
        "\ncheck =", check_AND, 
        "\nswitching activity =", switch_act_AND, "\n")

    print("OR Gate for input probabilities:", input, 
        "\nsignal probability =", sp_OR, 
        "\ncheck =", check_OR, 
        "\nswitching activity =", switch_act_OR, "\n")

    print("XOR Gate for input probabilities:", input, 
        "\nsignal probability =", sp_XOR, 
        "\ncheck =", check_XOR, 
        "\nswitching activity =", switch_act_XOR, "\n")

    print("NAND Gate for input probabilities:", input, 
        "\nsignal probability =", sp_NAND, 
        "\ncheck =", check_NAND, 
        "\nswitching activity =", switch_act_NAND, "\n")

    print("NOR Gate for input probabilities:", input, 
        "\nsignal probability =", sp_NOR, 
        "\ncheck =", check_NOR, 
        "\nswitching activity =", switch_act_NOR, "\n")

    return inputSize


# ΝΟΤ gate truth table
# 0 : 1
# 1 : 0
# signal probability calculator for a NOT gate
# input1sp: signal probability of first input signal
#        return: output signal probability
def spNOT(input1sp):
    return 1-input1sp


# 2-input AND gate truth table
# 0 0 : 0
# 0 1 : 0
# 1 0 : 0
# 1 1 : 1
# signal probability calculator for a 2-input AND gate
# input1sp: signal probability of first input signal
# input2sp: signal probability of second input signal
#        return: output signal probability
def sp2AND(input1sp, input2sp):
    return input1sp * input2sp


# 2-input OR gate truth table
# 0 0:0
# 0 1:1
# 1 0:1
# 1 1:1
# signal probability calculator for a 2-input OR gate
# input1sp: signal probability of first input signal
# input2sp: signal probability of second input signal
#        return: output signal probability
def sp2OR(input1sp, input2sp):
    return 1 - (1-input1sp) * (1-input2sp)
    # alternatively
    #return input1sp*input2sp + input1sp*(1-input2sp) + (1-input1sp)*input2sp;


# 2-input XOR gate truth table
# 0 0:0
# 0 1:1
# 1 0:1
# 1 1:0
# signal probability calculator for a 2-input XOR gate
# input1sp: signal probability of first input signal
# input2sp: signal probability of second inp
#        return: output signal probability
def sp2XOR(input1sp, input2sp):
    return input1sp*(1-input2sp) + (1-input1sp)*input2sp


# 2-input NAND gate truth table
# 0 0:1
# 0 1:1
# 1 0:1
# 1 1:0
# signal probability calculator for a 2-input XOR gate
# input1sp: signal probability of first input signal
# input2sp: signal probability of second input signal
#        return: output signal probability
def sp2NAND(input1sp, input2sp):
    return (1-input1sp)*(1-input2sp) + input1sp*(1-input2sp) + (1-input1sp)*input2sp


# 2-input NOR gate truth table
# 0 0:1
# 0 1:0
# 1 0:0
# 1 1:0
# signal probability calculator for a 2-input NOR gate
# input1sp: signal probability of first input signal
# input2sp: signal probability of second input signal
#        return: output signal probability
def sp2NOR(input1sp, input2sp):
    return (1-input1sp)*(1-input2sp)


# 3-input AND gate truth table
# 0 0 0: 0
# 0 0 1: 0
# 0 1 0: 0
# 0 1 1: 0
# 1 0 0: 0
# 1 0 1: 0
# 1 1 0: 0
# 1 1 1: 1
# signal probability calculator for a 3-input AND gate
# input1sp: signal probability of 1st input signal
# input2sp: signal probability of 2nd input signal
# input2sp: signal probability of 3rd input signal
#        return: output signal probability
def sp3AND(input1sp, input2sp, input3sp):
    return input1sp*input2sp*input3sp


# 3-input OR gate truth table
# 0 0 0: 0
# 0 0 1: 1
# 0 1 0: 1
# 0 1 1: 1
# 1 0 0: 1
# 1 0 1: 1
# 1 1 0: 1
# 1 1 1: 1
# signal probability calculator for a 3-input OR gate
# input1sp: signal probability of 1st input signal
# input2sp: signal probability of 2nd input signal
# input2sp: signal probability of 3rd input signal
#        return: output signal probability
def sp3OR(input1sp, input2sp, input3sp):
    return ( (1-input1sp)*(1-input2sp)*input3sp
            + (1-input1sp)*input2sp*(1-input3sp)
            + (1-input1sp)*input2sp*input3sp
            + input1sp*(1-input2sp)*(1-input3sp)
            + input1sp*(1-input2sp)*input3sp
            + input1sp*input2sp*(1-input3sp)
            + input1sp*input2sp*input3sp )


# 3-input ΧOR gate truth table
# 0 0 0: 0
# 0 0 1: 1
# 0 1 0: 1
# 0 1 1: 0
# 1 0 0: 1
# 1 0 1: 0
# 1 1 0: 0
# 1 1 1: 1
# signal probability calculator for a 3-input XOR gate
# input1sp: signal probability of 1st input signal
# input2sp: signal probability of 2nd input signal
# input2sp: signal probability of 3rd input signal
#        return: output signal probability
def sp3XOR(input1sp, input2sp, input3sp):
    return ( (1-input1sp)*(1-input2sp)*input3sp 
            + (1-input1sp)*input2sp*(1-input3sp) 
            + input1sp*(1-input2sp)*(1-input3sp) 
            + input1sp*input2sp*input3sp )


# 3-input NAND gate truth table
# 0 0 0: 1
# 0 0 1: 1
# 0 1 0: 1
# 0 1 1: 1
# 1 0 0: 1
# 1 0 1: 1
# 1 1 0: 1
# 1 1 1: 0
# signal probability calculator for a 3-input XOR gate
# input1sp: signal probability of 1st input signal
# input2sp: signal probability of 2nd input signal
# input2sp: signal probability of 3rd input signal
#        return: output signal probability
def sp3NAND(input1sp, input2sp, input3sp):
    return ( (1-input1sp)*(1-input2sp)*(1-input3sp) 
            + (1-input1sp)*(1-input2sp)*input3sp 
            + (1-input1sp)*input2sp*(1-input3sp) 
            + (1-input1sp)*input2sp*input3sp 
            + input1sp*(1-input2sp)*(1-input3sp) 
            + input1sp*(1-input2sp)*input3sp 
            + input1sp*input2sp*(1-input3sp) )


# 3-input NOR gate truth table
# 0 0 0: 1
# 0 0 1: 0
# 0 1 0: 0
# 0 1 1: 0
# 1 0 0: 0
# 1 0 1: 0
# 1 1 0: 0
# 1 1 1: 0
# signal probability calculator for a 3-input NOR gate
# input1sp: signal probability of 1st input signal
# input2sp: signal probability of 2nd input signal
# input2sp: signal probability of 3rd input signal
#        return: output signal probability
def sp3NOR(input1sp, input2sp, input3sp):
    return (1-input1sp)*(1-input2sp)*(1-input3sp)


# signal probability calculator for a N-input AND gate
# inputs: list of input signal probabilities 
#        return: output signal probability
def spAND(inputs):
    sp = 1
    for input in inputs:
        sp *= input
    return sp


# signal probability calculator for a N-input OR gate
# inputs: list of input signal probabilities 
#        return: output signal probability
def spOR(inputs):
    sp = 1
    for input in inputs:
        sp *= (1-input)
    return 1 - sp

    # alternatively, cascaded gates way
    # sp = sp2OR(inputs[0], inputs[1])
    # for i in range(2, len(inputs)):
    #     sp = sp2OR(sp, inputs[i])
    # return sp


# signal probability calculator for a N-input XOR gate
# inputs: list of input signal probabilities 
#        return: output signal probability
def spXOR(inputs):
    # cascaded gates way
    sp = sp2XOR(inputs[0], inputs[1])
    for i in range(2, len(inputs)):
        sp = sp2XOR(sp, inputs[i])
    return sp


# signal probability calculator for a N-input NAND gate
# inputs: list of input signal probabilities 
#        return: output signal probability
def spNAND(inputs):
    # complementary gates way
    sp = (1 - spAND(inputs))
    return sp


# signal probability calculator for a N-input NOR gate
# inputs: list of input signal probabilities 
#        return: output signal probability
def spNOR(inputs):
    #complementary gates way
    sp = (1 - spOR(inputs))
    return sp


# signal probability calculator for a N-input XNOR gate
# inputs: list of input signal probabilities 
#        return: output signal probability
def spXNOR(inputs):
    # complementary gates way
    sp = (1 - spXOR(inputs))
    return sp


# signal probability check for N-input AND gate
def checkAND(inputs):
    return 1 / (2**len(inputs))


# signal probability check for N-input OR gate
def checkOR(inputs):
    return ((2**len(inputs)) - 1) / (2**len(inputs))


# signal probability check for N-input XOR gate
def checkXOR(inputs):
    return ((2**len(inputs)) / 2) / (2**len(inputs))


# signal probability check for N-input NAND gate
def checkNAND(inputs):
    return ((2**len(inputs)) - 1) / (2**len(inputs))


# signal probability check for N-input NOR gate
def checkNOR(inputs):
    return 1 / (2**len(inputs))


# switching activity calculator for given signal probability
#       return: switching activity
def switchingActivity(sp):
    return (2 * sp * (1-sp))




if __name__ == '__main__':
    args = sys.argv[1:]
    signalprobs(args)
