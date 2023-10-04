#ifndef HW_LIB_H
#define HW_LIB_H

struct student {
	struct student* next;
	struct student* prev;
	char name[50];
	float grade;
};

void studentAdd(const char* name, const float* grade);
void studentRemove(const char* s);
struct student* studentFind(const char* name);
void studentPrint(struct student* s);
void studentPrintList();
float studentGetGrade(const char* name);
void studentLoad(const char* filename);
int studentCount();
void studentDeleteList();
float studentAverageGrade();
#endif
