lines = open("input.txt").readlines()
lines.append("\n\n")
print(lines)
calList = []
currCal = 0
for line in lines:
    if line == "\n":
        calList.append(currCal)
        currCal = 0
    elif line != "\n\n":
        currCal += int(line)
calList = sorted(calList, reverse=True)
s1 = calList[0]
s2 = sum(calList[:3])
print("Part 1: ", s1)
print("Part 2: ", s2)