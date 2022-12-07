import os

file = open("input.txt").read().splitlines()
current_path = "/"
filesystem = {}

### Build filesystem
for line in file:
	# Enter new directory, create new entry in filesystem if needed
	if line.startswith("$ cd"):
		current_path = os.path.realpath( os.path.join( current_path, line[4:].strip() ))
		if current_path not in filesystem:
			filesystem[current_path] = {
				'files' : [],
				'dirs' : []
			}
	# Register subdirectory
	elif line.startswith("dir"):
		filesystem[current_path]['dirs'].append(line[4:].strip())
	# Register file
	elif line[0] in "0123456789":
		size, filename = line.split(" ")
		filesystem[current_path]['files'].append([int(size), filename])

### Recursive function that gets size of a directory by summing the size of its files and add the sizes of all its subdirectories
def get_directory_size(filesystem, directory):
	files = filesystem[directory]['files']
	subdirectories = filesystem[directory]['dirs']

	total_filesize = sum([file[0] for file in files])
	total_subdirsize = sum([ get_directory_size(filesystem, os.path.join(directory, subdir)) for subdir in subdirectories ])

	return total_filesize + total_subdirsize

### Create mapping of all directories to their sizes
directory_to_size = { directory:get_directory_size(filesystem, directory) for directory in filesystem }

### Part 1
part1 = sum([ directory_to_size[d] for d in directory_to_size if directory_to_size[d] < 100000 ])
print("Part 1:", part1)

### Part 2
space_required = directory_to_size['/'] - 40000000
part2 = min([ directory_to_size[d] for d in directory_to_size if space_required < directory_to_size[d] ])
print("Part 2:", part2)