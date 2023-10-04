#include <stdio.h>
#include<stdbool.h>
struct person{
	char name[30];
	char father[30];
	char mother[30];
	struct person* next;
	struct person* prev;
};

bool addPerson(const char *name, const char *father, const char *mother);
bool load(const char *filename);
void printMaleAncestor(int gen, const char *name);
void printFemaleAncestor(int gen, const char *name);
void printDescendant(int gen, const char *name);
bool printAncestors(int gen, const char *name);
bool printDescendants(int gen ,const char *name);
//bool printSiblings(const char *name);
//bool printCousins(const char *name);
struct person* findDescendant(struct person* p,const char *name);
struct person* findPerson(struct person* p,const char *name);




