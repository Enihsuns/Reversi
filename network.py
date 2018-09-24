#!/usr/bin/env/python
# -*- coding: utf-8 -*

import random
import numpy as np
import json
import sys

class Network(object):

    def __init__(self, sizes=[64,91,10,1]):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron. """
        self.num_layers = len(sizes)
        self.sizes = sizes

        #input layer mapped to frist hidden layer using convolution 
        #weights is segmented into 9,16,25,36,49,64,each subfield of 
        #same size using same weights

        subfieldList = [9,16,25,36,49,64]
        self.weights_firstHidden = np.array([np.random.randn(x,1) for x in subfieldList])
        self.weights_secondHidden = np.array([np.random.randn(y,x) for x,y 
        								in zip(sizes[1:-1],sizes[2:])])

        subfieldBias = [36,25,16,9,4,1]
        self.bias_firstHidden = np.array([np.random.randn(x,1) for x in subfieldBias])
        self.bias_secondHidden = np.array([np.random.randn(x,1) for x in sizes[2:]])


    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.bias_secondHidden, self.weights_secondHidden):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def calculate(self,chess,index):
    	"""It helps calculate the activation value of first hidden layer.
    	the index indicates which size of the subfield to be calculated """
    	adjustChess = []
    	for i in range(9-index):
    		for j in range(9-index):
    			temp = []
    			for k in range(index):
    				temp += chess[i+k][j:j+index]
    			adjustChess.append(temp)

    	return np.array(adjustChess)

    			
    def evaluate(self,chess):
    	"""The chess is a two-dimension input array of (8,8),0 represent white,
    	1 represent black. Returns a value between 0 and 1 as the evaluation """

    	#input layer to first hidden layer
    	firstHiddenActivation = []
        for i in range(3,9):
        	temp = self.calculate(chess,i)
        	activation = sigmoid(np.dot(temp,self.weights_firstHidden[i-3])+self.bias_firstHidden[i-3])
        	activationList = list(activation)
        	firstHiddenActivation += activationList
        	#print activation
        firstHiddenActivation = np.array(firstHiddenActivation)
        
        value = self.feedforward(firstHiddenActivation)
 
        return value

    def save(self, filename):
        """Save the neural network to the file ``filename``."""
        data = {"sizes": self.sizes,
                "weights_firstHidden": [w.tolist() for w in self.weights_firstHidden],
                "bias_firstHidden": [b.tolist() for b in self.bias_firstHidden],
                "weights_secondHidden": [w.tolist() for w in self.weights_secondHidden], 
                "bias_secondHidden": [b.tolist() for b in self.bias_secondHidden]
                }
        f = open(filename, "w")
        json.dump(data, f)
        f.close()


#### Loading a Network
def load(filename):
    """Load a neural network from the file ``filename``.  Returns aninstance of Network."""

    f = open(filename, "r")
    data = json.load(f)
    f.close()
    net = Network(data["sizes"])
    net.weights_firstHidden = np.array([np.array(w) for w in data["weights_firstHidden"]])
    net.bias_firstHidden = np.array([np.array(b) for b in data["bias_firstHidden"]])
    net.weights_secondHidden = np.array([np.array(w) for w in data["weights_secondHidden"]])
    net.bias_secondHidden = np.array([np.array(b) for b in data["bias_secondHidden"]])
    return net


#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))


