from ev3dev.ev3 import LargeMotor, MediumMotor
from time import sleep


class CubeInTheShell(object):

	def __init__(self, motor_y, motor_x, motor_l):
		self._my = LargeMotor(motor_y)
		self._mx = MediumMotor(motor_x)
		self._ml = LargeMotor(motor_l)
		self._locked = False
		self._sa = 'hold'
		self._facing = 0
		self._facing_dict = {"F": -90, "R": 0, "B": 90, "L": 180}

	def reset_motors(self):
		self._my.position = 0
		self._mx.position = 0
		self._ml.position = 0

	def lock(self, speed=200):
		self._ml.run_to_abs_pos(position_sp=0 if self._locked else 180, speed_sp=speed, stop_action=self._sa)
		self._locked = not self._locked
		sleep(1)

	def turn_x(self, direction=1, speed=200):
		self.lock()
		self._mx.run_to_abs_pos(position_sp=-100*direction, speed_sp=speed, stop_action=self._sa)
		sleep(1)
		self.lock()
		self._mx.run_to_abs_pos(position_sp=0, speed_sp=speed, stop_action=self._sa)
		sleep(1)

	def turn_y(self, direction=1, repeat=1, speed=200):
		angle = (180 if repeat == 2 else 90) * 40 / 24
		angle *= -3 if direction == -1 else -1
		while angle < -360*40/24:
			angle += 360*40/24
		self._my.run_to_rel_pos(position_sp=angle, speed_sp=speed, stop_action=self._sa)
		sleep(abs(angle/90/40*24))

	def turn(self, move):
		direction = -1 if "'" in move else 1
		repeat = 2 if "2" in move else 1
		if "U" in move:
			self.lock()
			self.turn_y(direction, repeat)
			self.lock()
		elif "Y" in move:
			self.turn_y(direction, repeat)
		elif "X" in move:
			self.turn_x(direction)
		else:
			angle = self._facing_dict[move[0]] - self._facing
			self._facing = self._facing_dict[move[0]]
			if angle != 0:
				if angle >= 180:
					angle -= 360
				elif angle <= 180:
					angle += 360
				self.turn_y(1 if angle > 0 else -1, int(abs(angle/90)))
			for i in range(repeat):
				self.turn_x(direction)

	def turn_formula(self, formula):
		for move in formula:
			self.turn(move)
