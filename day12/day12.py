import numpy as np

def get_surrounding(x, y, W, H):
	coords = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
	return np.array([ (x,y) for (x,y) in coords if 0 <= x < W and 0 <= y < H ])

# Open and read file
file = open("input.txt").read().splitlines()
W, H = len(file[0]), len(file)

### Create mountain matrix
mountain = np.zeros((H, W), dtype=int)
start_x, start_y, stop_x, stop_y = 0, 0, 0, 0

for i_line, line in enumerate(file):
	mountain[i_line] = np.array([ ord(_)-ord('a') for _ in line ])
	if 'S' in line: start_x, start_y = line.index('S'), i_line
	if 'E' in line: stop_x,  stop_y  = line.index('E'), i_line

mountain[stop_y,  stop_x]  = 25
mountain[start_y, start_x] = 0

# Create cost matrix. All costs are infinite initially
costs = np.ones((H, W), dtype=int) * np.inf

# Initialize pathfinding, set cost of starting position to 0
costs[stop_y, stop_x] = 0
to_visit = [(stop_x, stop_y)]

# Run pathfinding
while 0 < len(to_visit):
	# Get current position 
	x, y = to_visit.pop(0)
	height, cost = mountain[y, x], costs[y, x]
	# Get all surroundings of current position that are valid movements
	surroundings = get_surrounding(x, y, W, H)
	heights = np.array([ mountain[b, a] for a,b in surroundings ])
	idx = height -1 <= heights
	# If cost of surrounding can be improved, do so and add to visiting list
	for [a, b], h in list(zip(surroundings[idx], heights[idx])):
		if cost + 1 < costs[b, a]:
			costs[b, a] = cost + 1
			to_visit.append((a, b))

print("Part 1:", int(costs[start_y, start_x]))
print("Part 2:", int(np.min(costs[mountain == 0])))