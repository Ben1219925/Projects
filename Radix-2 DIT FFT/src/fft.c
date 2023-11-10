#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include "fft.h"
#include <string.h>
#include <stdbool.h>

void c_dft(array *x, array *X){
	int N0 = (int)x->len/2;
	double theta;
	for(int r = 0; r < N0; r++){
		X->data[2*r] = 0;
		X->data[2*r+1] = 0;
		for(int k = 0; k <= N0-1; k++){
			theta = -(2*M_PI/N0)*r*k;
			X->data[2*r] += (x->data[2*k]*cos(theta)) - (x->data[2*k+1]*sin(theta));
			X->data[2*r+1] += (x->data[2*k]*sin(theta)) + (x->data[2*k+1] *cos(theta));
		}
	}
	
}

int bitReversal(int num, int bitNum) {
    int reversed = 0;
    while (bitNum--) {
        reversed <<= 1;
        reversed |= (num & 1);
        num >>= 1;
    }
    return reversed;
}


void c_fft(array *xOld, array *X) {
	//resize array
	array x;
	x.len = (size_t)pow(2,ceil(log2((double)xOld->len)));
	x.data = (double*)calloc(x.len*2,sizeof(double));
	memcpy(x.data, xOld->data, xOld->len * 2 *sizeof(double));
	
	int N0 = (int)x.len;
   	int bitNum = (int)log2(N0);
	int N;
	double theta;
	double gRe;
	double gIm;
	double hRe;
	double hIm;
	int reversedBit;
	double cosT;
	double sinT;
	int hIndex1;
	int hIndex2;
	int gIndex1;
	int gIndex2;
	// Parallelize bit-reversal
   	#pragma omp parallel for
   	//reverses bits and saves to the output array in the reverse bit order
   	for(int i = 0; i < N0; i++) {
       	reversedBit = bitReversal(i, bitNum);
       	X->data[2 * i] = x.data[2 * reversedBit];
       	X->data[2 * i + 1] = x.data[2 * reversedBit + 1];
   	}
	//steps of butterfly
   	for(int step = 1; step <= bitNum; step++){
		//same as 2^step but slightly faster
       	N = 1 << step; 
		//groups
		#pragma omp parallel for private(theta,cosT,sinT,gIndex1,gIndex2,hIndex1,hIndex2, gRe, gIm, hRe, hIm)
       	for(int k = 0; k < N0; k += N) {
			//each index in the group
           	for(int r = 0; r < N/2; r++) {
				printf("%d",r);
               	theta = -2 * M_PI * r/N;
				//using variables to reduce the number of calculations and attempt to speed up the function
				cosT = cos(theta);
				sinT = sin(theta);
				gIndex1 = 2 * (k+r);
				gIndex2 = gIndex1 + 1;
				hIndex1 =  2 * (k+r+N/2);
				hIndex2 = hIndex1 + 1;
			
				gRe = X->data[gIndex1];
               	gIm = X->data[gIndex2];
               	hRe = X->data[hIndex1] * cosT - X->data[hIndex2] * sinT;
               	hIm = X->data[hIndex1] * sinT + X->data[hIndex2] * cosT;

                
               	X->data[gIndex1] = gRe + hRe;
               	X->data[gIndex2] = gIm + hIm;

               	X->data[hIndex1] = gRe - hRe;
               	X->data[hIndex2] = gIm - hIm;
           	}
       	}
   	}
}

void c_ifft(array *XOld, array *x){
	//resize array
	array X;
	X.len = (size_t)pow(2,ceil(log2((double)XOld->len)));
	X.data = (double*)calloc(X.len*2,sizeof(double));
	memcpy(X.data, XOld->data, XOld->len * 2 *sizeof(double));
	
	int N0 = (int)X.len;
    int bitNum = (int)log2(N0);
	int N;
	double theta;
	double gRe;
	double gIm;
	double hRe;
	double hIm;
	int reversedBit;
	// Parallelize bit-reversal
    #pragma omp parallel for
    //reverses bits and saves to the output array in the reverse bit order
    for(int i = 0; i < N0; i++) {
        reversedBit = bitReversal(i, bitNum);
        x->data[2 * i] = X.data[2 * reversedBit];
        x->data[2 * i + 1] = X.data[2 * reversedBit + 1];
    }
	//steps of butterfly
    for(int step = 1; step <= bitNum; step++){
		//same as 2^step but slightly faster
        N = 1 << step; 
		//groups
		#pragma omp parallel for private(theta, gRe, gIm, hRe, hIm)
        for(int k = 0; k < N0; k += N) {
			//each index in the group
            for(int r = 0; r < N/2; r++) {
                theta = 2 * M_PI * r/N;
				
				gRe = x->data[2 * (k+r)];
                gIm = x->data[2 * (k+r) + 1];

                hRe = x->data[2 * (k+r+N/2)] * cos(theta) - x->data[2 * (k+r+N/2) + 1] * sin(theta);
                hIm = x->data[2 * (k+r+N/2)] * sin(theta) + x->data[2 * (k+r+N/2) + 1] * cos(theta);

                
                x->data[2 * (k+r)] = (gRe + hRe);
                x->data[2 * (k+r) + 1] = (gIm + hIm);

                x->data[2 * (k+r+N/2)] = (gRe - hRe);
                x->data[2 * (k+r+N/2) + 1] = (gIm - hIm);
            }
        }
    }
	for(int mult = 0; mult < N0; mult++){
		x->data[2*mult] *= 1.0/N0;
		x->data[2*mult+1] *= 1.0/N0;
	}	
}



void c_convolve(array *f, array *g, array *y){
	size_t yLen = f->len + g->len -1;
	size_t j;
	//make copies of f and h of size y_len
	array fCopy;
	fCopy.len = yLen;
	fCopy.data = (double *) calloc(yLen, sizeof(double));
	array gCopy;
	gCopy.len = yLen;
	gCopy.data = (double *) calloc(yLen, sizeof(double));

	memcpy(fCopy.data,f->data,f->len*sizeof(double));
	memcpy(gCopy.data,g->data,g->len*sizeof(double));

	for(size_t i = 0; i < yLen; i++){	
		j = i;
		for(size_t k = 0; k <= i; k++){	
			y->data[i] += fCopy.data[k]* gCopy.data[j];
			j--;
		}
		
	}
	free(fCopy.data);
	free(gCopy.data);
}

void c_fft_convolve(array *f, array *g, array *y){
	size_t yLen = y->len;
	//make copies of f and h of size y_len
	array fCopy;
	fCopy.len = yLen/2;
	fCopy.data = (double *) calloc(yLen, sizeof(double));
	array gCopy;
	gCopy.len = yLen/2;
	gCopy.data = (double *) calloc(yLen, sizeof(double));

	memcpy(fCopy.data, f->data, f->len * sizeof(double));
	memcpy(gCopy.data, g->data, g->len * sizeof(double));
	
	size_t len = (size_t)pow(2,ceil(log2((double)fCopy.len)));	

	array F;
	F.len = len;
	F.data = (double*)calloc(len*2,sizeof(double));

	array G;
	G.len = len;
	G.data = (double*)calloc(len*2,sizeof(double));

	array Y;
	Y.len = len;
	Y.data = (double*)calloc(len*2,sizeof(double));
	
	array temp;
	temp.len = len;
	temp.data = (double*)calloc(len*2,sizeof(double));

	c_fft(&fCopy,&F);
	c_fft(&gCopy,&G);

	for(int i = 0; i < len; i++){
		Y.data[2*i] = F.data[2*i] * G.data[2*i] - F.data[2*i+1] * G.data[2*i+1];
		Y.data[2*i+1] = F.data[2*i] * G.data[2*i+1] + F.data[2*i+1] * G.data[2*i];
	}

	c_ifft(&Y,&temp);
	memcpy(y->data, temp.data, y->len * sizeof(double));
}
