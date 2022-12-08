import time
import collections as collections

def day_():
    path = "data.txt"
    # path = "test-data.txt"

    start_time = time.perf_counter()
    data = get_data(path)

    time1 = time.perf_counter()

    (ans1,ans2) = stars(data)
    time2 = time.perf_counter()

    # ans2 = star2(data)
    # time3 = time.perf_counter()

    load_time = time1 - start_time
    star1_time = time2 - time1
    if 1:
        print(f'Load time: {load_time}')
        print(f'Star 1 and 2 time: {star1_time}')
        print(f'Star 1 answer: {ans1}')
        print(f'Star 2 answer: {ans2}')

def get_data(path):
    with open(path) as f:
        return f.read().splitlines()
    
totSpace = 70000000
unUsedNeeded = 30000000

def stars(data):
    dirSize = collections.Counter()
    currDirrs = []
    possibleDirs = collections.defaultdict()
    cnt = 0
    i = 0
    while i < len(data):
        line = data[i]
        # line = line.removeprefix("$ ")
        # print(f"line: {line}")
        if line == "$ cd ..":
            # print("popping")
            currDirrs.pop()
            i += 1
        elif line.startswith("$ cd "):
            d = line.removeprefix("$ cd ")
            if(d == "/" or d in possibleDirs[currDirrs[-1]]):
                # print("appending")
                currDirrs.append(d)
            else:
                print(f"not appending {d} to currDirrs")
            i += 1
        elif line.startswith("$ ls"):
            # print("ls")
            # print(f"currDirr: {currDirrs[-1]}")
            i += 1
            line = data[i]
            while(i < len(data) and not data[i].startswith("$ ")):
                # print(f"data[i]: {data[i]}")
                line = data[i]
                if not line.startswith("dir "):
                    size = int(line.split()[0])
                    for j in range(len(currDirrs)): # BRUH
                        name = "/".join(currDirrs[:j+1])
                        dirSize[name] += size
                    # for dirr in currDirrs:
                        # dirSize[dirr] += size
                else:
                    cnt += 1
                    # print(f"adding {line.removeprefix('dir ')} to possibleDirs")
                    # print(f"currDirrs: {currDirrs}")
                    dirr = currDirrs[-1]
                    possibleDirs.setdefault(dirr, []).append(line.removeprefix("dir "))
                i += 1

    dz = list(dirSize.items())
    # print(dz)
    print(f"count: {cnt}")
    s1 = sum([x[1] for x in dz if x[1] <= 100_000])

    currSize = dz[0][1]
    print(f"currSize: {currSize}")
    currUnused = totSpace - currSize
    spaceToRemove = unUsedNeeded-currUnused
    print(f"spaceToRemove: {spaceToRemove}")
    s2 = sorted([x[1] for x in dz if x[1] > spaceToRemove])[0]

    return (s1,s2)

def star2(data):
    #dirSizes is sirdet by star1
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