import re

pairs = open("input.txt").read().splitlines()

pairs = [ re.findall(r'\d+', pair) for pair in pairs ]
pairs = [list(map(int, pair)) for pair in pairs]

part1 = 0
for a1, b1, a2, b2 in pairs:
	if a1 <= a2 and b2 <= b1 \
	or a2 <= a1 and b1 <= b2: 
		part1 += 1

part2 = 0
for a1, b1, a2, b2 in pairs:
	if a1 <= a2 <= b1 \
	or a1 <= b2 <= b1 \
	or a2 <= a1 <= b2 \
	or a2 <= b1 <= b2:
		part2 += 1

print(part1)
print(part2)