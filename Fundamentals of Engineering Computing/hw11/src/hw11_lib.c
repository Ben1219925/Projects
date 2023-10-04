#include "hw11_lib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct student* head = NULL;
struct student* tail = NULL;

void studentAdd(const char* name, const float* grade){
	struct student *newStudent = malloc(sizeof(struct student));
	strncpy(newStudent->name,name,sizeof(newStudent->name));
	newStudent->grade = *grade;
	//empty list
	if(head == NULL){
		head = newStudent;
		newStudent->prev = NULL;
	}
	else{
		tail->next = newStudent;	
		newStudent->prev = tail;
	}
	newStudent->next = NULL;
	tail = newStudent;
}

void studentRemove(const char* name){
	struct student *temp = studentFind(name);
	//only student
	if(tail == head){
		free(temp);
		head = NULL;
		tail = NULL;
	}
	//first student
	if(head == temp){
		head = temp->next;
		head->prev = NULL;
		free(temp);
	}
	//last student
	if(tail == temp){
		tail = temp->prev;
		tail->next = NULL;
		free(temp);
	}
	else{
		temp->prev->next = temp->next;
		temp->next->prev = temp->prev;
		free(temp);
	}
}

struct student* studentFind(const char* name){
	struct student *temp = head;
	while(temp!=NULL){
		if(strcmp(temp->name,name)==0){
			return temp;	
		}
		temp = temp->next;
	}
	return NULL;	
}

void studentPrint(struct student* s){
	printf("%s\t%.2f\n",s->name,s->grade);
}

void studentPrintList(){
	if(head == NULL){
		printf("List is empty\n");
	}
	else{
		struct student *temp = head;
		while(temp != NULL){
			studentPrint(temp);
			temp = temp->next;
		}
	}
}

float studentGetGrade(const char* name){
	struct student* s = studentFind(name);
	if(s != NULL){
		return s->grade;
	}
	return 0;
}

 void studentLoad(const char* filename){
	char name[30];
	float grade;
	FILE *fp = fopen(filename,"r");
	if(fp == NULL){
		printf("File not found");
	}
	while(fscanf(fp, "%s%f",name,&grade) == 2){
		studentAdd(name,&grade);
	}
	fclose(fp);	
}

int studentCount(){
	int count = 0;
	struct student *temp = head;
	while(temp != NULL){
		count++;
		temp = temp->next;
	}
	return count;
}

void studentDeleteList(){
	struct student* temp = head;
	while(head != NULL){
		temp = head;
		head = head->next;
		free(temp);
	}
	tail = NULL;	
	head = NULL;
}

float studentAverageGrade(){
	int num = studentCount();
	float avg = 0;
	struct student* temp = head;
	if(head == NULL){
		return 0;
	}
	for(int i =0;i < num;i++){
		avg += temp->grade;
		temp = temp->next;
	}
	return avg/num;
}



