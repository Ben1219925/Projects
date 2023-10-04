import numpy as np
import _ece3210_lab01 as ece
import matplotlib.pyplot as plt

def py_cumtrapz(f, f_time):
	if len(f) != len(f_time):
		raise ValueError
	#length of the arrays
	L = len(f)
	deltaT = np.diff(f_time)
	# y = sum k=1-N (f(tk-1)+f(tk))/2 * deltaTk
	y = (f[:L-1]+f[1:]) * deltaT/2
	y = np.cumsum(y)
	#y_time = f_timek + deltaT/2
	y_time = f_time[:L-1] + deltaT/2

	return (y, y_time)

def c_cumtrapz(f,f_time):
	if len(f) != len(f_time):
		raise ValueError
	y, y_t = ece.cumtrapz(f, f_time)
	return y, y_t

def main():
	t = np.linspace(0,4,10000)
	f = t * np.exp(-2*t)*(t>=1)
	yt = (3/(4*np.exp(2))-1/4*np.exp(-2*t)*(2*t +1))*(t>=1)
	y,y_t = py_cumtrapz(f,t)
	c_y,c_y_t = c_cumtrapz(f,t)

	plt.xlim(0,4)
	plt.plot(t,yt,label="Analytical")
	plt.plot(t,f,label="f(t)")
	plt.plot(y_t,y, label= "Python Solution")
	plt.plot(c_y_t,c_y, label= "C Solution")
	plt.legend(loc='upper right')
	plt.show()


if __name__ == "__main__":
	main()
