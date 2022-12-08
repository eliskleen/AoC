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
        grid = []
        for r in rows:
            grid.append([int(x) for x in r])
        return grid
    
def star1(data):
    # print(data)
    visible = collections.defaultdict()
    s = len(data)-1

    currMaxX = currMaxY = currMaxXInv = currMaxYInv = 0
    for x in range(s+1):
        currMaxX = currMaxY = currMaxXInv = currMaxYInv = 0
        for y in range(s+1):
            # print(f"(x,y): ({x},{y})")
            if data[x][y] > currMaxX:
                currMaxX = data[x][y]
                visible[(x,y)] = (True, data[x][y], "x")
            if data[y][x] > currMaxY:
                currMaxY = data[y][x]
                visible[(y,x)] = (True, data[y][x], "y")
            if data[s-x][s-y] > currMaxXInv:
                currMaxXInv = data[s-x][s-y]
                visible[(s-x,s-y)] = (True, data[s-x][s-y], "xInv")
            if data[s-y][s-x] > currMaxYInv:
                currMaxYInv = data[s-y][s-x]
                visible[(s-y,s-x)] = (True, data[s-y][s-x], "yInv")
            if(x == 0 or y == 0 or x == s or y == s):
                visible[(x,y)] = (True, data[x][y])
                continue
    return len(visible)

def star2(data):
    s = len(data)-1
    maxdist = 0
    for x in range(s):
        for y in range(s):
            up = down = left = right = 0
            h = data[x][y]
            xc = x-1
            while xc >= 0:
                up += 1
                if data[xc][y] >= h:
                    break
                xc -= 1
            xc = x+1
            while xc <= s:
                down += 1
                if data[xc][y] >= h:
                    break
                xc += 1
            yc = y-1
            while yc >= 0:
                left += 1
                if data[x][yc] >= h:
                    break
                yc -= 1
            yc = y+1
            while yc <= s:
                right += 1
                if data[x][yc] >= h:
                    break
                yc += 1
            cd = up * down * left * right
            maxdist = max(maxdist, cd)
    return maxdist

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