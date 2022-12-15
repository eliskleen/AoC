import collections
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
        rows = f.read().splitlines()
        sensors = collections.defaultdict()
        for r in rows:
            cs = r.split(":")
            s = (int(cs[0].split(',')[0].split('=')[-1]), int(cs[0].split(',')[1].split('=')[-1]))
            b = (int(cs[1].split(',')[0].split('=')[-1]), int(cs[1].split(',')[1].split('=')[-1]))
            # print(f"Sensor {s} has range {b}")
            sensors[s] = b
        return sensors


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
def dxdy(a, b):
    return (abs(a[0] - b[0]), abs(a[1] - b[1]))


def getRanges(s, b):
    (dx, dy) = dxdy(s, b)
    ranges = []

    return ranges


def star1(data):
    return 0
    map = collections.defaultdict(lambda : '.')
    depth = 2000000
    # depth = 10
    for s, b in data.items():
        d = dist(s, b)
        x = s[0]
        y = s[1]
        if s[1] + d < depth and s[0] < depth:
            continue
        if s[1] - d > depth and s[0] > depth:
            continue
        dy = abs(y - depth)
        if dy > d:
            continue
        # print(f"x: {x}, y: {y}, d: {d}, b: {b}")
        dx = abs(d - dy)
        # print(f"dx: {dx}, dy: {dy}")
        for i in range(dx+1):
            if (x+i, depth) == b:
                continue
            map[(x+i, depth)] = "#"
            map[(x-i, depth)] = "#"

    return len([v for (k,v) in map.items() if v == "#" and k[1] == depth])
    # return count

        # for cx in range(xMin, xMax+1):
        #     dx = abs(cx - x)
        #     yMin = y - (d-dx)
        #     yMax = y + (d-dx)
        #     if yMin > depth or yMax < depth:
        #         continue
        #     for cy in range(yMin, yMax+1):
        #         print(f"({cx}, {cy})")
        #         if cy == depth and (cx, cy) != b:
        #             print("#")
        #             map[(cx, cy)] = "#"

    # ps = ""
    # for y in range(10, 11):
    #     ps += "\n" + str(y) + " "
    #     if(len(str(y)) < 2):
    #         ps += " "
    #     for x in range(-4, 26):
    #         ps += map[(x,y)]
    # print(ps)

    # return len([v for (k,v) in map.items() if v == "#" and k[1] == depth])


                    




        
        
    
    return 0

def star2(data):
    print("Star 2")
    max = 20
    max = 4000000
    dists = collections.defaultdict(lambda : 0)
    for s, b in data.items():
        d = dist(s, b)
        dists[s] = d
    y = 0
    while y < max:
        if y % 100_000 == 0:
            print(f"y: {y}")
        x = 1
        while x < max:
            reached = False
            for s, d in dists.items():
                cd = dist((x,y), s) 
                if cd <= d:
                    reached = True
                    x += abs(d - cd)
                    break
            x+= 1
            if not reached:
                x-= 1
                return (x)*4000000 + y
        y += 1

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