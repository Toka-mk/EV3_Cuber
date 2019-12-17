
# color
w = 'w'
r = 'r'
g = 'g'
b = 'b'
o = 'o'
y = 'y'


# orientation
ax = 0  # right
ay = 1  # top
az = 2  # front


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
		self._set_type()

	def __str__(self):
		return '[' + self.type + '	' + ''.join(c if c else 'X' for c in self.colors) + ']'

	# determine if this is a corner, an edge, a face, or a center piece
	def _set_type(self):
		no_color = self.colors.count(None)
		if no_color == 2:
			self.type = 'face'
		elif no_color == 1:
			self.type = 'edge'
		elif no_color == 0:
			self.type = 'corner'
		else:
			self.type = 'center'

	# rotate the piece around an axis
	def rotate(self, axis):
		if axis == ax:
			self.colors = [self.colors[ax], self.colors[az], self.colors[ay]]
		elif axis == ay:
			self.colors = [self.colors[az], self.colors[ay], self.colors[ax]]
		elif axis == az:
			self.colors = [self.colors[ay], self.colors[ax], self.colors[az]]

	# change the surface colors without changing orientation
	def update_surface(self, cx, cy, cz):
		self.colors = [cx, cy, cz]


class Cube(object):
	# a rubik's cube represented by 27 Piece object in a list

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
		self._update()

	def _update(self):
		self._front = [self._state[i] for i in range(9)]
		self._back = [self._state[i] for i in range(18, 27)]
		self._left = [self._state[i] for i in range(0, 27, 3)]
		self._right = [self._state[i] for i in range(2, 27, 3)]
		self._up = [self._state[i] for i in range(27) if i % 9 < 3]
		self._down = [self._state[i] for i in range(27) if i % 9 > 5]

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
		if face == F:
			return ''.join(piece.colors[az] for piece in self._front)
		elif face == B:
			return ''.join(piece.colors[az] for piece in self._back)
		elif face == L:
			return ''.join(piece.colors[ax] for piece in self._left)
		elif face == R:
			return ''.join(piece.colors[ax] for piece in self._right)
		elif face == U:
			return ''.join(piece.colors[ay] for piece in self._up)
		elif face == D:
			return ''.join(piece.colors[ay] for piece in self._down)

	def _is_face_solved(self, face):
		face_s = self.get_face(face)
		c = face_s[0]
		for i in face_s:
			if i != c:
				return False
		return True

	def is_solved(self):
		for face in (F, B, L, R, U, D):
			if not self._is_face_solved(face):
				return False
		return True

	# def rotate(self, face):


if __name__ == "__main__":
	c1 = Cube()
	print(c1)
	print('solved' if c1.is_solved() else 'not solved')
