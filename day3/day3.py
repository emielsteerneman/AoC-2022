bags = open("input.txt").read().splitlines()
containers = [ [_[:len(_)//2], _[len(_)//2:]] for _ in bags ]

s = lambda s : list(set.intersection(*map(set, s)))[0]
m = lambda c : ord(c) - 38 - 58 * c.islower()

part1 = sum( m(s(_)) for _ in containers )
part2 = sum( m(s(_)) for _ in zip(*[iter(bags)]*3) )

print("Part 1:", part1)
print("Part 2:", part2)

# Part 2 oneliner
print(sum(ord(d:=(set(a)&set(b)&set(c)).pop())-38-58*(d>'Z')for(a,b,c)in zip(*[iter(open('i').read().split())]*3)))