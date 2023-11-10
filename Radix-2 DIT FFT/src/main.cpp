#include <cstdio>
#include <stdlib.h>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <cmath>

extern "C" {
#include "fft.h"
}

namespace py = pybind11;

py::array_t<std::complex<double>> dft(py::array_t<std::complex<double>> &x_np){
	array x;
 	x.len = (size_t)x_np.request().size * 2;
    x.data = (double *)x_np.request().ptr; 
	
	py::array_t<std::complex<double>> X_np =
	py::array_t<std::complex<double>>((pybind11::ssize_t)(x.len/2));

	array X;
   	X.len = (size_t)X_np.request().size *2;
   	X.data = (double *)X_np.request().ptr;

	c_dft(&x, &X);
	return X_np;
}

py::array_t<std::complex<double>> fft(py::array_t<std::complex<double>> &x_np){
	array x;
 	x.len = (size_t)x_np.request().size;
    x.data = (double *)x_np.request().ptr; 
	
	int len = (int)pow(2,std::ceil(log2(x.len)));
		
	py::array_t<std::complex<double>> X_np =
	py::array_t<std::complex<double>>((pybind11::ssize_t)(len));

	array X;
   	X.len = (size_t)X_np.request().size;
   	X.data = (double *)X_np.request().ptr;

	c_fft(&x, &X);
	return X_np;
}

py::array_t<std::complex<double>> ifft(py::array_t<std::complex<double>> &X_np){
	
	array X;
 	X.len = (size_t)X_np.request().size;
    X.data = (double *)X_np.request().ptr; 
	int len = (int)pow(2,std::ceil(log2(X.len)));

	py::array_t<std::complex<double>> x_np =
	py::array_t<std::complex<double>>((pybind11::ssize_t)(len));

	array x;
   	x.len = (size_t)x_np.request().size;
   	x.data = (double *)x_np.request().ptr;

	c_ifft(&X, &x);
	return x_np;
}

py::array_t<std::complex<double>> convolve(py::array_t<std::complex<double>> &f_np, py::array_t<std::complex<double>> &g_np){
	array f;
 	f.len = (size_t)f_np.request().size*2;
    f.data = (double *)f_np.request().ptr; 

	array g;
 	g.len = (size_t)g_np.request().size*2;
    g.data = (double *)g_np.request().ptr; 

	py::array_t<std::complex<double>> y_np =
	py::array_t<std::complex<double>>((pybind11::ssize_t)((f.len/2) + (g.len/2) -1));

	array y;
   	y.len = (size_t)y_np.request().size*2;
   	y.data = (double *)y_np.request().ptr;

	c_convolve(&f, &g, &y);
	return y_np;
}

py::array_t<std::complex<double>> fft_convolve(py::array_t<std::complex<double>> &f_np, py::array_t<std::complex<double>> &g_np){
	array f;
 	f.len = (size_t)f_np.request().size*2;
    f.data = (double *)f_np.request().ptr; 

	array g;
 	g.len = (size_t)g_np.request().size*2;
    g.data = (double *)g_np.request().ptr; 

	py::array_t<std::complex<double>> y_np =
	py::array_t<std::complex<double>>((pybind11::ssize_t)((f.len/2) + (g.len/2) -1));

	array y;
   	y.len = (size_t)y_np.request().size*2;
   	y.data = (double *)y_np.request().ptr;

	c_fft_convolve(&f, &g, &y);
	return y_np;
}

PYBIND11_MODULE(_ece3210_lab07, m)
{
    m.doc() = "a collection of functions for ECE 3210 lab 7";
    m.def("dft", &dft,
          "This function implements the DFT of an array x and returns the transform array X");
	m.def("fft", &fft,
          "This function implements the FFT of an array x and returns the transform array X");
	m.def("ifft", &ifft,
		  "This function implements the inverse fft of an array X and returns the transform array x");
	m.def("convolve", &convolve,
          "This function implements the convolution of two arrays f and g, and returns the convolved array y");
	m.def("fft_convolve", &fft_convolve,
          "This function implements the fft convolution of two arrays f and g, and returns the convolved array y");
}
