#include "hw11_lib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void){
	char cmd;
	char name[30];
	int n = 0;
	char str[30];
	do{
		printf("> ");
		fgets(str,sizeof(str),stdin);
		n = sscanf(str,"%c%s",&cmd,name);	
		switch(cmd){
			case 'g':
				if(n == 2){
					printf("%.2f\n",studentGetGrade(name));
				}
				if(n == 1){
					printf("%.2f\n",studentAverageGrade());		
				}
				break;
			case 'r':
				if(n == 2){
					studentRemove(name);				
				}
				else{
					printf("Error,incorrect input");
				}
				break;
			case 'p':
				studentPrintList();
				break;
			case 'c':
				printf("%d\n",studentCount());
				break;
			case 'd':
				studentDeleteList();
				break;
			case 'l':
				if(n ==2){
					studentLoad(name);
				}
				else{
					printf("Error,incorrect input");
				}
				break;
			case 'q':
				break;
			default:
				printf("Invalid command");
			
		}
	}while(cmd != 'q');

	return 0;
}
