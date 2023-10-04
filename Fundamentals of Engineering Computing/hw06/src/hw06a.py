#!/usr/bin/python3
import numpy as np
from scipy import optimize as op
import sys

def f(T,ni,element):
	B = {"Si":1.08e31,"Ge":2.31e30,"GaAs":1.27e29}
	EG = {"Si":1.12,"Ge":.66,"GaAs":1.42}
	k = 8.62e-5
	return B[element]*(T**3)*np.exp(-(EG[element]/(k*T))) - (ni**2)

def FindT(ni,minT=1,maxT=1000,element="Si"):
	T = op.brentq(f,minT,maxT, args=(ni,element))
	return T

def main():
	ni = float(sys.argv[1])
	try:
		if len(sys.argv) == 2:
			T = FindT(ni)
		elif len(sys.argv) == 4:
			minT = int(sys.argv[2])
			maxT = int(sys.argv[3])
			T = FindT(ni,minT,maxT)
		else:	
			minT = int(sys.argv[2])
			maxT = int(sys.argv[3])
			element = sys.argv[4]
			T = FindT(ni,minT,maxT,element)

	except Exception:
		print("No Solution")
		return -1
	
	print("T={:.2e}".format(T))

if __name__ == "__main__":
	main()
