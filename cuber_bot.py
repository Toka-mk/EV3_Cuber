from ev3dev.ev3 import LargeMotor, MediumMotor
from time import sleep

motor_y = LargeMotor('outA')
motor_x = MediumMotor('outB')
motor_lock = LargeMotor('outC')

locked = False
stop_action = 'brake'


def reset_motors():
	motor_y.position = 0
	motor_x.position = 0
	motor_lock.position = 0


def lock():
	global locked
	motor_lock.run_to_abs_pos(position_sp=0 if locked else 180, speed_sp=200, stop_action=stop_action)
	locked = not locked
	sleep(1)


def x_turn(cw=1, speed=200):
	lock()
	motor_x.run_to_abs_pos(position_sp=(-100 if cw else 100), speed_sp=speed, stop_action=stop_action)
	sleep(1)
	lock()
	motor_x.run_to_abs_pos(position_sp=(-5 if cw else 0), speed_sp=speed, stop_action=stop_action)
	sleep(1)


def y_turn(face='Y', speed=200,):
	if 'U' in face:
		lock()
	angle = (180 if '2' in face else 90)*40/24
	angle *= -3 if "'" in face else -1
	motor_y.run_to_rel_pos(position_sp=angle, speed_sp=speed, stop_action=stop_action)
	sleep(angle / -90 / 2)
	if 'U' in face:
		lock()


if __name__ == '__main__':
	y_turn("U")
	x_turn()
	y_turn("Y2")
	x_turn(0)
	sleep(5)
	x_turn()
	y_turn("Y2")
	x_turn(0)
	y_turn("U'")
