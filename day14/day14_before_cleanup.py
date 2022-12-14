import re
import numpy as np
import cv2

paths_str = open("input.txt").read().splitlines()
paths = []

minx, maxx, miny, maxy = np.inf, 0, np.inf, 0

for p in paths_str:
	ints = list(map( int, re.findall(r'\d+', p) ))
	coords = np.array(list(zip(ints[::2], ints[1::2])))

	minx, maxx, miny, maxy = \
	min([ x for x, _ in coords ] + [minx]), \
	max([ x for x, _ in coords ] + [maxx]), \
	min([ y for _, y in coords ] + [miny]), \
	max([ y for _, y in coords ] + [maxy])

	paths.append(coords)

minxy, maxxy = np.array([minx, 0]), np.array([maxx, maxy])

print(minxy, maxxy, maxxy - minxy)
exit()
for p in paths: p -= minxy - [5, 0]
for p in paths: print(p.tolist())

cave = np.zeros( (maxxy - minxy + [10,5])[::-1], dtype=np.uint8 )

for p in paths:
	for a, b in list(zip(p, p[1::])):
		# m = np.argmin([ sum(ab[0]), sum(ab[1]) ])
		# print()
		# print(ab, ab[m], ab[1-m])
		cv2.line(cave, a, b, 1)

		# print(cave)

H, W = cave.shape


sand_y, sand_x = 0, 500 - minx + 5

cave_ = np.copy(cave)
cave[sand_y, sand_x] = 2

cave_ = cv2.resize(cave, (W*4, H*4), interpolation=cv2.INTER_NEAREST)
cv2.imshow("image",  cave_ * 127)
cv2.waitKey()

def move(cave, y, x):
	# print("[move]", [y,x])
	coords = [ np.s_[y+1,x], np.s_[y+1,x-1], np.s_[y+1,x+1] ]

	for coord in coords:
		y_, x_ = coord
		if H <= y_ or x_ < 0 or W <= x_:
			# print("[move]", coord, "out of bounds", (H, W))
			return False, [-1, -1]
		
		if 0 <= x_ and x_ < W:
			if cave[coord] == 0:
				# print("[move]", np.s_[y,x], "->", coord)
				cave[y, x] = 0
				cave[coord] = 2
				return True, [y_, x_]
	# print("[move]", np.s_[y,x], "can't move")
	return True, [y, x]

y, x = sand_y, sand_x
running = True
n_sand = 0
while running:
	try:
		running, [y_, x_] = move(cave, y, x)
		# print([y,x], "->", [y_, x_])
		
		# if False or 730 < n_sand and 150 < y:
		# 	cave_ = cv2.resize(cave, (W*10, H*10), interpolation=cv2.INTER_NEAREST)
		# 	cv2.imshow("image",  cave_ * 127)
		# 	if cv2.waitKey(200) == 27:
		# 		running = False

		if maxy+4 <= y_:
			print("DONE! maxy <= y_")
			break

		if [y_, x_] == [sand_y, sand_x]:
			print("DONE!")
			break

		if [y,x] == [y_, x_]:
			print("Rest!\n", H, W) # 171, 51
			y, x = sand_y, sand_x
			n_sand += 1

			if n_sand % 10 == 0:
				cave_ = cv2.resize(cave, (W*4, H*4), interpolation=cv2.INTER_NEAREST)
				cv2.imshow("image",  cave_ * 127)
				if cv2.waitKey(1) == 27:
					running = False



		else:
			y, x = y_, x_
	except Exception as e:
		print(e)
		print(n_sand)
		exit()
	# 	n_sand += 1
	# 	print("to rest!\n\n")
	# 	y, x = 0, 500 - minx
	# 	cv2.imshow("image",  cave_ * 127)
	# 	if cv2.waitKey(2) == 27:
	# 		running = False

print("Done!", n_sand, W, H)
cv2.imshow("image",  cave_ * 127)
if cv2.waitKey() == 27:
	running = False

	# lower = cave[y+1, x]
	# if lower == 0:
	# 	cave[y, x] = 0
	# 	cave[y+1, x] = 1
	# 	return

	# left = cave[y, x-1]







# Part 1: 737
# Part 2: 28145