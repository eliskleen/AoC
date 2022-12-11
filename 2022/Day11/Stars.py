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

class Monkey():
    def __init__(self, data, divByThree=True):
        self.divByThree = divByThree
        lines = data.split("\n")
        self.name = lines[0].split(" ")[1][:1]
        self.thrownItems = 0
        self.parseItems(lines[1])
        self.parseOp(lines[2])
        self.parseTest(lines[3], lines[4], lines[5])
        self.mod = 3
    def parseTest(self, test, true, false):
        self.div = int(test.split(" ")[-1])
        self.true = int(true.split(" ")[-1])
        self.false = int(false.split(" ")[-1])
    def parseOp(self, line):
        sym = line.split(" ")[-2]
        # print(f"val: {line.split(' ')[-1]}")
        v = line.split(" ")[-1]
        if(v == "old"):
            self.op = lambda x: x*x
            return
        val = int(v)
        if sym == "+":
            self.op = lambda x: x + val
        elif sym == "*":
            self.op = lambda x: x * val
        else:
            print(sym)
            raise Exception("Invalid op")
    def parseItems(self, line):
        line = line.split(":")[1].strip()
        line = line.split(",")
        self.items = [int(x) for x in line]


    def throw(self, ms):
        for i in range(len(self.items)):
        # for i in self.items:
            self.thrownItems += 1
            item = self.items.pop(0)
            wl = self.op(item)
            # print(f"{self.name} gets {wl} from {i}")
            if self.divByThree:
                wl = wl//3
            else:
                wl = wl%self.mod # this is wack
            t = self.doTest(wl) 
            # print(f"{self.name} throws {int(wl/3)} to {ms[t].name}")
            ms[t].items.append(wl)



    def doTest(self, wl):
        if wl % self.div == 0:
            return self.true
        else:
            return self.false



def get_data(path):
    with open(path) as f:
        return f.read().split("\n\n")
def star1(data):
    ms = []
    rounds = 20
    for d in data:
        ms.append(Monkey(d))
    for i in range(rounds):
        for m in ms:
            m.throw(ms)

    print(f"ms: {len(ms)}")
    for m in ms:
        # print(f"{m.name} holds {m.items} items after {rounds} rounds")
        print(f"{m.name} threw {m.thrownItems} items")

    max = (list(sorted(ms, key=lambda x: x.thrownItems))[-2:])



    return max[0].thrownItems*max[1].thrownItems

def star2(data):
    ms = []
    rounds = 10_000
    for d in data:
        ms.append(Monkey(d, False))
        # ms.append(Monkey(d))
    div = 1
    for m in ms:
        div *= m.div
    for m in ms:
        m.mod = div

    for i in range(rounds):
        if(i % 100 == 0):
            print(f"round: {i}")
        for m in ms:
            m.throw(ms)

    print(f"ms: {len(ms)}")
    for m in ms:
        # print(f"{m.name} holds {m.items} items after {rounds} rounds")
        print(f"{m.name} threw {m.thrownItems} items")

    max = (list(sorted(ms, key=lambda x: x.thrownItems))[-2:])


    return max[0].thrownItems*max[1].thrownItems

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