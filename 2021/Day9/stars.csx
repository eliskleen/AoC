long main()
{
    var watch = new Stopwatch();
    watch.Start();
    var vals = File.ReadAllLines("input.txt").Select(s => s.Select(c => (int.Parse(c.ToString()))).ToList()).ToList();
    var lowPoints = getImprovedLows(vals);
    //var lowPoints = g netLowPoints(vals);
    var one = star1(vals, lowPoints);
    var two = star2(vals, lowPoints);
    watch.Stop();
   // Console.WriteLine(one + " " + two);
    return watch.ElapsedMilliseconds;
    //~20 ms first run, when ran 300 times in a row it avarages about 5 ms
}
int star2(List<List<int>> vals, List<(int, int, int)> lowPoints = null)
{
    if(lowPoints == null)
        lowPoints = getLowPoints(vals).ToList();
    var map = vals.Select(s => s.Select(c => (c, false)).ToList()).ToList();
    var basins = new List<int>();
    foreach (var point in lowPoints)
        basins.Add(countBasinSize(map, point.Item2, point.Item3));

    basins.Sort();
    basins.Reverse();
    var sum = 1;
    basins.GetRange(0, 3).ForEach(b => sum *= b);
    return sum;
}
int countBasinSize(List<List<(int, bool)>> vals, int x, int y)
{
    var basin = 0;
    var xMax = vals.Count;
    var yMax = vals[0].Count;
    var testVal = vals[x][y].Item1; 
    var coords = new (int, int)[4]{(x-1, y), (x+1, y),
                                   (x, y-1), (x, y+1)}.ToList();
    if(!vals[x][y].Item2)
    {
        basin++;
        vals[x][y] = (vals[x][y].Item1, true);
    } 
    foreach (var c in coords)
    {
        if(c.Item1 < 0 || c.Item1 > xMax -1
        || c.Item2 < 0 || c.Item2 > yMax -1)
            continue;
        var current = vals[c.Item1][c.Item2];
        if(!current.Item2//not visited
        && current.Item1 < 9) //small enough
        {
            current.Item2 = true;
            vals[c.Item1][c.Item2] = current;
            basin++;
            basin += countBasinSize(vals, c.Item1, c.Item2) ;   
        }   
    }
    return basin;
}
int star1(List<List<int>> vals, List<(int, int, int)> lowPoints = null)
{
    if(lowPoints == null)
        lowPoints = getLowPoints(vals).ToList();
    return lowPoints.Select(s => s.Item1+1).Sum();
}
List<(int, int, int)> getImprovedLows(List<List<int>> vals)
{
    var visited = vals.Select(s => s.Select(c => false).ToList()).ToList();
    var lowPoints = new List<(int, int, int)>(); 
    int x = -1, y = 0;
    foreach (var line in vals)
    {
        x++;
        y = 0;
        foreach (var coord in line)
        {
            if(visited[x][y])
                continue;
            visited[x][y] = true;
            var smallestNeighbour = getSmalestNeighbour(vals, x, y);
            if(smallestNeighbour.Item1 > coord)
                lowPoints.Add((coord, x, y));
            y++;
        }
    }
    return lowPoints;       
}
List<(int, int, int)> getLowPoints(List<List<int>> vals)
{
    var lowPoints = new List<(int, int, int)>();
    for(int i = 0; i < vals.Count; i++)
    {
        for(int j = 0; j < vals[0].Count; j++)
        {
            var smallestNeighbour = getSmalestNeighbour(vals, i, j);
            if(smallestNeighbour.Item1 > vals[i][j])
                lowPoints.Add((vals[i][j], i, j));
       }
    }
    return lowPoints;
}
(int, int, int) getSmalestNeighbour(List<List<int>> vals, int x, int y)
{
    var xMax = vals.Count;
    var yMax = vals[0].Count;
    var coords = new (int, int)[4]{(-1, 0), (1, 0),
                            (0, -1), (0, 1)}.ToList();
    var smallest = 10;
    int i = -1;
    int j = -1;
    foreach (var c in coords)
    {
        i = c.Item1;
        j = c.Item2;
        if(i+x < 0 || i+x > xMax -1
        || j+y < 0 || j+y > yMax -1)
            continue;
        if(vals[x+i][y+j] < smallest)
            smallest = vals[x+i][y+j]; 
    }
    return (smallest, i, j);
}
long sum = 0;
var times = 300;
for(int i = 0; i< times; i++)
    sum += main();
Console.WriteLine("Avarage of "+times+ " runs: "+(float)sum/(float)times);
Console.WriteLine(sum);