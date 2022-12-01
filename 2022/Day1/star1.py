
lines = open("input.txt").readlines()
lines.append("\n\n")
print(lines)
calList = []
currCal = 0
for line in lines:
    if line == "\n":
        calList.append(currCal)
        currCal = 0
    else:
        currCal += int(line)


print(max(calList))
