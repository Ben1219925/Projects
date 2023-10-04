#include <cstdio>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

extern "C" {
#include "convolve.h"
}

namespace py = pybind11;

std::tuple<py::array_t<double>, py::array_t<double>> convolve(py::array_t<double> &f_np, py::array_t<double> &t_f_np, py::array_t<double> &h_np, py::array_t<double> &t_h_np)
{
    array f;
    f.len = (size_t)f_np.request().size;
    f.data = (double *)f_np.request().ptr;

    array t_f;
    t_f.len = (size_t)t_f_np.request().size;
    t_f.data = (double *)t_f_np.request().ptr;

	array h;
    h.len = (size_t)h_np.request().size;
    h.data = (double *)h_np.request().ptr;
	
	array t_h;
    t_h.len = (size_t)t_h_np.request().size;
    t_h.data = (double *)t_h_np.request().ptr;

    py::array_t<double> y_np =
	py::array_t<double>((pybind11::ssize_t)(f.len+h.len -1));
    
    array y;
    y.len = (size_t)y_np.request().size;
    y.data = (double *)y_np.request().ptr;

    py::array_t<double> t_y_np =
	py::array_t<double>((pybind11::ssize_t)(t_f.len+t_h.len-1));
    
    array t_y;
    t_y.len = (size_t)t_y_np.request().size;
    t_y.data = (double *)t_y_np.request().ptr;
	
    cont_convolve(&f, &t_f, &h, &t_h, &y, &t_y);
 
    return std::make_tuple(y_np, t_y_np);
}


PYBIND11_MODULE(_ece3210_lab03, m)
{
    m.doc() = "a collection of functions for ECE 3210 lab 3";
    m.def("convolve", &convolve,
          "computes the numerical approximation of the continuous convolution integral");
}
