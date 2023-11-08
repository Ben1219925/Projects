#!/usr/bin/python3
import scanf as sf

class resistor:
	def __init__(self, s):
		self.read(s)

	def current(self,V):
		I = V/self.value		
		return I

	def read(self,s):
		scan = s.split()

		l=len(scan)
		if not scan[0].lower().startswith("r"):
			raise ValueError("Resistor must start with an R: {:s}".format(s).strip())
			
		if l<4:
			raise ValueError("Resistor requires at least 4 values: {:s}".format(s).strip())
			
		vals = decodeValue(scan[3])
		self.name = scan[0].lower()
		self.posNode = scan[1].lower()
		self.negNode = scan[2].lower()
		self.value = float(vals)
	
	def print(self):
		print("{:s}\t{:s}\t{:s}\t{:.2e}".format(self.name,self.posNode,self.negNode, self.value))

def decodeValue(s):
	if s[-1].isalpha():
		vals = sf.scanf("%f%s", s)
		scan = [vals[0],vals[1].lower()]
	
		if scan[1] == "t":
			scan[0] *= 1e12

		elif scan[1] == "g":
			scan[0] *= 1e9

		elif scan[1] == "meg" or scan[1] == "x":
			scan[0] *= 1e6

		elif scan[1] == "k":
			scan[0] *= 1e3
		
		elif scan[1] == "m":
			scan[0] *= 1e-3

		elif scan[1] == "u":
			scan[0] *= 1e-6

		elif scan[1] == "n":
			scan[0] *= 1e-9

		elif scan[1] == "p":
			scan[0] *= 1e-12
	
		elif scan[1] == "f":
			scan[0] *= 1e-15

		elif scan[1] == "a":
			scan[0] *= 1e-18

		else:
			print("Invalid Value: {:s}".format(s))
		return scan[0]
	else:
		return s

	
