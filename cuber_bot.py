from solution import *
from Cube_in_the_Shell import *


r_c = CubeInTheShell()
v_c = Cube()


def scramble():
	scram = v_c.scramble()
	print(scram)
	r_c.turn_formula(scram)


def solve(colors=None):
	if colors:
		v_c.read(colors)
	r_c.turn_formula(solve(v_c))


def main():
	scramble()
	solve()


if __name__ == '__main__':
	main()
