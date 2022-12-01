with open("input.txt", "r") as f:
    cls = []
    for cl in f.read().split("\n\n"):
        cls.append(sum([int(x) for x in cl.split("\n")]))
cls = sorted(cls, reverse=True)
print("Part 1: " + str(cls[0]))
print("Part 2: " + str(sum(cls[:3])))
