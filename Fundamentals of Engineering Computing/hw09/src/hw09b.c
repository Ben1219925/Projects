#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int rep(char* in, char* out, char* word, char* replace){
	int i = 0;
	int cnt = 0;
	int replaceLen = strlen(replace);
	int wordLen = strlen(word);
	
	while(in[i] != '\0'){
		if(strstr(&in[i],word) == &in[i]){
			cnt++;
			i += wordLen - 1;
		}
		i++;
	}
   	char* temp = (char*)malloc(i + cnt * (replaceLen - wordLen) + 1);
	i = 0;	
	while(*in){
		if(strstr(in, word) == in){
			strcpy(&temp[i],replace);
			i += replaceLen;
			in += wordLen;
		}
		else 
			temp[i++] = *in++;
	}
	temp[i] = '\0';
	sprintf(out,"%s",temp);
	free(temp);
	return cnt;
}

int main(){
	char fileName[30];
	char outFileName[30];
	char word[20];
	char replaceWord[20];
	char temp[100];
	char temp2[100];
	char str[7000];
	char* filePath;
	int cnt = 0;
	
	printf("Please enter a filename: ");
	scanf("%29s",fileName);

	FILE *fp = fopen(fileName,"r");
	if(fp == NULL){
		printf("File not found");
		return -1;
	}

	printf("Please enter a word to search for: ");
	scanf("%19s",word);

	printf("Please enter a word to replace it with: ");
	scanf("%19s",replaceWord);	
	
	while(!feof(fp)){
		fgets(temp,sizeof(temp),fp);
		int tempCnt = rep(temp, temp2, word, replaceWord);
		cnt += tempCnt;
		strcat(str,temp2);
	}
	fclose(fp);
	printf("The word %s was found %d times\n",word,cnt);
	filePath = strrchr(fileName, '/');
	if(filePath != NULL){
	strcpy(outFileName,filePath+1);
	}
	else{
		strcpy(outFileName,fileName);
	}

	char* outFileNamePtr = strtok(outFileName,".");	
	strcat(outFileNamePtr,".out");	
	FILE *ofp = fopen(outFileNamePtr,"w");
	if(ofp == NULL){
		printf("File not found");
		return -1;
	}
	str[strlen(str)-1] = '\0';
	fprintf(ofp,"%s",str);
	fclose(ofp);
	return 0;
}
