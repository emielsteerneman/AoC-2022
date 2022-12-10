text = open("input.txt").read()

elves_inventory_summation = [ 
    sum([ 
        *map(int, inv.split("\n")) 
    ]) for inv in text.split("\n\n") 
]

print("Part 1:", max( elves_inventory_summation ))
print("Part 2:", sum( sorted(elves_inventory_summation)[-3:] ))