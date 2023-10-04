#!/usr/bin/python3

def isEven(x):
    return (x%2) == 0

def isPrime(x):
	i = 2
	while i < x:
		if x%i == 0:
			return False
		i+=1
	return True

def numbers():
    for i in range(1,21):
        even = "odd"
        prime = "composite"
        if isEven(i):
            even = "even"
        if isPrime(i):
            prime = "prime"
        print("{:d}\t{:s}\t{:s}".format(i,even,prime))

def main():
    if len(sys.argv) < 2:
		s = input("Please enter an integer: ").split()
	else:
		s = sys.argv[1:]

	for i in s:
		try:
			i = int(i)
		except ValueError as e:
			raise Exception(
			"{:s} is not an integer, please try again".format(i)

	numbers()

if __name__ == "__main__":
    try:
		main()
	except Exception as e:
		print(e)
