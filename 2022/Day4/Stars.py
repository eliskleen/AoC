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
    with open(path) as f:
        return f.read().splitlines()
    
def getAss(pair):
    pair = pair.split(',')
    return (set(getRange(pair[0])), set(getRange(pair[1])))

def getRange(e):
    return range(int(e.split('-')[0]), int(e.split('-')[1])+1)

def star1(pairs):
    return sum([1 if e1.issubset(e2) or e2.issubset(e1) else 0 for e1, e2 in [getAss(p) for p in pairs]])

def star2(pairs):
    return sum([1 if (e1 & e2) else 0 for e1, e2 in [getAss(p) for p in pairs]])

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