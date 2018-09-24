#!/usr/bin/env/python
# -*- coding: utf-8 -*

import network
import alphaBetaTree
import numpy as np
import random
import copy


class PSO(object):

	def __init__(self,num=20):
		self.num = num
		self.particle = [network.Network() for i in range(num)]
		self.speed = [network.Network() for i in range(num)]
		self.pbest = [network.Network() for i in range(num)]
		self.pbestCount = [-100]*num
		self.currentCount = [0]*num
		self.gbestIndex = 0
		self.w =0.9
		self.c1 = 2.0
		self.c2 = 2.0
		#self.competeNum = num/2

	def reduceInertiaWeight():
		pass

	def updateVandP(self):
		"""Function used to update velecity and position of each particle in each iteration,it utilities numpy's vectorized
		arithmetic feature"""

		for i in range(self.num):
			#update the speed
			
			self.speed[i].weights_firstHidden = self.w * self.speed[i].weights_firstHidden + self.c1 * random.uniform(0,1) * \
			          (self.pbest[i].weights_firstHidden - self.particle[i].weights_firstHidden) + self.c2 * random.uniform(0,1) * \
			          (self.pbest[self.gbestIndex].weights_firstHidden - self.particle[i].weights_firstHidden)
			self.speed[i].weights_secondHidden = self.w * self.speed[i].weights_secondHidden + self.c1 * random.uniform(0,1) * \
			          (self.pbest[i].weights_secondHidden - self.particle[i].weights_secondHidden) + self.c2 * random.uniform(0,1) * \
			          (self.pbest[self.gbestIndex].weights_secondHidden - self.particle[i].weights_secondHidden)
			self.speed[i].bias_firstHidden = self.w * self.speed[i].bias_firstHidden + self.c1 * random.uniform(0,1) * \
			          (self.pbest[i].bias_firstHidden - self.particle[i].bias_firstHidden) + self.c2 * random.uniform(0,1) * \
			          (self.pbest[self.gbestIndex].bias_firstHidden - self.particle[i].bias_firstHidden)
			self.speed[i].bias_secondHidden = self.w * self.speed[i].bias_secondHidden + self.c1 * random.uniform(0,1) * \
			          (self.pbest[i].bias_secondHidden - self.particle[i].bias_secondHidden) + self.c2 * random.uniform(0,1) * \
			          (self.pbest[self.gbestIndex].bias_secondHidden - self.particle[i].bias_secondHidden)

			#update current position
			self.particle[i].weights_firstHidden = self.particle[i].weights_firstHidden + self.speed[i].weights_firstHidden
			self.particle[i].weights_secondHidden = self.particle[i].weights_secondHidden + self.speed[i].weights_secondHidden
			self.particle[i].bias_firstHidden = self.particle[i].bias_firstHidden + self.speed[i].bias_firstHidden
			self.particle[i].bias_secondHidden = self.particle[i].bias_secondHidden + self.speed[i].bias_secondHidden


	def compete(self,playerA,playerB):
		"""Function used to simulate two players compete for survival, it call interface for which alphaBetaTree provides
		'win' gains 1 point, 'lose' gains -1 point, 'draw' gain no point """

		point = alphaBetaTree.simulate(self.particle[playerA],self.particle[playerB])
		return point
        

	def computeFitness(self):
		for i in range(self.num):
			self.currentCount[i] = 0
		for i in range(self.num):
			for j in range(i+1,self.num):
				point = self.compete(i,j)
				self.currentCount[i] += point
				self.currentCount[j] += (-point)
		for i in range(self.num):
			print "particle %d" % i
			print "count",self.currentCount[i]
                    

	def updateGandP(self):
		"""Function used to update globalBest and PersonalBest value in each iteration"""
		
		#update pbest 
		for i in range(self.num):
			if self.currentCount[i] >= self.pbestCount[i]:
				#update gbest
				if self.currentCount[i] >= self.pbestCount[self.gbestIndex]:
					self.gbestIndex = i
				#update pbest
				self.pbestCount[i] = self.currentCount[i]
				self.pbest[i] = copy.deepcopy(self.particle[i])
		print "gloabal best:",self.gbestIndex


	def getBestParticle(self,filename):
		"""Function used to store the best Network into a file """

		self.pbest[self.gbestIndex].save(filename)



