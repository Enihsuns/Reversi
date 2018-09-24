#!/usr/bin/env/python
# -*- coding: utf-8 -*

import numpy as np
import pso
import network

swarm = pso.PSO(num=5)

print "start training"
print "each iteration will print all particles' fitness"
print "iter 1"
swarm.computeFitness()
swarm.updateGandP()

iterNum = 9
for i in range(iterNum):
    print "iter %d" % (i+2)
    swarm.updateVandP()
    swarm.computeFitness()
    swarm.updateGandP()
 #store the best network into file   
swarm.getBestParticle("network.json")
