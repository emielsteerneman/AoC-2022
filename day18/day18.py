import numpy as np

file = open("input.txt").read().splitlines()

def calculate_sides(cubes):
	n_sides = len(cubes) * 6
	for ia in range(len(cubes)):
		for ib in range(ia+1, len(cubes)):
			dist = distance(cubes[ia], cubes[ib])
			if dist == 1: n_sides -= 2
	return n_sides

def cluster(cubes):
	idx = np.arange(len(cubes))
	for ia, a in enumerate(cubes):
		for ib, b in enumerate(cubes):
			if distance(a,b) != 1: continue
			idx_cluster = min(idx[ia], idx[ib])
			idx[idx==idx[ia]] = idx_cluster
			idx[idx==idx[ib]] = idx_cluster
	return idx

def distance(a, b):
	return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

SIZE = 23
world = []
for a in range(SIZE):
	for b in range(SIZE):
		for c in range(SIZE):
			world.append((a,b,c))

droplets = [ tuple(map(lambda v: int(v)+1, _.split(","))) for _ in file ]
for d in droplets: world.remove(d)

total_sides = calculate_sides(droplets)
print(f"Part 1: {total_sides}")

clusters = cluster(world)
cluster_idx = np.unique(clusters)

for idx in np.unique(clusters):
	if idx == 0: continue
	cubes_cluster = [ world[_] for _ in np.where(clusters == idx)[0] ]
	cubes_sides = calculate_sides(cubes_cluster)
	total_sides -= cubes_sides

print(f"Part 2: {total_sides}")
exit()