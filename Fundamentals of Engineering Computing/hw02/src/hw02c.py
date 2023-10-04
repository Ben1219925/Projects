#!/usr/bin/python3

def getComponent(c):
	c = c.lower()
	if c == 'r':
		return "Resistor"
	if c == 'c':
		return "Capacitor"
	if c == 'l':
		return "Inductor"
	if c== 'd':
		return "Diode"
	if c == 'v':
		return "Voltage Source"
	if c == 'i':
		return "Current Source"
	else:
		raise ValueError("Component {:s} is invalid".format(c))
		
def main():
	component = ['C','V','i','L','x','D','R','r','d','c']
	for i in component:
		try:
			print("{:s}\t{:s}".format(i,getComponent(i)))
		except ValueError as e:
			print(e)
			

if __name__ == "__main__":
    main()

