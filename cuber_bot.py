# from solution import *
from Cube_in_the_Shell import *


rc = CubeInTheShell('outA', 'outB', 'outC')
# mv_c = Cube()


# def scramble():
# 	scram = v_c.scramble()
# 	print(scram)
# 	r_c.turn_formula(scram)


# def solve(colors=None):
# 	if colors:
# 		v_c.read(colors)
# 	r_c.turn_formula(solve(v_c))


def main():
	move = ["U", "X", "Y", "X'", "U"]
	move_reverse = ["U'", "X", "Y'", "X'", "U'"]
	rc.turn_formula(move)
	sleep(3)
	rc.turn_formula(move_reverse)
	# scramble()
	# solve()


if __name__ == '__main__':
	main()
