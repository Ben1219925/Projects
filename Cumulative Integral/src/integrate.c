#include "integrate.h"
#include <stdio.h>

void cumulative_integrate(array *y, array *y_time, const array *f, const array *f_time){
	double deltaT;
	for (int k=1; k < f->len; k++){
		deltaT = f_time->data[k] - f_time->data[k-1];
		y->data[k-1] = (f->data[k-1] + f->data[k]) * (deltaT/2);
		y_time->data[k-1] = f_time->data[k-1] + deltaT/2; 
	}
	
	for (int i=1; i < y->len; i++){
		y->data[i] = y->data[i-1] + y->data[i];
	}
}

