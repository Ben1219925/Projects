import _ece3210_lab03 as ece
import numpy as np
import matplotlib.pyplot as plt
import time

def py_convolve(f, t_f, h, t_h):
	if len(f) != len(t_f) or len(h) != len(t_h):
		raise ValueError
	y_len = len(f)+len(h)-1
	h_len = len(h)
	y = np.zeros(y_len)
	t_y = np.zeros(y_len)
	t_y[0] = t_f[0] + t_h[0]
	T = t_f[1]-t_f[0]	
	h = np.pad(h,(0,len(f)-1), 'constant',constant_values=(0,0))
	f = np.pad(f,(0,h_len-1), 'constant', constant_values=(0,0))
	for i in range(y_len):
		y[i] = np.sum(f[:i] * h[i:0:-1]) + f[i]*h[0]
		if i+1 < y_len:
			t_y[i+1] =  t_y[i] + T

	return y*T,t_y

def c_convolve(f, t_f, h, t_h):
	if len(f) != len(t_f) or len(h) != len(t_h):
		raise ValueError
	y, t_y = ece.convolve(f,t_f,h,t_h)
	return y, t_y

def main():
	#verification plot
	tf = np.arange(0,10,.0001)
	th = np.arange(0,5,.0001)
	t = np.arange(0,15,.0001)
	f_t = np.exp(-tf/2)*(tf>=1)*(tf<=10)
	h_t = np.exp(-th)*(th>=2)*(th<=5)

	#py_y,py_t_y = py_convolve(f_t,t,h_t,th)
	c_y, c_t_y = c_convolve(f_t,tf,h_t,th)

	#analytical
	y_ta = 2*(np.exp(t/2)-np.exp(3/2))*np.exp(-t-1)*(t>= 3)*(t<=6)+(2*np.exp(-1)-2*np.exp(-5/2))*np.exp(-t/2)*(t > 6)*(t<12)+(-2*(np.exp(t/2)-np.exp(15/2))*(np.exp(-t-5/2)))*(t >= 12)*(t <= 15)

	#plt.plot(py_t_y,py_y,label="Python")
	plt.plot(c_t_y,c_y, label = "C")
	plt.plot(t,y_ta,label="Analytical")

	plt.title("C vs. Analytical")
	plt.xlabel("Time")
	plt.ylabel("y(t)")
	plt.legend()
	#plt.savefig("a.png")
	plt.show()

	T = [0.01,0.005,0.001,0.0005,0.0001,0.00005]
	py_time = np.zeros([6])
	c_time = np.zeros([6])

	#time plot
	for i in range(0,6):
		t_f = np.arange(1,5,T[i])
		t_h = np.arange(-2,3,T[i])
		f = np.random.uniform(-10,10,size=len(t_f))
		h = np.random.uniform(-10,10,size=len(t_h))

		start = time.time()
		py_convolve(f,t_f,h,t_h)
		end = time.time()
		py_time[i] = end - start

		start = time.time()
		c_convolve(f,t_f,h,t_h)
		end = time.time()
		c_time[i] = end - start
		#print(c_time)
	plt.title("Python vs. C Implementation Time")
	plt.xlabel("Sampling rate")
	plt.ylabel("Implementation Time")
	plt.loglog(T,py_time, label = "python time")
	plt.loglog(T,c_time, label = "C time")
	plt.legend()
	#plt.savefig("b.png")
	plt.show()

	
if __name__ == "__main__":
	main()

