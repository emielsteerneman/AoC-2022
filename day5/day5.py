import re
import copy

# Open file and split into stack, indices, and instructions
file = open("input.txt").read()
stack_str, instructions = file.split("\n\n")
*stack_str, indices = stack_str.splitlines() 

# Get stack width, initialize stack
stack_width = int(re.findall(r'\d+', indices)[-1])
stack = [[] for _ in range(stack_width)]

# Fill stack (doesn't work for stack widths over 9)
for line in stack_str[::-1]:
	[ stack[ci].append(c) for ci, c in enumerate(line[1::4]) if c != ' ']

# Deepcopy stack for part 1 and 2	
stack1, stack2 = copy.deepcopy(stack), copy.deepcopy(stack)

# Iterate over all instructions
for instr in instructions.splitlines():
	numbers = re.findall(r'\d+', instr)
	n, f, t = map(int, numbers)
	f, t = f-1, t-1
	
	stack1[f], cargo = stack1[f][:-n], stack1[f][-n:]
	stack1[t] += cargo[::-1]

	stack2[f], cargo = stack2[f][:-n], stack2[f][-n:]
	stack2[t] += cargo

print("Part 1:", ''.join([ s[-1] for s in stack1 ])) # RNZLFZSJH
print("Part 2:", ''.join([ s[-1] for s in stack2 ])) # CNSFCGJSM