#ifndef CONVOLVE_H
#define CONVOLVE_H
#include <stdio.h>

typedef struct array{
	size_t len;
	double *data;
}array;

void cont_convolve(array *f, array *t_f, array *h, array *t_h, array *y, array *t_y);

#endif


