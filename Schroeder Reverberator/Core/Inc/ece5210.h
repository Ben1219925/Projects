#ifndef ECE5210_H
#define ECE5210_H

#include <stdint.h>

/* 
   this controls the right channel behavior.  if defined,
   this will just pass the original signal through the right
   channel.  if not defined, it will copy the processed samples
   into the right channel.
*/
#define PASSTHROUGH_RIGHT

typedef struct buffer {
	float data [2251];
	int16_t ind ;
} buffer ;

int16_t process_sample_left(int16_t sample_in);
float AP(float x, buffer* buf, float g, int16_t N);
float FBCF(float x, buffer* buf, float g, int16_t N);

#endif
