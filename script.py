from __future__ import division
import numpy
import sys
from random import random
import math

filename = "c:\Lab\labview_playing\MOTConf.csv"
rate = 20000
configfile = open(filename, 'r')
conf = [line.strip().split(',') for line in configfile.readlines()]

def parsesetting(conf, rate, totalt):
    global numpy, math
    cp = numpy.array([float(val)/1000 for val in conf[0] if val != ''])
    ncp = len(cp)
    ct = numpy.array([float(val)/1000 for val in conf[1][:ncp]])
    cv = numpy.array([float(val) for val in conf[2][:ncp]])
    special = numpy.array([int(val) for val in conf[6][:ncp]])
    
    changes = []
    for i in range(ncp):
        vprev = cv[i-1]
        vthis = cv[i]
        timescale = ct[i]
        if timescale == 0 or (i == ncp-1):
            changes += [[vthis]]
        else:
            intervals = int(timescale * rate)  # implicit rounding down
            tsteps = numpy.linspace(0, intervals/rate, intervals + 1)
            funcchoose = {3: 'adiabatic',
                          4: 'exponential',
                          5: 'linear',
                          6: 'sinne',
                          }
            try:
                funcshape = funcchoose[special[i]]
            except KeyError:
                funcshape = funcchoose[5]

            # For testing
            funcshape = 'linear'

            if funcshape == 'adiabatic':
                raise NotImplemented
            elif funcshape == 'exponential':
                raise NotImplemented
            elif funcshape == 'sine':
                raise NotImplemented
            elif funcshape == 'linear':
                vals = (vthis - vprev) * tsteps / timescale + vprev
            else:
                raise ValueError

            if tsteps[-1] < timescale:
                vals = numpy.append(vals, vthis)
            changes += [list(vals)]

    intervals = int(math.ceil(totalt * rate))
    tlist = numpy.linspace(0, intervals/rate, intervals+1)

    icp = 0
    counter = 0
    values = []
    for t in tlist:
        if t >= cp[icp + 1]:
            icp += 1
            counter = 0

        if counter == 0:
            nvals = len(changes[icp])

        if counter < nvals:
            newval = changes[icp][counter]
            counter += 1
        else:
            newval = changes[icp][-1]
        values += [newval]
    return numpy.array(values)

def parseconfig(conf, rate):
    global parsesetting, math

    ch1n = int(conf[0][0])
    ch2n = int(conf[0][1])
    nparam = int(conf[0][2])
    totalt = float(conf[0][3]) / 1000
    ch1start = 2
    ch2start = ch1start + ch1n*nparam + 1

    intervals = int(math.ceil(totalt * rate))
    result = [[]] * (ch1n + ch2n)

    for i in range(ch1n):
        idx = ch1start + i * nparam
        values = parsesetting(conf[idx:idx+nparam], rate, totalt)
        result[i] = list(values)
    for i in range(ch2n):
        idx = ch2start + i * nparam
        values = parsesetting(conf[idx:idx+nparam], rate, totalt)
        result[ch1n+i] = list(values)

    return result
    
# Return variable
result = parseconfig(conf, rate)
out = result

# import pylab as pl
# ntimes = len(result[0])
# times = numpy.linspace(0, (ntimes-1) / rate, ntimes)
# for i in range(len(result)):
#     pl.plot(times, result[i], label='Ch %d' %(i))
# pl.legend(loc='best', bbox_to_anchor=(1.0, 1.0))
# pl.savefig('waveform.png')


