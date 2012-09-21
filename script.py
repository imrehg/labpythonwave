from __future__ import division
import numpy
import sys
from random import random
import math

try:  # if these succeeds, we are running inside LabPython
    infilename
    rate
    loopnum
    LabPython = True
except NameError:  # if this happens, we are running as a stand-alone script
    infilename = "c:\Lab\waveform\MOTConf.csv"
    rate = 20000
    loopnum = 0
    LabPython = False


configfile = open(infilename, 'r')
conf = [line.strip().split(',') for line in configfile.readlines()]

# These are the ramp functions we know about
funcchoose = {0: 'linear',
              3: 'adiabatic',
              4: 'exponential',
              5: 'linear',
              6: 'sine',
              }

def parsesetting(conf, rate, loopnum):
    """ Parse settings from configuration file

    Input:
    conf:
    rate:
    totalt:
    loopnum:

    Output:
    values:

    """
    global numpy, math, funcchoose
    cp = numpy.array([float(val)/1000 for val in conf[0] if val != ''])
    ncp = len(cp)
    ct = numpy.array([float(val)/1000 for val in conf[1][:ncp]])
    cv = numpy.array([float(val) for val in conf[2][:ncp]])
    
    dcp = numpy.array([float(val)/1000 for val in conf[3][:ncp]]) 
    dct = numpy.array([float(val)/1000 for val in conf[4][:ncp]]) 
    dcv = numpy.array([float(val)/1000 for val in conf[5][:ncp]]) 

    special = numpy.array([int(val) for val in conf[6][:ncp]])
    reserve = numpy.array([int(val) for val in conf[7][:ncp]])

    cp += loopnum * dcp
    totalt = cp[-1] + ct[-1]  # the last interval plus change

    changes = []
    for i in range(ncp):
        vprev = cv[i-1] + loopnum * dcv[i-1]
        vthis = cv[i] + loopnum * dcv[i]
        timescale = ct[i] + loopnum * dct[i]
        if timescale == 0:
            changes += [[vthis]]
        else:
            intervals = int(timescale * rate)  # implicit rounding down
            tsteps = numpy.linspace(0, intervals/rate, intervals + 1)

            try:
                funcshape = funcchoose[special[i]]
            except KeyError:
                raise NotImplementedError("Time dependence: %d" %special[i])

            if funcshape == 'adiabatic':
                A, B = numpy.power([vprev, vthis], -0.5)
                a = (A - B) / timescale
                vals = 1 / (A - a * tsteps)**2
            elif funcshape == 'exponential':
                raise NotImplementedError("Exponential time dependence")
            elif funcshape == 'sine':
                amplitude = reserve[i] / 2
                vals = amplitude * numpy.sin(2 * numpy.pi * tsteps / tsteps[-1]) + vthis
            elif funcshape == 'linear':
                vals = (vthis - vprev) * tsteps / timescale + vprev
            else:
                raise ValueError

            if tsteps[-1] < timescale:
                vals = numpy.append(vals, vthis)
            vals = numpy.append(vals, vthis)
            changes += [list(vals)]

    intervals = int(math.ceil(totalt * rate))
    tlist = numpy.linspace(0, intervals/rate, intervals+1)

    icp = 0
    counter = 0
    values = []
    for t in tlist:
        if icp < (ncp-1) and t >= cp[icp + 1]:
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

def parseconfig(conf, rate, loopnum):
    """ Parse the total configutation file

    Input
    conf:
    rate:
    loopnum:

    Output
    result: waveforms

    """
    global parsesetting, math

    ch1n = int(conf[0][0])
    ch2n = int(conf[0][1])
    nparam = int(conf[0][2])
    ch1start = 2
    ch2start = ch1start + ch1n*nparam + 1

    # intervals = int(math.ceil(totalt * rate))
    result = [[]] * (ch1n + ch2n)

    maxlength = -1
    for i in range(ch1n):
        idx = ch1start + i * nparam
        values = parsesetting(conf[idx:idx+nparam], rate, loopnum)
        result[i] = list(values)
        maxlength = max(len(values), maxlength)
    for i in range(ch2n):
        idx = ch2start + i * nparam
        values = parsesetting(conf[idx:idx+nparam], rate, loopnum)
        result[ch1n+i] = list(values)
        maxlength = max(len(values), maxlength)

    # Equalize the results' length
    for i in range(len(result)):
        result[i] += [result[i][-1]] * (maxlength - len(result[i]))

    return result
    
# Return variable
result = parseconfig(conf, rate, loopnum)
out = result

if not LabPython:
    import pylab as pl
    ntimes = len(result[0])
    times = numpy.linspace(0, (ntimes-1) / rate, ntimes)
    for i in range(len(result)):
        pl.plot(times, result[i], label='Ch %d' %(i))
    # pl.legend(loc='best', bbox_to_anchor=(1.0, 1.0))
    pl.savefig('waveform.png')


