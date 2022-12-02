# A X rock
# B Y paper
# C Z scissors
lost = {"A": "Z", "C": "Y", "B": "X", "score":0}
win = {"A": "Y", "C": "X", "B": "Z", "score":6}
draw = {"A": "X", "B": "Y", "C": "Z", "score":3}
score = {"X":1, "Y":2, "Z":3}


def match(elf, me):
    if lost[elf] == me:
        return lost["score"] + score[me]
    elif win[elf] == me:
        return win["score"] + score[me]
    elif draw[elf] == me:
        return draw["score"] + score[me]
    print("Error" + elf + " " + me)

# Y = draw, X = lose, Z = win
def predict(elf, res):
    match res:
        case "Y": return [v for k, v in draw.items() if k == elf][0]
        case "X": return [v for k, v in lost.items() if k == elf][0]
        case "Z": return [v for k, v in win.items() if k == elf][0]

def sol():
    with open ("input.txt", "r") as f:
        games = f.read().split("\n")
    s = sum([match(m[0], m[2]) for m in games])
    print(s)
    s = sum([match(m[0], predict(m[0], m[2])) for m in games])
    print(s)
    
if __name__ == "__main__":
    sol()