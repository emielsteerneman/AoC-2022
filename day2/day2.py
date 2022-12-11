games = [ [ord(_[0])-65, ord(_[-1])-88] for _ in open("input.txt").read().splitlines()]

part1 = sum([ 3 * ((b - a + 1) % 3) + b + 1 for a, b in games ])
part2 = sum([ (a + b + 2) % 3 + 1 + b * 3 for a, b in games ])

print("Part 1:", part1)
print("Part 2:", part2)