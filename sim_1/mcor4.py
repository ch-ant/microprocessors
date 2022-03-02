# ANTONIOU CHRISTODOULOS
# AM 2641
# MICROPROCESSORS ΜΥE021
#
# Monte Carlo simulation for the switching activity of a 4 input OR gate
#
# run command:
# python3 mcor.py <N>
#   <N>: number of permutations
#
#
# 4 input OR gate truth table:
#   I1 I2 I3 I4 | O
#   X  X  X  1 | 1 
#   X  X  1  X | 1 
#   X  1  X  X | 1 
#   1  X  X  X | 1 
#   0  0  0  0 | 0


import sys
import random as R


def mcor4(N):

    workload = [ [0, 0, 0, 0],
                            [1, 1, 1, 1],
                            [0, 0, 0, 1],
                            [1, 1, 1, 1],
                            [0, 1, 0, 1,] ]
    #workload = []

    for i in range(N):
        workload.append([ R.randint(0, 1), R.randint(0, 1), R.randint(0, 1), R.randint(0, 1) ])

    # every row in workload has the same number of columns
    rows = len(workload)    # vectors number
    columns = len(workload[0])  # inputs number

    gateOutput = 0 | 0 | 0 | 0
    switchesCounter=  0

    for i in range(rows):
        newGateOutput = workload[i][0] | workload[i][1] | workload[i][2] | workload[i][3]

        if (gateOutput == newGateOutput): 
            continue

        gateOutput = newGateOutput
        switchesCounter += 1

    print("switchesCounter: ", switchesCounter)
    print("vectors: ", rows)
    switchingActivity = switchesCounter / rows
    return switchingActivity


N = int(sys.argv[1])
print(mcor4(N))