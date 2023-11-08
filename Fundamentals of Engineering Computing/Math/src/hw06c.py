#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd

def main():
	data = pd.read_csv("../test/data.correct")
	data.plot(x="time", xlabel = "time (sec)", ylabel="current (mA)", title="Spice Otput")
	plt.show()


if __name__ == "__main__":
	main()

