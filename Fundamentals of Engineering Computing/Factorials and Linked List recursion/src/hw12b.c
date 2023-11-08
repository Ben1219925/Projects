#include <stdio.h>
#include "hw12_lib.h"


int main(int argc, char **argv){
	load(argv[1]);
	printf("Ancestors of %s: \n",argv[2]);
	printAncestors(0,argv[2]);
	printf("Descendants of %s: \n",argv[2]);
	printDescendants(0,argv[2]);



	return 0;
}
