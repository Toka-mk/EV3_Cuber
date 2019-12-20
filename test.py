from rubik_solver import utils
from cube import *

c = Cube()
c.scramble(30)
print(c)
c.print_graph()

solve = utils.solve(c.__str__())
print(solve)

for move in solve:
	c.turn(move.raw)
c.print_graph()
