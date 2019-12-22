from cube import *
from rubik_solver.utils import solve as f2lsolve


def compare_color(s1, s2, color=y):
	for i, j in zip(s1, s2):
		if [i, j].count(color) == 1:
			return False
	return True


def f2l(cube):  # F2L using rubik_solver
	moves = [x.raw for x in f2lsolve(cube.__str__())]
	cube.turn_formula(moves)
	return moves


def yellow_cross(cube):
	moves = []
	formula = ("F", "R", "U", "R'", "U'", "F'")
	top = cube.get_face(U)

	if all(top[i] != y for i in (1, 3, 5, 7)):  # if no yellow other than center
		cube.turn_formula(formula)
		moves += formula
		top = cube.get_face(U)

	while not all(top[i] == y for i in (1, 3, 5, 7)):  # while top cross not reached
		# print(cube.get_face(U))
		while top[3] != y or not (top[1] == y or top[5] == y):
			cube.turn(U)
			moves.append(U)
			top = cube.get_face(U)
		cube.turn_formula(formula)
		moves += formula
		top = cube.get_face(U)
	return moves


def oll(cube):
	moves = []

	formulas = {
		'y  y y  y   ': ["L", "U'", "R'", "U", "L'", "U", "R", "U", "R'", "U", "R"],
		'   y y   y y': ["R", "U", "R'", "U", "R", "U'", "R'", "U", "R", "U2", "R'"],
		'  y     y  y': ["L'", "U", "R", "U'", "L", "U", "R'"],
		'y  y     y  ': ["R'", "U2", "R", "U", "R'", "U", "R"],
		'  y   y     ': ["R'", "F'", "L", "F", "R", "F'", "L'", "F"],
		'  y      y  ': ["R'", "F'", "L'", "F", "R", "F'", "L", "F"],
		'y y         ': ["R'", "U'", "R", "U'", "R'", "U'2", "R"]
	}

	while cube.get_face(U) != 'yyyyyyyyy':
		for pattern in formulas.keys():
			if compare_color(cube.get_face(U, True), pattern):
				formula = formulas[pattern]
				cube.turn_formula(formula)
				moves += formula
				break
		cube.turn(U)
		moves.append(U)

	return moves


def count_side_pairs(t_side):
	pairs = 0
	pos = 0
	for i in range(0, 12, 3):
		if t_side[i] == t_side[i+2]:
			pairs += 1
			pos = int(i / 3)
	return pairs, pos


def count_correct_edge(t_side):
	edge = 0
	pos = 0
	for i in range(0, 12, 3):
		if t_side[i] == t_side[i+1]:
			edge += 1
			pos = int(i / 3)
	return edge, pos


def pll(cube):
	moves = []
	pairs, pos = count_side_pairs(cube.get_face(U, True))

	while pairs < 4:
		formula = ["L'", "B", "L'", "F2", "L", "B'", "L'", "F2", "L2"]

		if pairs == 1:
			p_form = ["U2", "U", None, "U'"]
			p_move = p_form[pos]
			if p_move:
				cube.turn(p_move)
				moves.append(p_move)

		cube.turn_formula(formula)
		moves += formula
		pairs, pos = count_side_pairs(cube.get_face(U, True))

	edge, pos = count_correct_edge(cube.get_face(U, True))
	while edge < 4:
		formula = ["R", "U'", "R", "U", "R", "U", "R", "U'", "R'", "U'", "R2"]

		if edge == 1:
			p_form = [None, "U'", "U2", "U"]
			p_move = p_form[pos]
			if p_move:
				cube.turn(p_move)
				moves.append(p_move)

		cube.turn_formula(formula)
		moves += formula
		edge, pos = count_correct_edge(cube.get_face(U, True))

	while not cube.is_solved():
		cube.turn(U)
		moves.append(U)

	return moves


def simplify(s):
	for i in range(0, len(s) - 1):
		if i >= len(s) - 1:
			break
		if s[i][0] == s[i + 1][0] and (s[i] + s[i + 1]).count("'") == 1:
			del s[i]
			del s[i]
			i -= 1
	for i in range(0, len(s) - 1):
		if i >= len(s) - 1:
			break
		if s[i] == s[i + 1]:
			if i + 2 < len(s) and s[i] == s[i + 2]:
				del s[i]
				del s[i]
				if "'" in s[i]:
					s[i] = s[i].replace("'", "")
				else:
					s[i] += "'"
			else:
				del s[i]
				if "2" in s[i]:
					del s[i]
					i -= 1
				else:
					s[i] += "2"


def solve(cube):
	s = f2l(cube) + yellow_cross(cube) + oll(cube) + pll(cube)
	simplify(s)
	return s


def main():
	c = Cube()
	d = Cube()
	scram = c.scramble(20)
	simplify(scram)
	print('  '.join(x for x in scram))
	d.turn_formula(scram)
	d.graph()
	solution = solve(c)
	print('  '.join(x for x in solution))
	d.turn_formula(solution)
	d.graph()


if __name__ == '__main__':
	main()
