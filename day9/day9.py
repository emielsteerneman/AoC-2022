import math

commands = open("input.txt").read().splitlines()
commands = [ [cmd[0], int(cmd[2:])] for cmd in commands ]

part1, part2 = [], []
coordinates = [ [0, 0] for i in range(10) ]

# For each command
for d, n in commands:
	
	# For each step in command
	for i in range(n):
		
		# Move head
		if d == "U": coordinates[0][1] -= 1
		if d == "D": coordinates[0][1] += 1
		if d == "L": coordinates[0][0] -= 1
		if d == "R": coordinates[0][0] += 1

		# Update each knot
		for icoord in range(len(coordinates)-1):
			Hx, Hy = coordinates[icoord]
			Tx, Ty = coordinates[icoord+1]

			# Calculate euclidean distance
			dx, dy = Tx - Hx, Ty - Hy
			distance = math.sqrt( dx**2 + dy**2 )
			
			# Basically, if distance further than sqrt(2)
			if 2 <= distance:
				# Normalize distance vector, round it, add it to upstream knot
				Tx, Ty = Hx+round(dx/distance), Hy+round(dy/distance)
				coordinates[icoord+1] = [Tx, Ty]

		part1.append( (coordinates[1][0], coordinates[1][1]) )
		part2.append( (coordinates[-1][0], coordinates[-1][1]) )

print("Part1:", len(set(part1)))
print("Part2:", len(set(part2)))
