#include "hw12_lib.h"
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

struct person* head = NULL;
struct person* tail = NULL;

bool addPerson(const char* name, const char *father, const char *mother){	
	struct person* newPerson = malloc(sizeof(struct person));
	strncpy(newPerson->name,name,sizeof(newPerson->name));
	strncpy(newPerson->father,father,sizeof(newPerson->father));
	strncpy(newPerson->mother,mother,sizeof(newPerson->mother));
	
	if(head == NULL){
		head = newPerson;
		newPerson->prev = NULL;
	}

	else{
		tail->next = newPerson;	
		newPerson->prev = tail;
		}
	newPerson->next = NULL;
	tail = newPerson;	
	return true;
}

bool load(const char *filename){
	char name[30];
	char father[30];
	char mother[30];
	FILE *fp = fopen(filename,"r");
	if(fp == NULL){
		printf("File not found");
		return false;
	}
	while(fscanf(fp, "%s%s%s", name, father, mother) == 3){
		addPerson(name,father,mother);
	}
	fclose(fp);
	return true;
}

void printMaleAncestor(int gen, const char *name){
	if(gen == 0)
		printf("father %s\n",name);
	else{
		for(int i = 1; i< gen; i++){
			printf("great ");	
		}
		printf("grandfather %s\n",name);
	}
	
}

void printFemaleAncestor(int gen, const char *name){
	if(gen == 0)
		printf("mother %s\n",name);
	else{
		for(int i = 1; i< gen; i++){
			printf("great ");	
		}
		printf("grandmother %s\n",name);
	}
}

void printDescendant(int gen, const char *name){
	if(gen == 0)
		printf("child %s\n",name);
	else{
		for(int i = 1; i< gen; i++){
			printf("great ");	
		}
		printf("grandchild %s\n",name);
	}
}

bool printAncestors(int gen, const char *name){
	struct person* p = findPerson(head,name);	
	if(p != NULL){
		if(strcmp(p->father,"NULL")){
			printMaleAncestor(gen,p->father);
			printAncestors(++gen,p->father);
		}
		else
			return false;
		if(strcmp(p->mother, "NULL")){
			printFemaleAncestor(gen-1,p->mother);
			printAncestors(gen,p->mother);
			}
		return true;
	}
	return false;
}

bool printDescendants(int gen, const char *name){
	struct person* p = findDescendant(head,name);
	while(findDescendant(p,name)){
		printDescendant(gen,p->name);
		printDescendants(gen+1,p->name);
		p = findDescendant(p->next,name);
	}
	return true;

}

struct person* findDescendant(struct person* p, const char* name){
	if(p != NULL){
		if(strcmp(p->father,name)==0 || strcmp(p->mother,name)==0){
			return p;	
		}
		if(p->next != NULL){
			return findDescendant(p->next,name);
		}
		
	}
	return NULL;
}

struct person* findPerson(struct person* p,const char *name){
	if(p != NULL){
		if(strcmp(p->name,name)==0){
			return p;	
		}

		if(p->next != NULL){
			return findPerson(p->next,name);
		}
	}
	return NULL;
}

