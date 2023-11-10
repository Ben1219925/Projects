import numpy as np
import time
import matplotlib.pyplot as plt
import _ece3210_lab07 as ece

def dft(x):
	X = ece.dft(x)
	return X
	
def fft(x):
	X = ece.fft(x)
	return X

def ifft(X):
	x = ece.ifft(X)
	return x

def convolve(f, g):
	y = ece.convolve(f, g)
	return y
	
def fft_convolve(f, g):
	y = ece.fft_convolve(f, g)
	return y


def main():
	fk = np.arange(1,17)
	print("Testing linear convolution")
	f = np.arange(8) + 1
	g = (np.arange(4) +1)[:: -1]
	y = convolve(f, g)
	ffty = fft_convolve(f, g)
	diff = y-ffty
	ylen = len(f)+len(g)-1

	if abs(diff.real.all()) < 1e-15:
		print(".")
	else:
		print(f"convolve: {y}")
		print(f"fft convolve: {ffty}")
		print("F")

	print("Testing DFT fidelity")
	myX = dft(fk)
	X = np.fft.fft(fk)
	diff = X - myX

	if abs(diff.all()) < 1e-15:
		print(".")
	else:
		print(f"MyX: {myX}")
		print(f"fftX: {X}")
		print("F")

	print("Testing FFT fidelity")
	myX = fft(fk)
	N_adjust = int(2**np.ceil(np.log2(len(fk))))
	X = np.fft.fft(fk,N_adjust)
	diff = myX-X

	if abs(diff.all()) < 1e-10:
		print(".")
	else:
		print(f"MyX: {myX}")
		print(f"fftX: {X}")
		print("F")

	print("Testing FFT convolution")
	f = np.arange(8) + 1
	g = (np.arange(4) +1)[:: -1]
	y = convolve(f, g)
	ffty = fft_convolve(f, g)
	diff = y-ffty
	ylen = len(f)+len(g)-1

	if abs(diff.real.all()) < 1e-15:
		print(".")
	else:
		print(f"convolve: {y}")
		print(f"fft convolve: {ffty}")
		print("F")

	print("Testing IFFT fidelity")
	myx = ifft(X)
	x = np.fft.ifft(X,N_adjust)
	diff = myx - x

	if abs(diff.all()) < 1e-15:
		print(".")
	else:
		print(f"Myx: {myx}")
		print(f"fftx: {x}")
		print("F")

	dTime = [0,0,0,0,0,0,0,0,0]
	fTime = [0,0,0,0,0,0,0,0,0]
	power = [2**3,2**4,2**5,2**6,2**7,2**8,2**9,2**10,2**11]

	for i in range(0,9):
		x = np.random.random(power[i])*100

		start = time.time()
		dft(x)
		end = time.time()
		dTime[i] = end-start
	
		start = time.time()
		fft(x)
		end = time.time()
		fTime[i] = end-start

	plt.loglog(power,dTime, label= "DFT")
	plt.loglog(power,fTime, label = "FFT")
	plt.xlabel("Array Size")
	plt.ylabel("Time")
	plt.legend()
	plt.title("DFT vs. FFT Time")
#	plt.savefig("ftPlot")
	plt.show()
	
	cTime = [0,0,0,0,0,0,0]
	fTime = [0,0,0,0,0,0,0]
	length = [1000,3000,6000,10000,30000,60000,100000]

	for i in range(0,7):
		f = np.random.uniform(-1000,1000,size=length[i])
		g = np.random.uniform(-1000,1000,size=length[i])


		start = time.time()
		convolve(f,g)
		end = time.time()
		cTime[i] = end-start

		start = time.time()
		fft_convolve(f,g)
		end = time.time()
		fTime[i] = end-start

	plt.loglog(length,cTime, label= "Discrete")
	plt.loglog(length,fTime, label = "FFT")
	plt.xlabel("Array Length")
	plt.ylabel("Time")
	plt.legend()
	plt.title("Discrete Convolution vs. FFT Convolution Time")
#	plt.savefig("cPlot")
	plt.show()

if __name__ == "__main__":
	main()
