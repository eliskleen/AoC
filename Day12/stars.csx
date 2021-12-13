class Tunnle
{
    public Tunnle(Cave to, Cave from)
    {
        this.to = to;
        this.from = from;
    }
    public Cave to { get; set; }
    public Cave from { get; set; }
    public bool contains(Cave c)
    {
        return from.Equals(c) || to.Equals(c);
    }
    public override bool Equals(object obj)
    {
        if(obj is not Tunnle)
            return false;
        var t = obj as Tunnle;
        return ((t.from.Equals(this.from) && t.to.Equals(this.to)));
             //|| (t.to.Equals(this.from) && t.from.Equals(this.to)));
    }
}
class Cave 
{
    public Cave(string name)
    {
        this.name = name;
        visited = false;
        small = Char.IsLower(name[0]);
        connectedTunnles = new List<Tunnle>();
    }
    public string name { get; set; }   
    public bool visited { get; set; }
    public bool small { get; set; }
    public List<Tunnle> connectedTunnles { get; set; }
    public List<Tunnle> getOutgoingTunnles()
    {
        var ret = new List<Tunnle>();
        foreach (var tunnle in this.connectedTunnles)
        {
            var to = tunnle.from.Equals(this) ? tunnle.to : tunnle.from;
            ret.Add(new Tunnle(to, this));
        }
        return ret;
    }
    public override bool Equals(object obj)
    {
        if(obj is not Cave)
            return false;
        return (obj as Cave).name == this.name; 
    }
}
class CaveSystem 
{
    public CaveSystem(List<string> input)
    {
        this.caves = new List<Cave>();

        this.tunnles = new List<Tunnle>();
        var split = new List<string>();
        string fromName;
        string toName;
        Cave to;
        Cave from;
        Tunnle tunnel;
        foreach (var line in input)
        {
            split = line.Split('-').ToList();
            fromName = split[0];
            toName = split[1];
            to = new Cave(toName);
            from = new Cave(fromName);
            tunnel = new Tunnle(to, from);
            if(!caves.Contains(to))
                caves.Add(to);
            if(!caves.Contains(from))
                caves.Add(from);
            tunnles.Add(tunnel);
        }
        foreach (var t in tunnles)
        {
            caves.Find(c => c.name == t.from.name)
                 .connectedTunnles.Add(t);
            caves.Find(c => c.name == t.to.name)
                 .connectedTunnles.Add(new Tunnle(t.from, t.to));
        }
    }
    public List<Cave> caves { get; set; } 
    public List<Tunnle> tunnles { get; set; }   

    public List<List<Tunnle>> getPathsFrom(Cave from, Cave to, int maxInSmall)
    {
        var paths = new List<List<Tunnle>>();
        var stack = new List<(Tunnle[], Cave)>();
        foreach (var tunnle in from.getOutgoingTunnles())
        {
            var arr = new Tunnle[1]{tunnle};
            stack.Add((arr, arr[0].to));    
        }
        var path = new List<Tunnle>();
        Cave next = stack[0].Item2;
        while(stack.Count != 0)
        {
            var current = stack.First(); 
            current.Item2 = caves.FirstOrDefault(c => c.Equals(current.Item2));
            stack.Remove(current);
            if(current.Item2.Equals(to))
            {
                if(!paths.Contains(current.Item1.ToList()))
                    paths.Add(current.Item1.ToList());
                continue;
            }
             var smalls = current.Item1.Where(t => t.to.small).Select(t => t.to).ToList();
            foreach (var outgoing in current.Item2.getOutgoingTunnles())
            {
               
                if(outgoing.to.small)
                    smalls.Add(outgoing.to);
                var dups = smalls.GroupBy(c => c.name).Where(c => c.Count() >= maxInSmall).ToList().Count;
                smalls.Remove(outgoing.to);
                if(dups > 1 && outgoing.to.small && maxInSmall > 1)
                    continue;
                if(smalls.GroupBy(c => c.name).Any(g => g.Count() > maxInSmall))
                    continue;
                if(outgoing.to.Equals(from))
                    continue;
                var arr = new Tunnle[current.Item1.Length + 1];
                current.Item1.CopyTo(arr, 0);
                arr[current.Item1.Length] = outgoing;
                if(!stack.Contains((arr, outgoing.to)))
                    stack.Add((arr, outgoing.to));
                    
            }
        }
        return paths;
    }
    bool contains(List<List<Tunnle>> paths, List<Tunnle> path)
    {
    if(paths.Count == 0)
        return false; 
    if(paths.All(p => p.Count != path.Count))
        {
            var pp = paths.Where(l => l.Count >= path.Count)
                          .Select(r => r.GetRange(0, path.Count)).ToList();
            return contains(pp, path); 
        }
    foreach (var p in paths)
    {
        if(p.Count != path.Count)
            continue;
        var s = true;
        for (int i = 0; i < p.Count; i++)
        {
            if(!p[i].Equals(path[i]))
                s = false;       
        }
        if(s)
            return true;
    }
    return false;
}
}
int star1(CaveSystem sys, Cave start, Cave end, bool print)
{
    var paths = sys.getPathsFrom(start, end, 1);
    if(print)
        foreach (var path in paths)
        {
                foreach (var tunnle in path)
                    Console.Write(tunnle.from.name + ",");
                Console.WriteLine(path.Last().to.name);
        }
    return paths.Count;
}
int star2(CaveSystem sys, Cave start, Cave end, bool print)
{
    var paths = sys.getPathsFrom(start, end, 2);
    if(print)
        foreach (var path in paths)
        {
                foreach (var tunnle in path)
                    Console.Write(tunnle.from.name + ",");
                Console.WriteLine(path.Last().to.name);
        }
    return paths.Count;
}
long main()
{
    var lines = File.ReadAllLines("input.txt").ToList();
    var sys = new CaveSystem(lines);
    var start = sys.caves.Find(c => c.name == "start");
    var end = sys.caves.Find(c => c.name == "end");
    var watch = new Stopwatch();
    watch.Start();
    var one = star1(sys, start, end, false);
    var two = star2(sys, start, end, false);
    watch.Stop();
    Console.WriteLine(one + " " + two + " " + watch.ElapsedMilliseconds);
    return watch.ElapsedMilliseconds;
}
long sum = 0;
var times = 10;
for(int i = 0; i< times; i++)
    sum += main();
Console.WriteLine("Avarage of "+times+ " runs: "+(float)sum/(float)times);
Console.WriteLine(sum);