import re
import cv2
import math
import numpy as np
import cv2
import functools

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return int(qx), int(qy)

@functools.cache
def shortest_route(start, stop, visited=frozenset(), indent=0):
	global volcano
	p = lambda *args, **kwargs: print(f"{indent*'  '}[sr][{start}][{stop}][{visited}]", *args, **kwargs)

	if start == stop:
		# # p("Arrived!")
		return 0

	# Add self to visited
	visited = visited.union(set([start]))
	# Get connections
	connected = set(volcano[start]['connected'].keys())
	# Subtract nodes already visited
	connected = connected.difference(visited)
	
	# Unreachable from this node
	if len(connected) == 0: return 999999999999
	# Get costs via all possible routes
	costs = [ volcano[start]['connected'][c] + shortest_route(c, stop, visited, indent+1) for c in connected ]

	return min(costs)

	


file = open("input_full.txt").read().splitlines()

volcano = {}

for line in file:
	flow_rate = int(re.findall(r'\d+', line)[0])
	at, *connected = re.findall(f'[A-Z][A-Z]', line)

	paths = {label:1 for label in connected }
	volcano[at] = {'flow_rate':flow_rate, 'connected':paths}

# Find all useless paths
labels = list(volcano)
for label in labels:
	flow_rate, connected = volcano[label]['flow_rate'], volcano[label]['connected']
	if flow_rate != 0 or len(connected) != 2: continue
	cost = sum(connected.values())
	# print(f"\n{label}", flow_rate, connected, cost)
	# Replace label
	map_ = {a:b for a,b in zip(list(connected), list(connected)[::-1])}
	for c in connected:
		# print("  before", c, volcano[c]['connected'])
		volcano[c]['connected'].pop(label)
		volcano[c]['connected'][map_[c]] = cost
		# print("  after", c, volcano[c]['connected'])
	volcano[label]['connected'] = []

	flow_rate, connected = volcano[label]['flow_rate'], volcano[label]['connected']
	# print(label, flow_rate, connected)
	volcano.pop(label)




# Draw volcano
SIZE = 900
img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)

labels = list(volcano)
# labels = [ v for v in volcano if 0 < len(volcano[v]['connected']) ]

radians = np.linspace(0, 2 * np.pi, len(labels)+1)
label_to_rad = { label:rad for label, rad in zip(labels, radians) }

for label, rad in zip(labels, radians):
	print(label, volcano[label])
	x,  y  = rotate([SIZE//2,SIZE//2], [50, SIZE//2], rad)
	tx, ty = rotate([SIZE//2,SIZE//2], [20, SIZE//2], rad)
	flow_rate = volcano[label]['flow_rate']
	color = (255,255,255) if 0 < flow_rate else (127, 127, 127)
	color = (0,0,255) if label == labels[0] else color
	cv2.circle(img, (x, y), 10, color, -1)
	cv2.putText(img, label + " " + str(flow_rate), (tx, ty), cv2.FONT_HERSHEY_PLAIN, 1, color, 1, cv2.LINE_AA)
	for c in volcano[label]['connected']:
		lx, ly = rotate([SIZE//2,SIZE//2], [70, SIZE//2], rad)
		cx, cy = rotate([SIZE//2,SIZE//2], [70, SIZE//2], label_to_rad[c])
		cv2.line(img, (lx, ly), (cx, cy), (255,255,255), 2)

# cv2.imshow("image", img)
# cv2.waitKey()



# exit()
print()
print()

TARGET = 0
STEPS = 1

max_indent = 0

def walk(dude, elephant, valves_opened, total_pressure_released, minutes_left, indent=0):
	total_flow = sum([ volcano[v]['flow_rate'] for v in valves_opened ])

	global max_indent
	if max_indent < indent:
		max_indent = indent
		print(max_indent)

	
	p = lambda *args, **kwargs: print(f"{indent*'    '}[walk][{30-minutes_left}][{total_pressure_released}][->{total_flow}]", *args, **kwargs)
	# p = lambda *args, **kwargs: None

	dude[STEPS] -= 1
	elephant[STEPS] -= 1

	# p(f"Actors {dude} {elephant}")

	# If out of time, stop
	if minutes_left <= 0: return total_pressure_released
	
	# Check if any actor arrived at a valve
	sub = 0
	if dude[STEPS] == -1:
		valves_opened = valves_opened.union([dude[TARGET]])
		# p(f"Dude opened valve {dude[TARGET]}")
	if elephant[STEPS] == -1:
		valves_opened = valves_opened.union([elephant[TARGET]])
		# p(f"Elephant opened valve {elephant[TARGET]}")
	

	# If both dude and elephant are still walking, continue
	if 0 <= dude[STEPS] and 0 <= elephant[STEPS]:
		# p("Walking...")
		return walk(dude, elephant, valves_opened, total_pressure_released + total_flow, minutes_left-1, indent+1)


	## For now, it doesn't matter if both dude and elephant walk towards the same valve

	total_flow = sum([ volcano[v]['flow_rate'] for v in valves_opened ])
	# p(f"Opened: {','.join(valves_opened)} -> {total_flow}")

	valves_closed = set( volcano.keys() ).difference(valves_opened)

	if len(valves_closed) == 0:
		# p(f"All valves opened! Added flow: {total_flow} * {minutes_left} = {total_flow * minutes_left}")
		return total_pressure_released + total_flow * minutes_left

	# Pressure released when not moving anymore
	pressure_released = minutes_left * total_flow
	# p(f"Standing still: {total_flow} * {minutes_left} = {total_flow * minutes_left}")

	if dude[STEPS] == -1 and elephant[STEPS] == -1:
		for v1 in valves_closed:
			for v2 in valves_closed:
				# p(f"Assigning new valve to both: {v1} {v2}")

				dude_, elephant_ = dude[:], elephant[:]
				
				dude_[STEPS] = shortest_route(dude[TARGET], v1)
				dude_[TARGET] = v1
				elephant_[STEPS] = shortest_route(elephant[TARGET], v2)
				elephant_[TARGET] = v2

				if dude_ == elephant_:
					# print("Skipping this one")
					continue

				r = walk(dude_, elephant_, valves_opened, total_pressure_released + total_flow, minutes_left-1, indent+1)

				if pressure_released < r:
					# p(f"More release for {v1} {v2} : {r}")
					pressure_released = r

	elif dude[STEPS] == -1:
		# p("Assigning new valve to dude")
		for v1 in valves_closed:
			dude_ = dude[:]
			dude_[STEPS] = shortest_route(dude_[TARGET], v1)
			dude_[TARGET] = v1
			r = walk(dude_, elephant[:], valves_opened, total_pressure_released + total_flow, minutes_left-1, indent+1)

			if pressure_released < r:
				# p(f"More release for {v1} : {r}")
				pressure_released = r

	elif elephant[STEPS] == -1:
		# p("Assigning new valve to elephant")
		for v1 in valves_closed:
			elephant_ = elephant[:]
			elephant_[STEPS] = shortest_route(elephant_[TARGET], v1)
			elephant_[TARGET] = v1
			r = walk(dude[:], elephant_, valves_opened, total_pressure_released + total_flow, minutes_left-1, indent+1)

			if pressure_released < r:
				# p(f"More release for {v1} : {r}")
				pressure_released = r


	# p(f"Best result: {pressure_released}")
	return pressure_released

possible_valves = [ v for v in volcano if 0 < len(volcano[v]['connected']) ]

keys = list(volcano.keys())

for k in keys:
	if len(volcano[k]['connected']) == 0:
		volcano.pop(k)

print(list(volcano.keys()))

actors = [['AA', 0]]


# r = walk(volcano, 'AA', set(['AA']), 0, 30, 0, ['DD', 'BB', 'JJ', 'HH', 'EE', 'CC'])
r = walk(['AA', 0], ['AA', 0], set(['AA']), 0, 15)




print(r)






# Part 1 : 1728
















