import numpy as np
import cv2

### Create forest
forest_file = open("input.txt").read().splitlines()
WIDTH, HEIGHT = len(forest_file[0]), len(forest_file)
forest = np.zeros((HEIGHT, WIDTH), dtype=int)
for i_row, row in enumerate(forest_file):
	for i_col, tree_height in enumerate(row):
		forest[i_row, i_col] = int(tree_height)

### Start part1 with outer borders already counted
part1 = HEIGHT * 2 + WIDTH * 2 - 4
part2 = 0

### Iterate over entire forest, except for outer borders
for row in range(1, WIDTH-1):
	for col in range(1, HEIGHT-1):
		tree = forest[row, col]

		# Find all trees just as high or higher than current tree
		forest_copy = np.copy(forest)
		forest_copy = np.clip(forest_copy - tree + 1, 0, 9) != 0

		# Get all trees left, right, up, and down of current tree
		left, right = forest_copy[row, :col], forest_copy[row, col+1:]
		up, down = forest_copy[:row, col], forest_copy[row+1:, col]

		# Part 1
		part1 += np.sum(left) == 0 or np.sum(right) == 0 or np.sum(up) == 0 or np.sum(down) == 0

		# Part 2
		dleft  = len(left)  if sum(left)  == 0 else np.argmax(np.flip(left)) + 1
		dright = len(right) if sum(right) == 0 else np.argmax(right) + 1
		dup    = len(up)    if sum(up)    == 0 else np.argmax(np.flip(up)) + 1
		ddown  = len(down)  if sum(down)  == 0 else np.argmax(down) + 1
		
		score = dleft * dright * dup * ddown
		part2 = max(part2, score)
		
print("part1:", part1)
print("part2:", part2)