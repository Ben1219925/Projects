#!/usr/bin/python3
import control as ctl
import matplotlib.pyplot as plt

def main():
	s=ctl.TransferFunction.s
	H=(5*(s+5)*(s+3)*(s+1))/((s+6)*(s+12)*(s+5))
	ctl.bode_plot(H,Hz=True, omega=(.01,10),dB=True)
	ctl.pzmap(H)
	plt.show()

if __name__ == "__main__":
	main()
