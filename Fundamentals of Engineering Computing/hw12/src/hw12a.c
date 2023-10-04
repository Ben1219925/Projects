#include <stdio.h>

int factorial(int num){
	if (num == 0)
		return 1;
	return num*factorial(num-1);
}


int main(int argc, char **argv){
	if(argc < 2){
		printf("Error, no number entered");
		return -1;
	}
	int num;
	sscanf(argv[1],"%d", &num);

	if(num >=0 && num <= 10)
		printf("%d\n",factorial(num));
	else
		printf("Invalid input\n");

	return 0;
}
