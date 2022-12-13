from functools import cmp_to_key

def compare(left, right):
	if type(left) == int and type(right) == int:
		if left < right: return GOOD
		if right < left: return BAD
		return UNKNOWN

	if type(left) == list and type(right) == list:
		pairs = list(zip(left, right))
		returns = list(map(lambda lr: compare(*lr), pairs))
		if all(map(lambda _: _ == UNKNOWN, returns)):
			return compare(len(left), len(right))
		idx_good = returns.index(GOOD) if GOOD in returns else len(returns)
		idx_bad  = returns.index(BAD)  if BAD  in returns else len(returns)
		return compare(idx_good, idx_bad)

	if type(left) == int:
		return compare([left], right)
	if type(right) == int:
		return compare(left, [right])

def compare_sort(left, right):
	return -1 if compare(left, right) == GOOD else 1

pairs = open("input.txt").read().split("\n\n")
BAD, GOOD, UNKNOWN = 0, 1, 2
results, packets = [], []

for pair in pairs:
	left, right = pair.split("\n")
	results.append( compare(eval(left), eval(right)) )
	packets += [ eval(left), eval(right) ]

part1 = sum([ idx+1 for idx,r in enumerate(results) if r == GOOD ])
print("Part 1:", part1)

packets += [ [[2]], [[6]] ]
packets.sort(key=cmp_to_key(compare_sort))
part2 = (packets.index([[2]])+1) * (packets.index([[6]])+1)
print("Part 2:", part2)