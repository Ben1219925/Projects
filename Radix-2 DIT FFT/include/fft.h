#ifndef FFT_H
#define FFT_H
#include <stdio.h>


typedef struct array{
	size_t len;
	double *data;
}array;

void c_dft(array *x, array *X);
void c_fft(array *x, array *X);
void c_ifft(array *X, array *x);
void c_convolve(array *f, array *g, array *y);
void c_fft_convolve(array *f, array *g, array *y);

#endif
