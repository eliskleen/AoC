from collections import Counter
import time

def day_():
    path = "input1.txt"
    # path = "test.txt"

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

#a,b -> c,d is the start coord and the end coord, return all coords in between
def getCoords(a,b,c,d, straightOnly = True):

    if a == c:
        return [(a,i) for i in range(min(b,d),max(b,d)+1)]
    elif b == d:
        return [(i,b) for i in range(min(a,c),max(a,c)+1)]
    elif straightOnly:
        print(f"Not straight line {a},{b} -> {c},{d}")
        return []
    else: #diagonal
        if a > c:
            a,b,c,d = c,d,a,b
        if b > d:
            return [(a+i,b-i) for i in range(c-a+1)]
        else:
            return [(a+i,b+i) for i in range(c-a+1)]

        
        
# create a diag line from a,b to c,d
    



def star1(data):
    c = Counter()
    for line in data:
        f,s = line.split(" -> ")
        f = f.split(",")
        s = s.split(",")
        for i in getCoords(int(f[0]),int(f[1]),int(s[0]),int(s[1])):
            c[i] += 1

        
    return sum([1 for i in c.values() if i > 1])

def star2(data):
    c = Counter()
    for line in data:
        f,s = line.split(" -> ")
        f = f.split(",")
        s = s.split(",")
        for i in getCoords(int(f[0]),int(f[1]),int(s[0]),int(s[1]), False):
            c[i] += 1

        
    return sum([1 for i in c.values() if i > 1])
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