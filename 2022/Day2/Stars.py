import time

def day_():
    path = "data.txt"
    # path = "test-data.txt"

    start_time = time.perf_counter()
    data = get_data(path)

    time1 = time.perf_counter()

    ans1 = star1(data)
    time2 = time.perf_counter()

    ans2 = star2(data)
    time3 = time.perf_counter()

    load_time = time1 - start_time
    star1_time = time2 - time1
    star2_time = time3 - time2
    if 1:
        print(f'Load time: {load_time}')
        print(f'Star 1 time: {star1_time}')
        print(f'Star 2 time: {star2_time}')
        print(f'Star 1 answer: {ans1}')
        print(f'Star 2 answer: {ans2}')

def get_data(path):
    with open(path, "r") as f:
        return f.read().split('\n')
# A X rock
# B Y paper
# C Z scissors
lost = {"A": "Z", "C": "Y", "B": "X", "score": 0}
win = {"A": "Y", "C": "X", "B": "Z", "score": 6}
draw = {"A": "X", "B": "Y", "C": "Z", "score": 3}
score = {"X": 1, "Y": 2, "Z": 3}


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
        case "Y":
            return [v for k, v in draw.items() if k == elf][0]
        case "X":
            return [v for k, v in lost.items() if k == elf][0]
        case "Z":
            return [v for k, v in win.items() if k == elf][0]

   
def star1(games):
    return sum([match(m[0], m[2]) for m in games])    

def star2(data):
    return sum([match(m[0], predict(m[0], m[2])) for m in data])
    return 0

def main():
    import cProfile
    import pstats
    with cProfile.Profile() as pr:
        day_()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    stats.dump_stats(filename = 'profiling.prof')

if __name__ == '__main__':
    main()