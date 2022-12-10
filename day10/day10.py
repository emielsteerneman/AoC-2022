import numpy as np

commands = open("input.txt").read().splitlines()

register = 1
values = [1]
CRT = np.zeros(40*6, dtype=int)

def draw(CRT, cycle, register):
	at = register + cycle // 40 * 40
	if cycle in [at-1, at, at+1]: CRT[cycle] = 1

for cmd in commands:
	if cmd == "noop": 
		draw(CRT, len(values)-1, register)
		values.append(register)
	
	else:
		draw(CRT, len(values)-1, register)
		values.append(register)
		val = int(cmd.split(" ")[1])

		draw(CRT, len(values)-1, register)
		values.append(register)
		register += val

part1 = sum([ ind * values[ind] for ind in [20, 60, 100, 140, 180, 220] ])
print("Part 1:", part1)

print("Part 2:")
string = "".join([ " #"[_] for _ in CRT])
for i in range(6):
	print(string[ i*40 : (i+1)*40 ])