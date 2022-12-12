import re
import math

class Monkey:
	def __init__(self, monkey_id, starting_items, operation, divtest, iftrue, iffalse):
		self.monkey_id = monkey_id
		self.starting_items = starting_items[:]
		self.items = starting_items[:]
		self.operation = lambda old : eval( operation )
		self.divtest = divtest
		self.iftrue = iftrue
		self.iffalse = iffalse
		self.n_items_inspected = 0
	
	def inspect(self, is_part1, factor):
		result = []
		self.n_items_inspected += len(self.items)
		while len(self.items):
			item = self.items.pop(0)
			item = self.operation(item)
			if is_part1: item //= 3
			item = item % factor
			result.append([ item, self.iftrue if item % self.divtest == 0 else self.iffalse ])
		return result

	def reset(self):
		self.items = self.starting_items[:]
		self.n_items_inspected = 0

monkeys_str = open("input.txt").read().split("\n\n")
monkeys = []

for monkey_str in monkeys_str:
	to_int = lambda _ : list(map(int, _))
	get_ints = lambda _ : list(map(int, re.findall(r'\d+', _) ))

	lines = monkey_str.splitlines()

	monkey_id = get_ints(lines[0])[0]
	starting_items = get_ints(lines[1])
	operation = lines[2].split(" = ")[1]
	divtest = get_ints(lines[3])[0]
	iftrue  = get_ints(lines[4])[0]
	iffalse = get_ints(lines[5])[0]

	monkeys.append(Monkey(monkey_id, starting_items, operation, divtest, iftrue, iffalse))

factor = 1
for monkey in monkeys: factor *= monkey.divtest

for i in range(20):
	for monkey in monkeys:
		for item, to in monkey.inspect(True, factor):
			monkeys[to].items.append(item)

n_inspected = sorted([ m.n_items_inspected for m in monkeys ])
part1 = n_inspected[-2] * n_inspected[-1]
print("Part 1:", part1)

for monkey in monkeys: monkey.reset()

for i in range(10000):
	for monkey in monkeys:
		for item, to in monkey.inspect(False, factor):
			monkeys[to].items.append(item)

n_inspected = sorted([ m.n_items_inspected for m in monkeys ])
part2 = n_inspected[-2] * n_inspected[-1]
print("Part 2:", part2)