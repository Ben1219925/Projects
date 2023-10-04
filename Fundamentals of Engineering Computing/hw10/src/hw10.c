#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv){
	if(argc < 4){
		printf("Error, not enough arguments");
		return -1;
	}
	int bufferSize;
	sscanf(argv[3],"%d", &bufferSize);
	float* buffer;
	buffer = (float *)calloc(bufferSize,sizeof(float));
	float avg = 0;
	int numValIn = 0;
	int numValOut = 0;
	int write = 0;
	
	FILE *fpi = fopen(argv[1], "r");
	if(fpi == NULL){
		printf("File not found.");
		return -1;
	}
	
	FILE *fpo = fopen(argv[2], "w");
	if(fpo == NULL){
		printf("File not found.");
		return -1;
	}
	
	while (fscanf(fpi,"%f",&buffer[write++]) == 1){
		if(write  >= bufferSize){
			write = 0;
		}
		if(buffer[bufferSize-1] != 0){
			for(int j = 0; j < bufferSize; j++){
				avg += buffer[j];
			}	
			avg /= bufferSize;
			fprintf(fpo,"%f\n",avg);
			numValOut++;
			avg = 0;
			
		}
			
		numValIn++;
	}
	printf("Input file contains %d values\n",numValIn);
	printf("Wrote %d values to output file\n",numValOut);
	

	fclose(fpo);
	fclose(fpi);
	free(buffer);

	return 0;
}
