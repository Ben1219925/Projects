#include "ece5210.h"

#include <stdio.h>
#include <string.h>
#include <math.h>

buffer x_buffer1;
buffer x_buffer2;
buffer x_buffer3;

buffer buffer1;
buffer buffer2;
buffer buffer3;
buffer buffer4;

buffer x_buffer4;
buffer x_buffer5;
buffer x_buffer6;

buffer buffer5;
buffer buffer6;
buffer buffer7;
buffer buffer8;

float AP(float x, buffer* buf, float g, int16_t N){
	int16_t n = buf->ind;
	float y = 0;
	int index = n - N;
	if (index < 0)
		index += N;
	buf->data[n] = x - g*buf->data[index];
	y = -g*buf->data[n] + buf->data[index];	
	buf->ind = (n+1) % N;

	
	return y;
}

float FBCF(float x, buffer* buf, float g, int16_t N){
	int16_t n = buf->ind;
	float y = 0;
	int index = n - N;
	if (index < 0)
		index += N;
	buf->data[n] = x - g*buf->data[index];
	y = buf->data[n];	
	buf->ind = (n+1) % N;

	
	return y;
}

int16_t process_sample_left(int16_t sample_in)
{
    int16_t sample_out = 0;
    float sample_in_f = (float)sample_in;

	//Version with comb followed by all pass
    float x1 = FBCF(sample_in_f, &buffer1,0.805,901);
	float x2 = FBCF(sample_in_f, &buffer2,0.827,778);
	float x3 = FBCF(sample_in_f, &buffer3,0.783,1011);
	float x4 = FBCF(sample_in_f, &buffer4,0.764,1123);
    float sample = x1+x2+x3+x4;

	float AP1 = AP(sample, &x_buffer1, 0.7, 125);
	float AP2 = AP(AP1, &x_buffer2, 0.7, 42);
	float AP3 = AP(AP2, &x_buffer3, 0.7, 12);
	float option1 = AP3;
	float option2 = -option1;

	//Versions with all pass followed by comb
	AP1 = AP(sample_in_f, &x_buffer4, 0.7, 347);
	AP2 = AP(AP1, &x_buffer5, 0.7, 113);
	AP3 = AP(AP2, &x_buffer6, 0.7, 37);

	x1 = FBCF(AP3, &buffer5,0.773,1687);
	x2 = FBCF(AP3, &buffer6,0.802,1601);
	x3 = FBCF(AP3, &buffer7,0.753,2053);
	x4 = FBCF(AP3, &buffer8,0.733,2251);

	//multiple outputs to choose from depending on desired mixing
	float s1 = x1+x3;
	float s2 = x2+x4;
	float option3 = s1 + s2;
	float option4 = -option3;
	float option5 = s1 - s2;
	float option6 = -option5;

	//choose which option to output
	float sample_out_f = option6;


	// Convert back to int16_t
	sample_out = (int16_t)sample_out_f;
	return sample_out;
}

