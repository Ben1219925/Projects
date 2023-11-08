#!/usr/bin/python3
import sys
import sympy as sp


def solve(Kn,VDD,Vg,Vtn=1,lam=0):
	Id,Vo,Vs = sp.symbols("Id Vo Vs")
	s=sp.solve((Kn*(VDD-Vo-Vtn)**2 * (1+lam*(VDD-Vo))-Id,
				Kn*(Vg-Vs-Vtn)**2 * (1+lam*(Vo-Vs))-Id,
				Kn*(Vs-Vtn)**2 * (1+lam*Vs)-Id),
				(Id,Vo,Vs))
	for v in s:
		Id=float(sp.re(v[0]))
		Vo=float(sp.re(v[1]))
		Vs=float(sp.re(v[2]))
		if Id>0 and Vo>0 and Vo<VDD and Vs>0:
			return (Id,Vo,Vs)
	
	raise ValueError("No solution found")
	
def main():
	try:	
		Kn = float(sys.argv[1])
		Vdd = float(sys.argv[2])
		Vg = float(sys.argv[3])
		if len(sys.argv) == 4:
			Id,Vo,Vs = solve(Kn,Vdd,Vg)
		elif len(sys.argv) == 5:
			Vtn = float(sys.argv[4])
			Id,Vo,Vs = solve(Kn,Vdd,Vg,Vtn)
		else:
			Vtn = float(sys.argv[4])
			LambdaT = float(sys.argv[5])
			Id,Vo,Vs = solve(Kn,Vdd,Vg,Vtn,LambdaT)
	except ValueError as e:
		print(e)
		return -1	
	print("Id={:.2e} Vo={:.2e} Vs={:.2e}".format(Id,Vo,Vs))

if __name__ == "__main__":
	main()
