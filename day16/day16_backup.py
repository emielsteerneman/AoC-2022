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
		# p("Arrived!")
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

@functools.cache
def walk(at, valves_opened, total_pressure_released, minutes_left):
	indent=0
	pressure = sum([ volcano[v]['flow_rate'] for v in valves_opened ])
	
	p = lambda *args, **kwargs: print(f"{indent*'    '}[walk][{at}][{30-minutes_left}][{total_pressure_released}][->{pressure}]", *args, **kwargs)
	p = lambda *args, **kwargs: None
	
	p(f"At {at}")

	# If out of time, stop
	if minutes_left <= 0: return 0
	
	# Open own valve
	if at not in valves_opened:
		minutes_left -= 1
		valves_opened = valves_opened.union([at])
		total_pressure_released += pressure
		p(f"Opened valve {at}")

	# If out of time, stop
	if minutes_left <= 0:
		return total_pressure_released
	
	connected = volcano[at]['connected']
	pressure = sum([ volcano[v]['flow_rate'] for v in valves_opened ])

	p(f"Opened: {','.join(valves_opened)} -> {pressure}")

	all_valves = set( volcano.keys() )
	valves_closed = all_valves.difference(valves_opened)
	# p(f"Closed: {','.join(valves_closed)}")

	if len(valves_closed) == 0:
		p(f"All valves opened! Added pressure: {pressure} * {minutes_left} = {pressure * minutes_left}")
		return total_pressure_released + pressure * minutes_left


	# Pressure released when not moving anymore
	pressure_released = minutes_left * pressure
	p(f"Standing still: {pressure} * {minutes_left} = {pressure * minutes_left}")

	for valve in valves_closed:
		cost = shortest_route(at, valve)

		# cost = connected[c]
		# p(f"Moving to {c} ({cost})")
		# total_pressure_released += pressure * min(cost, minutes_left)
		r = walk(valve, valves_opened, total_pressure_released + cost*pressure, minutes_left - cost)

		# r += min(cost, minutes_left) * pressure
		# p(f"=valve {valve} : cost {cost} : r {r}")

		
		if pressure_released < r:
			p(f"More release for {valve} : {r}")
			pressure_released = r

	p(f"Best result: {pressure_released}")
	return pressure_released

possible_valves = [ v for v in volcano if 0 < len(volcano[v]['connected']) ]

keys = list(volcano.keys())

for k in keys:
	if len(volcano[k]['connected']) == 0:
		volcano.pop(k)

print(list(volcano.keys()))



# r = walk(volcano, 'AA', set(['AA']), 0, 30, 0, ['DD', 'BB', 'JJ', 'HH', 'EE', 'CC'])
r = walk('AA', frozenset(['AA']), 0, 30)




print(r)






# Part 1 : 1728
















