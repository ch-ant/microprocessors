# ANTONIOU CHRISTODOULOS
# AM 2641
# MICROPROCESSORS ΜΥE021
#
# Demo simulation of a logic circuit.
# Calculates the switching activity of all outputs.
#
# run command:
# python3 demo.py 


from datastructures import Element
from datastructures import Signal
from datastructures import Simulation

import signalprobs as SP


def model(a, b, c):
    E0 = Element('AND', [0, 1], 4)
    E1 = Element('NOT', [2], 5)
    E2 = Element('AND', [4, 5], 3)

    S0 = Signal('a', a)
    S1 = Signal('b', b)
    S2 = Signal('c', c)
    S3 = Signal('e', 0)
    S4 = Signal('f', 0)
    S5 = Signal('d', 0)

    simulation = Simulation()
    simulation.signals = [S0, S1, S2, S5, S3, S4]
    simulation.elements = [E0, E1, E2]

    for element in simulation.elements:
        simulation.process(element)
    return simulation


def testbench():
    print("a b c | e f | d")
    for a in range(2):
        for b in range(2):
            for c in range(2):
                simulation = model(a, b, c)
                # e = simulation.signals[4]
                # f = simulation.signals[5]
                # d = simulation.signals[3]
                e = simulation.findSignal('e')
                f = simulation.findSignal('f')
                d = simulation.findSignal('d')
                print(str(a), str(b), str(c) , "|", str(e.value), str(f.value), "|", str(d.value))


def switchingActivity(spA, spB, spC):
    simulation = model(spA, spB, spC)

    e = simulation.findSignal('e')
    f = simulation.findSignal('f')
    d = simulation.findSignal('d')

    switch_act_e = SP.switchingActivity(e.value)
    switch_act_f = SP.switchingActivity(f.value)
    switch_act_d = SP.switchingActivity(d.value)

    print("Switching activity of signal e:", switch_act_e, "\n"
        "Switching activity of signal f:", switch_act_f, "\n"
        "Switching activity of signal d:", switch_act_d, "\n")


if __name__ == '__main__':
    print("\n***********  TRUTH TABLE  ************\n")
    testbench()

    print("\n*****  AVERAGE SWITCHING ACTIVITY  *****\n")
    switchingActivity(0.5, 0.5, 0.5)

    print("\n*****  SWITCHING ACTIVITY WITH AM *****\n")
    switchingActivity(0.2641, 0.2641, 0.2641)