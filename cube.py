import random


# color
w = 'w'
r = 'r'
g = 'g'
b = 'b'
o = 'o'
y = 'y'

# orientation
X = 0  # right
Y = 1  # top
Z = 2  # front

# face
F = 'F'
B = 'B'
R = 'R'
L = 'L'
U = 'U'
D = 'D'


class Cubie(object):
	# a piece that has 0 or 1 or 2 or 3 colored surfaces

	# cx, cy, cz represent the color in the x, y, z direction respectively
	def __init__(self, cx, cy, cz):
		self.colors = [cx, cy, cz]

	def __str__(self):
		return '[' + ''.join(c if c else ' ' for c in self.colors) + ']'

	# rotate the piece around an axis
	def rotate(self, axis):
		if axis == X:
			self.colors = [self.colors[X], self.colors[Z], self.colors[Y]]
		elif axis == Y:
			self.colors = [self.colors[Z], self.colors[Y], self.colors[X]]
		elif axis == Z:
			self.colors = [self.colors[Y], self.colors[X], self.colors[Z]]

	# change the surface colors without changing orientation
	def update_colors(self, new_color):
		self.colors = new_color


class Cube(object):
	"""
	a rubik's cube represented by 27 Piece objects in a list arranged in the following order:

	front		middle		back
	0  1  2		9  10 11	18 19 20
	3  4  5		12 13 14	21 22 23
	6  7  8		15 16 17	24 25 26

	six lists (_front, _back, _left, etc.) store the pieces on their respective face
	starting from the top-left and continues clock-wise,
	with the center piece at the end of the list
	e.g.: _front = [0, 1, 2, 5, 8, 7, 6, 3, 4]
	"""

	# initialize a cube in the solved state
	def __init__(self, state=None):
		self._orientation = [X, Y, Z]
		self._state = []

		if not state:
			for i in range(27):
				cx = cy = cz = None

				if i % 3 == 0:  # left
					cx = b
				elif i % 3 == 2:  # right
					cx = g
				if i < 9:  # front
					cz = r
				elif i > 17:  # back
					cz = o
				if i % 9 < 3:  # up
					cy = y
				elif i % 9 > 5:  # down
					cy = w

				self._state.append(Cubie(cx, cy, cz))

		self._front = [self._state[i] for i in (0, 1, 2, 5, 8, 7, 6, 3, 4)]
		self._back = [self._state[i] for i in (20, 19, 18, 21, 24, 25, 26, 23, 22)]
		self._left = [self._state[i] for i in (18, 9, 0, 3, 6, 15, 24, 21, 12)]
		self._right = [self._state[i] for i in (2, 11, 20, 23, 26, 17, 8, 5, 14)]
		self._up = [self._state[i] for i in (18, 19, 20, 11, 2, 1, 0, 9, 10)]
		self._down = [self._state[i] for i in (6, 7, 8, 17, 26, 25, 24, 15, 16)]
		self._equator = [self._state[i] for i in (3, 4, 5, 14, 23, 22, 21, 12, 13)]

		self._face_dict = {
			F: (self._front, Z), B: (self._back, Z),
			L: (self._left, X), R: (self._right, X),
			U: (self._up, Y), D: (self._down, Y)
		}

	def __str__(self):
		line = ''
		for face in (U, L, F, R, B, D):
			line += self.get_face(face)
		return line

	def graph(self, p=True):
		graph = ''
		line = self.__str__()
		for i in range(3):
			graph += '         '
			for color in [x for x in line[i*3:i*3+3]]:
				graph += ' ' + color + ' '
			graph += '\n'
		for i in range(3):
			for j in range(4):
				for color in [x for x in line[j*9+i*3+9:j*9+i*3+12]]:
					graph += ' ' + color + ' '
			graph += '\n'
		for i in range(3):
			graph += '         '
			for color in [x for x in line[i*3+45:i*3+48]]:
				graph += ' ' + color + ' '
			graph += '\n'
		if p:
			print(graph)
		else:
			return graph

	# return a string consisting of colors of a face
	def get_face(self, face, side=False):
		face_s = self._face_dict[face][0]
		if not side:
			axis = self._face_dict[face][1]
			return ''.join(face_s[i].colors[axis] for i in (0, 1, 2, 7, 8, 3, 6, 5, 4))
		else:
			# for i, cubie in enumerate(face_s):
			re = ''
			for i in range(0, 8, 2):
				axis = X if i % 4 == 2 else Z
				for j in range(3):
					# print(i, j, axis, face_s[i+j].colors)
					re += face_s[i+j if i+j < 8 else 0].colors[axis]
			return re

	def is_solved(self):
		for face in self._face_dict.keys():
			face_s = self.get_face(face)
			c = face_s[0]
			for i in face_s[1:]:
				# print(i)
				if i != c:
					return False
		return True

	def turn(self, face):
		if 'Y' in face:
			self.rotate_y(False if "'" in face else True)
			if '2' in face:
				self.rotate_y(False if "'" in face else True)
			return

		shift = 2 if "'" in face else -2
		face_s = self._face_dict[face[0]][0]
		axis = self._face_dict[face[0]][1]
		face_ref = [face_s[(i + shift) % 8].colors for i in range(8)]
		for color, color_new in zip(face_s[:-1], face_ref):
			color.update_colors(color_new)
			color.rotate(axis)

		if '2' in face:
			self.turn(face[:-1])

	def turn_formula(self, formula):
		for move in formula:
			self.turn(move)

	def rotate_y(self, cw=True):
		shift = 0;
		if cw:
			self.turn(U)
			self.turn("D'")
			shift = 2
		else:
			self.turn("U'")
			self.turn(D)
			shift = -2
		cubies = self._equator
		cubies_ref = [cubies[(i + shift) % 8].colors for i in range(8)]
		for color, color_new in zip(cubies[:-1], cubies_ref):
			color.update_colors(color_new)
			color.rotate(Y)

	def scramble(self, turns=10):
		p = []
		for i in range(turns):
			move = random.choice(list(self._face_dict.keys()))
			move += random.choice(["'", ''])
			self.turn(move)
			p.append(move)
		return p


if __name__ == '__main__':
	c1 = Cube()
	c1.graph()
	print('solved\n' if c1.is_solved() else 'not solved')
	print(' '.join(x for x in c1.scramble()))
	print(c1.get_face(U, True))
	c1.graph()
	print(c1)
	print('solved' if c1.is_solved() else 'not solved')
