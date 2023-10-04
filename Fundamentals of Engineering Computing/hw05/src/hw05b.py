#!/usr/bin/python3
import sys
import hw05_lib as h5

def main():
	if len(sys.argv) < 2:
		print("No netlist file given")
		exit()
	Rs = []
	inName = sys.argv[1]
	inFile = open(inName, 'r')
	for line in inFile:	
		try:
			Rs.append(h5.resistor(line))
		except ValueError as e:
			print(e)
			
	inFile.close()
	for R in Rs:
		R.print()


if __name__ == "__main__":
	main()
