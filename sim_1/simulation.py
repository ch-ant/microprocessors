# ANTONIOU CHRISTODOULOS
# AM 2641
# MICROPROCESSORS ΜΥE021
#
# Simulation of a small logic circuit.
# Calculates the switching activity using Signal Probabilities and Monte Carlo simulation.
#
# run command:
# python3 simulation.py <args>
#   <args>: list of input values
#
# run example:
# python3 simulation.py 0.5 0.5 0.5

import signalprobs as SP
import random as R
import sys

def model(a, b, c):
    e = SP.spAND([a, b])
    f = SP.spNOT(c)
    d = SP.spAND([e, f])

    return [e, f, d]


def testbench():
    print("a b c | e f | d")
    for a in range(2):
        for b in range(2):
            for c in range(2):
                [e, f, d] = model(a, b, c)
                print(a, b, c, "|", e, f, "|", d)


def switchingActivity(spA, spB, spC):
    [spE, spF, spD] = model(spA, spB, spC)

    switch_act_e = SP.switchingActivity(spE)
    switch_act_f = SP.switchingActivity(spF)
    switch_act_d = SP.switchingActivity(spD)

    print("Switching activity of signal e:", switch_act_e, "\n"
        "Switching activity of signal f:", switch_act_f, "\n"
        "Switching activity of signal d:", switch_act_d, "\n")


def monteCarlo(N):
    workload = []
    for i in range(N):
        workload.append( [ R.randint(0, 1), R.randint(0, 1), R.randint(0, 1)] )
    
    vectors = len(workload)

    [e, f, d] = model(0, 0, 0)
    switchesE = 0
    switchesF = 0
    switchesD = 0

    for input in workload:
        a = input[0]
        b = input[1]
        c = input[2]

        [newE, newF, newD] = model(a, b, c)

        if e != newE:
            e = newE
            switchesE += 1

        if f != newF:
            f = newF
            switchesF += 1

        if d != newD:
            d = newD
            switchesD += 1

    switch_act_e = switchesE / vectors
    switch_act_f = switchesF / vectors
    switch_act_d = switchesD / vectors

    print("Signal e:\nswitches:", switchesE, "\nswitching activity:", switch_act_e,
            "\n\nSignal f:\nswitches:", switchesF, "\nswitching activity:", switch_act_f,
            "\n\nSignal d:\nswitches:", switchesD, "\nswitching activity:", switch_act_d, 
            "\n\nVectors:", vectors)



args = sys.argv[1:]
input = [ float(i) for i in args ]



print("\n***********  TRUTH TABLE  ************\n")
testbench()

print("\n*****  SWITCHING ACTIVITY WITH SIGNAL PROBS  *****\n")
switchingActivity(input[0], input[1], input[2])

print("\n*****  SWITCHING ACTIVITY WITH MONTE CARLO  *****\n")
monteCarlo(50000)