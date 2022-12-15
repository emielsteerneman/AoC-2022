import re
import numpy as np

# Manhattan Distance
def mhd(x1, y1, x2, y2):
	return abs(x1-x2) + abs(y1-y2)

# Merge ranges
def merge_ranges(ranges, range_):
	for ir, r in enumerate(ranges):
		[al, ar], [bl, br] = r, range_
		# No overlap
		if ar+1 < bl or br+1 < al: continue
		# Overlap
		nxt = ranges[:ir] + ranges[ir+1:]
		overlap = [ min(al, bl), max(ar, br) ]
		return merge_ranges(nxt, overlap)

	return ranges + [range_]

# Parse file
file = open("input.txt").read().splitlines()

sensors, beacons, sensors_beacons_range = [], [], []

for sb in file:
	ints = list(map( int, re.findall(r'-?\d+', sb) ))
	[sx, sy], [bx, by] = np.array(list(zip(ints[::2], ints[1::2])))
	range_ = mhd(sx,sy,bx,by)
	sensors.append( (sx, sy) )
	beacons.append( (bx, by) )
	sensors_beacons_range.append([ [sx, sy], [bx, by], range_ ])

sensors = list(set(sensors))
beacons = list(set(beacons))

for y in range(0, 4000000):
	current_ranges = None
	# For each beacon
	for [sx, sy], [_, _], sensor_range in sensors_beacons_range:
		# Get distance to row
		distance = mhd(sx,sy,sx,y)
		# If sensor out of row distance, skip
		if sensor_range < distance: continue
		# Create range
		leftover = sensor_range - distance
		range_ = [sx-leftover, sx+leftover]
		# Merge range into existing range(s)
		if current_ranges is None: current_ranges = [ range_ ]
		current_ranges = merge_ranges(current_ranges, range_)


	if 1 < len(current_ranges):
		print("Part 2:", current_ranges[0][0] * 400000 + y)

	if y == 2000000:
		total = 0
		for x1,x2 in current_ranges:
			total += x2-x1+1
			for sx, sy in sensors: 
				if sy == y and x1 <= sx and sx <= x2: total -= 1
			for bx, by in beacons:
				if by == y and x1 <= bx and bx <= x2: total -= 1		
		print("Part 1:", total)

"""
Onroerendezaakbelasting (OZB)
Watersysteemheffing
Rioolheffing
Belasting op Leidingen (BoL)
Waterschapsbelasting
Reinigingsheffing	
- Afvalstoffenheffing
- Reinigingsrechten
"""
