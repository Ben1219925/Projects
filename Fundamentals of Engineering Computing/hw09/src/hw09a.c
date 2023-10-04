#include <stdio.h>
#include <string.h>


int main(int argc, char **argv){
	const char str[] = "The quick brown fox jumps over the lazy dog!";
	printf("The string is %ld characters long\n", strlen(str));
	printf("The letter z is at index %ld\n",strchr(str,'z')-str);
	
	char editStr[80];
	strcpy(editStr,str);
	char* word = strtok(editStr," ");
	for(int i = 0; i < 2; i++){
		word = strtok(NULL," ");
		if (word == NULL){
			printf("Not enough words!\n");
			return -1;
		}
	}
	printf("The third word is %s\n",word);
	char temp[80];
	strcpy(temp,str);
	char* jumps = strstr(temp, "jumps");
	char* afterJump = strtok(jumps, " ");
	afterJump = strtok(NULL, " ");
	printf("The word after jumps is %s\n",afterJump);
	
	char str2[] = "Mary had a little lamb.";
	char spaces[] = "  ";
	char newString[80];
	strcpy(newString, str);
	
	strcpy(newString,strcat(newString,spaces));
	strcpy(newString,strcat(newString,str2));
	printf("%s\n",newString);


	return 0;
}
