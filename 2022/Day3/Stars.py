import time
import itertools

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
        print(f"Load time: {load_time}")
        print(f"Star 1 time: {star1_time}")
        print(f"Star 2 time: {star2_time}")
        print(f"Star 1 answer: {ans1}")
        print(f"Star 2 answer: {ans2}")


def get_data(path):
    with open(path, "r", encoding="UTF-8") as f:
        return f.read().splitlines()


def inBoth(bp):
    s = len(bp) // 2
    for p in bp[0 : s]:
        if p in bp[s :]:
            return p
    print(f"Error: {bp}")
    return ''

def star1(bps):
    return sum([ord(p)-96 if p.islower() else ord(p)-38 if not p == '' else 0 for p in [inBoth([c for c in bp]) for bp in bps]] )


def inThree(g):
    for p in g[0]:
        if p in g[1] and p in g[2]:
            return p
    return ''
def star2(data):
    gs = [data[x:x+3] for x in range(0, len(data), 3)]
    return sum([ord(p)-96 if p.islower() else ord(p)-38 if not p == '' else 0 for p in [inThree([c for c in bp]) for bp in gs]] )


def main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        day_()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    stats.dump_stats(filename="profiling.prof")


if __name__ == "__main__":
    main()
