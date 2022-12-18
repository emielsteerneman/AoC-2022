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

def shortest_route(start, stop, visited=set(), indent=0):
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
		volcano[c]['connected'].pop(label)
		volcano[c]['connected'][map_[c]] = cost
	volcano[label]['connected'] = []

	flow_rate, connected = volcano[label]['flow_rate'], volcano[label]['connected']
	volcano.pop(label)

ROUTING_TABLE = {}

for a in volcano.keys():
	ROUTING_TABLE[a] = {}
	for b in volcano.keys():
		ROUTING_TABLE[a][b] = shortest_route(a, b)

# Draw volcano
SIZE = 900
img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)

labels = list(volcano)

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

max_value = 0

# @functools.cache
def walk(dude_target, dude_steps, elephant_target, elephant_steps, valves_opened, total_pressure_released, minutes_left):

	global max_value
	if max_value < total_pressure_released:
		max_value = total_pressure_released
		print(max_value)


	potential = total_pressure_released + sum([ volcano[v]['flow_rate'] for v in volcano ]) * minutes_left
	if potential < max_value:
		return total_pressure_released
	
	dude_steps -= 1
	elephant_steps -= 1

	# If out of time, stop
	if minutes_left <= 0: return total_pressure_released
	
	# Check if any actor arrived at a valve
	sub = 0
	if dude_steps == -1:     valves_opened = valves_opened.union([dude_target])
	if elephant_steps == -1: valves_opened = valves_opened.union([elephant_target])

	total_flow = sum([ volcano[v]['flow_rate'] for v in valves_opened ])

	# If both dude and elephant are still walking, continue
	if 0 <= dude_steps and 0 <= elephant_steps:
		return walk(dude_target, dude_steps, elephant_target, elephant_steps, \
			valves_opened, total_pressure_released + total_flow, minutes_left-1)

	### For now, it doesn't matter if both dude and elephant walk towards the same valve
	valves_closed = list(set( volcano.keys() ).difference(valves_opened))
	valves_closed = sorted(valves_closed, key=lambda v: volcano[v]['flow_rate'])[::-1]

	# Pressure released when not moving anymore
	pressure_released = minutes_left * total_flow

	if dude_steps == -1 and elephant_steps == -1:
		for v1 in valves_closed:
			for v2 in valves_closed:
				r = walk(v1, ROUTING_TABLE[dude_target][v1], v2, ROUTING_TABLE[elephant_target][v2], \
					valves_opened, total_pressure_released + total_flow, minutes_left-1)
				pressure_released = max(r, pressure_released)

	elif dude_steps == -1:
		for v1 in valves_closed:
			r = walk(v1, ROUTING_TABLE[dude_target][v1], elephant_target, elephant_steps, \
				valves_opened, total_pressure_released + total_flow, minutes_left-1)
			pressure_released = max(r, pressure_released)

	elif elephant_steps == -1:
		for v1 in valves_closed:
			r = walk(dude_target, dude_steps, v1, ROUTING_TABLE[elephant_target][v1], \
				valves_opened, total_pressure_released + total_flow, minutes_left-1)
			pressure_released = max(r, pressure_released)

	return pressure_released

print(list(volcano.keys()))

print("Part 1:", walk('AA', 0, 'AA', 9999999, frozenset(['AA']), 0, 30))
print("Part 2:", walk('AA', 0, 'AA', 0, frozenset(['AA']), 0, 26))
