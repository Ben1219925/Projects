#!/usr/bin/python3
import hw05_lib as h5

def main():
	Res = input("Enter a resistor: ")
	try:
		R = h5.resistor(Res)
		R.print()
		V = h5.decodeValue( input("Enter a voltage: "))
		I = R.current(V)
		print("I = {:.2e}".format(I))
	except ValueError as e:
		print(e)
if __name__ == "__main__":
	main()

