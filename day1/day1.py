text = open("input.txt").read()

elves_inventory = text.split("\n\n")
elves_inventory = [ [ *map(int, inv.split("\n")) ] for inv in elves_inventory ]

elves_inventory_summation = [ sum(_) for _ in elves_inventory ]

# Day 1
print( max( elves_inventory_summation ))

# Day 2
print( sum( sorted(elves_inventory_summation)[-3:] ))