#include <cstdio>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

extern "C" {
#include "integrate.h"
}

namespace py = pybind11;

std::tuple<py::array_t<double>, py::array_t<double>> cumtrapz(py::array_t<double> &f_np,
					py::array_t<double> &f_time_np)
{

    array f_time;
    f_time.len = (size_t)f_time_np.request().size;
    f_time.data = (double *)f_time_np.request().ptr;

    array f;
    f.len = (size_t)f_np.request().size;
    f.data = (double *)f_np.request().ptr;

    py::array_t<double> y_np =
	py::array_t<double>((pybind11::ssize_t)(f.len - 1));
    
    array y;
    y.len = (size_t)y_np.request().size;
    y.data = (double *)y_np.request().ptr;

    py::array_t<double> y_time_np =
	py::array_t<double>((pybind11::ssize_t)(f_time.len - 1));
    
    array y_time;
    y_time.len = (size_t)y_time_np.request().size;
    y_time.data = (double *)y_time_np.request().ptr;

    cumulative_integrate(&y, &y_time, &f, &f_time);
    
    return std::make_tuple(y_np, y_time_np);
}


PYBIND11_MODULE(_ece3210_lab01, m)
{
    m.doc() = "a collection of functions for ECE 3210 lab 1";
    m.def("cumtrapz", &cumtrapz,
          "computes the cumulative integral of an arbitrary waveform");
}
