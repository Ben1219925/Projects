#include "convolve.h"
#include <stdio.h>
#include <stdlib.h>

void cont_convolve(array *f, array *t_f, array *h, array *t_h, array *y, array *t_y){
	size_t y_len = f->len + h->len -1;
	size_t j = 0;
	//make copies of f and h of size y_len
	array f_copy;
	f_copy.len = y_len;
	f_copy.data = (double *) calloc(y_len,  sizeof(double));
	array h_copy;
	h_copy.len = y_len;
	h_copy.data = (double *) calloc(y_len,  sizeof(double));
	//set up t_y[0]
	t_y->data[0] = t_f->data[0] + t_h->data[0];
	//find deltaT
	double T = t_f->data[1] - t_f->data[0];
	//copy array values and pad copies end with zeros
	for(size_t i = 0; i < y_len; i++){	
		if(i < f->len)
			f_copy.data[i] = f->data[i];	
		if(i < h->len)
			h_copy.data[i] = h->data[i];
		j = i;
		for(size_t k = 0; k <= i; k++){	
			y->data[i] += (f_copy.data[k]* h_copy.data[j]);
			j--;
		}
		y->data[i] = y->data[i] * T;
		
		if (i+1 < y_len)
			t_y->data[i+1] = t_y->data[i] + T;
	}
	free(f_copy.data);
	free(h_copy.data);
}
