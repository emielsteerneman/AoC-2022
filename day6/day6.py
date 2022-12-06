stream = open("input.txt").read()



for i in range(len(stream)-3):
	marker = stream[i:i+4]
	if(len(list(set(marker)))) == 4:
		print(i+4, marker)
		break

for i in range(len(stream)-13):
	marker = stream[i:i+14]
	if(len(list(set(marker)))) == 14:
		print(i+14, marker)
		break