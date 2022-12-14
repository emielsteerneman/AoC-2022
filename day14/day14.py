import re
import numpy as np
import cv2

def show_cave(cave, timeout=0):
	H, W = cave.shape
	D = int(H*1.2)
	r = int(min(1920/(D*2), 1080/H))
	cave_ = cv2.resize(cave[:, 500-D:500+D], (D*2*r, H*r), interpolation=cv2.INTER_NEAREST)
	cv2.imshow("Cave", cave_ * 127)
	if cv2.waitKey(timeout) == 27:
		exit()

def move(cave, y, x, y_limit):
	# Add sand
	cave[y, x] = 2
	# Down, down left, down right
	coords = [ np.s_[y+1,x], np.s_[y+1,x-1], np.s_[y+1,x+1] ]

	for coord in coords:
		y_, x_ = coord
		# Sand has reached depth limit
		if y_limit <= y_: 
			cave[y, x] = 0
			return False, [-1, -1]
		# Free to move		
		if cave[coord] == 0:
			cave[y, x] = 0
			cave[coord] = 2
			return True, [y_, x_]
	# Sand can't move
	return True, [y, x]

def run(cave, spawn_y, spawn_x, y_limit, draw, draw_timeout=20):
	sand_y, sand_x = spawn_y, spawn_x
	running = True
	while running:
		# Move piece of sand
		running, [sand_y_, sand_x_] = move(cave, sand_y, sand_x, y_limit)
		# Sand is filled up all the way to the spawn point
		if [sand_y_, sand_x_] == [spawn_y, spawn_x]: break

		# Sand didn't move, reset it
		if sand_y == sand_y_:
			sand_y, sand_x = spawn_y, spawn_x
		# Sand moved, update it
		else:
			sand_y, sand_x = sand_y_, sand_x_
		
		if draw: show_cave(cave, draw_timeout)

	return cave

walls_str = open("input.txt").read().splitlines()
walls = []

maxy = 0

# Parse all walls and find cave depth
for p in walls_str:
	# Find all numbers, parse, and turn into pairs
	ints = list(map( int, re.findall(r'\d+', p) ))
	coords = np.array(list(zip(ints[::2], ints[1::2])))
	walls.append(coords)
	# Update  cave depth
	maxy = max([ y for _, y in coords ] + [maxy])

# Define floor width and depth
floor_xfrom, floor_xto = 500-maxy-30, 500+maxy+30
floor_y = maxy+2

# Add floor
walls.append(np.array([[floor_xfrom, floor_y], [floor_xto, floor_y]]))
minx, maxx = floor_xfrom - 2, floor_xto + 2
# Create cave
cave = np.zeros( (floor_y+5, 1000), dtype=np.uint8 )
# Fill cave using CV2.line
for p in walls:
	for a, b in list(zip(p, p[1::])):
		cv2.line(cave, a, b, 1)

# Run simulations
cave1 = run(np.copy(cave), 0, 500, floor_y-1, False)
cave2 = run(np.copy(cave), 0, 500, floor_y+1, False)

part1 = np.sum(cave1 == 2)
part2 = np.sum(cave2 == 2)

print("Part 1:", part1) # 737
print("Part 2:", part2) # 28145