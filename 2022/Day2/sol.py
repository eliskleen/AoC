def sol():
    games = []
    with open("input.txt", "r") as f:
        games = f.read().split("\n")
    s = sum([match(m[0], m[2]) for m in games])
    print(s)
    s = sum([match(m[0], predict(m[0], m[2])) for m in games])
    print(s)

    

def rep(s):
    return s.replace("A", "R").replace("B", "P").replace("C", "S").replace("X", "R").replace("Y", "P").replace("Z", "S")
def match(elf, me):
    elf = rep(elf)
    me = rep(me)
    if elf == "R":
        if me == "R":
            return 3+1
        elif me == "P":
            return 6+2
        elif me == "S":
            return 0+3
    elif elf == "P":
        if me == "R":
            return 0+1
        elif me == "P":
            return 3+2
        elif me == "S":
            return 6+3
    elif elf == "S":
        if me == "R":
            return 6+1
        elif me == "P":
            return 0+2
        elif me == "S":
            return 3+3

# Y = draw, X = lose, Z = win
def predict(elf, res):
    elf = rep(elf)
    if elf == "R":
        if res == "Y":
            return "R"
        elif res == "X":
            return "S"
        elif res == "Z":
            return "P"
    elif elf == "P":
        if res == "Y":
            return "P"
        elif res == "X":
            return "R"
        elif res == "Z":
            return "S"
    elif elf == "S":
        if res == "Y":
            return "S"
        elif res == "X":
            return "P"
        elif res == "Z":
            return "R"

            
if __name__ == "__main__":
    sol()