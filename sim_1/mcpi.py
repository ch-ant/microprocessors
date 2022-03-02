# ANTONIOU CHRISTODOULOS
# AM 2641
# MICROPROCESSORS ΜΥE021
#
# Monte Carlo simulation for pi value estimation
#
# run command:
# python3 mcpi.py <N>
#   <N>: number of sample points


from math import sqrt
import random as R
import sys


def mcpi(N):

    PI = 3.14159265359
    a = 1
    r = a / 2

    Esquare = a ** 2
    Ecircle = PI * (r ** 2)
    innerCounter = 0

    for i in range(N):

        Sx = R.random()
        Sy = R.random()
        distance = sqrt( (Sx - 0.5)**2 + (Sy - 0.5)**2)

        if distance <= r:
            innerCounter += 1

    ratio = innerCounter / N * 4
    return ratio

N = int(sys.argv[1])
print(mcpi(N))