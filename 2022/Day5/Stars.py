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
        data = f.read().split("\n\n")
        boxes = data[0].split("\n")
        dict = {}
        rows = boxes.pop().split(' ')
        rows = list(filter(lambda r : r != '', rows))
        rows = list(map(int, rows))
        for i in range(rows[-1]):
            dict[i] = []
        n = 0
        for r in boxes:
            bs = [r[x:x+4].strip().replace("[", "").replace("]", "") for x in range(0, len(r), 4)]
            for i in range(len(bs)):
                if(bs[i] != ''):
                    dict[i].append(bs[i])
        moves = []
        for r in data[1].split('\n'):
            l = r.split(' ')
            moves.append((int(l[1]), int(l[3]), int(l[5])))
        return dict.copy(), moves

def star1(data):
    d, moves = data
    dict = {}
    for i in d:
        dict[i] = d[i].copy()
    for m in moves:
        for i in range(m[0]):
            dict[m[2]-1].insert(0,dict[m[1]-1].pop(0))
    ret = ""
    for i in range(len(dict)):
        ret += "".join(dict[i][0])
    return ret

def star2(data):
    dict, moves = data
    for m in moves:
        dict[m[2]-1] = (dict[m[1]-1][:m[0]]) + dict[m[2]-1]
        dict[m[1]-1] = dict[m[1]-1][m[0]:]
    ret = ""
    for i in range(len(dict)):
        ret += "".join(dict[i][0])
    return ret

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