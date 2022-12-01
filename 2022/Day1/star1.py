
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


print(max(calList))
