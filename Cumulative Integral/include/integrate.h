#ifndef INTEGRATE_H
#define INTEGRATE_H
#include <stdio.h>

typedef struct array {
	size_t len;
	double *data;
} array;

void cumulative_integrate(array *y, array *y_time, const array *f, const array *f_time);
#endif
