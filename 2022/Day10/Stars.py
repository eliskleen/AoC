import time

def day_():
    path = "data.txt"
    path = "test-data.txt"

    start_time = time.perf_counter()
    data = get_data(path)

    time1 = time.perf_counter()

    (ans1, ans2) = stars(data)
    time2 = time.perf_counter()


    load_time = time1 - start_time
    star1_time = time2 - time1
    if 1:
        print(f'Load time: {load_time}')
        print(f'Star 1 and 2 time: {star1_time}')
        print(f'Star 1 answer: {ans1}')
        print(f'Star 2 answer: \n{ans2}')

def get_data(path):
    with open(path) as f:
        return list(map(lambda r : r.split(" ") if " " in r else [r, ''], f.read().splitlines()))
    


class CPU:
    def __init__(self) -> None:
        self.x = 1
        self.cycle = 1
        self.ss = 0
        self.printStr = ""
        self.drawCTR(self.x, self.cycle)

    def noop(self):
        self.cycle += 1
        self.ss = self.checkCycle(self.x, self.ss, self.cycle)

    def addx(self, val):
        self.cycle += 1
        self.ss = self.checkCycle(self.x, self.ss, self.cycle)
        self.cycle += 1
        self.x += int(val)
        self.ss = self.checkCycle(self.x, self.ss, self.cycle)

    def checkCycle(self, x, ss, cycle):
        self.drawCTR(x, cycle)
        t = 20
        c = cycle
        if cycle > 20:
            c -= 20
            t = 40
        if c % t == 0:
            print(f"cycle: {cycle}, x: {x}, ss: {ss}, x*cycle: {x*cycle}")
            return ss + x*cycle
        return ss

    def drawCTR(self, x, cycle):
        c = cycle % 40
        if abs (x+1-c) < 2:
            self.printStr += "#"
        else:
            self.printStr += "."
        if cycle % 40 == 0:
            self.printStr += "\n"
            return

def stars(data):
    cpu = CPU()
    for (inst, val) in data:
        if inst == "addx":
            cpu.addx(val) 
        elif inst == "noop":
            cpu.noop()
    return (cpu.ss, cpu.printStr)

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