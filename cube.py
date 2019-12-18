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


class Piece(object):
	# a piece that has 0 or 1 or 2 or 3 colored surfaces

	# cx, cy, cz represent the color in the x, y, z direction respectively
	def __init__(self, cx, cy, cz):
		self.colors = [cx, cy, cz]

	def __str__(self):
		return '[' + ''.join(c if c else 'X' for c in self.colors) + ']'

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
	a rubik's cube represented by 27 Piece object in a list arranged in the following order:

	 front		 middle		 back
	0  1  2		9  10 11	18 19 20
	3  4  5		12 13 14	21 22 23
	6  7  8		15 16 17	24 25 26

	six lists (_front, _back, _left, etc.) that store the pieces on a specific face
	starting from the top-left and continues clock-wise,
	with the center piece at the end of the list
	e.g.: _front = [0, 1, 2, 5, 8, 7, 6, 3, 4]

	"""

	# initialize a cube in the solved state
	def __init__(self):
		self._state = []
		for i in range(27):
			cx = cy = cz = None

			if i % 3 == 0:
				cx = g
			elif i % 3 == 2:
				cx = b
			if i < 9:
				cz = r
			elif i > 17:
				cz = o
			if i % 9 < 3:
				cy = w
			elif i % 9 > 5:
				cy = y

			self._state.append(Piece(cx, cy, cz))

		#
		self._front = [self._state[i] for i in (0, 1, 2, 5, 8, 7, 6, 3, 4)]
		self._back = [self._state[i] for i in (20, 19, 18, 21, 24, 25, 26, 23, 22)]
		self._left = [self._state[i] for i in (18, 9, 0, 3, 6, 15, 24, 21, 12)]
		self._right = [self._state[i] for i in (2, 11, 20, 23, 26, 17, 8, 5, 14)]
		self._up = [self._state[i] for i in (18, 19, 20, 11, 2, 1, 0, 9, 10)]
		self._down = [self._state[i] for i in (6, 7, 8, 17, 26, 25, 24, 15, 16)]

		self._face_dict = {
			F: (self._front, Z), B: (self._back, Z),
			L: (self._left, X), R: (self._right, X),
			U: (self._up, Y), D: (self._down, Y)
		}

	def __str__(self):
		re = ''
		for i in range(27):
			re += str(self._state[i])
			if i % 3 == 2:
				re += '\n'
			else:
				re += ' || '
			if i % 9 == 8:
				re += '\n'
		return re

	# return a string consisting of colors of a face
	def get_face(self, face):
		face_s = self._face_dict[face][0]
		axis = self._face_dict[face][1]
		return ''.join(piece.colors[axis] for piece in face_s)

	def is_solved(self):
		for face in (F, B, L, R, U, D):
			face_s = self.get_face(face)
			c = face_s[-1]
			for i in face_s:
				# print(i)
				if i != c:
					return False
		return True

	def rotate(self, face):
		shift = 2 if '\'' in face else -2
		face_s = self._face_dict[face[0]][0]
		axis = self._face_dict[face[0]][1]
		face_ref = [face_s[(i + shift) % 8].colors for i in range(8)]
		for i in range(8):
			face_s[i].update_colors(face_ref[i])
			face_s[i].rotate(axis)


if __name__ == "__main__":
	c1 = Cube()
	print(c1)
	print('solved' if c1.is_solved() else 'not solved')
