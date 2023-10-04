#!/usr/bin/python3

def array():
	students = {"Larry":75, "Moe":85, "Curly":65, "Sleepy":48, "Happy":98}
	return students
	
def main():
	students = array()
	for s in sorted(students):
		print("{:s}\t{:d}".format(s,students[s]))
	
	for s in sorted(students.items(), key = lambda item:item[1]):
		print("{:s}\t{:d}".format(s[0],s[1]))

if __name__ == "__main__":
	main()
