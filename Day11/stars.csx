using System.Reflection.Emit;
long main()
{
    var oct = getInput();
    var one = star1(oct, 100);
    oct = getInput();
    var two = star2(oct);
    Console.WriteLine(one.Item1 + " " + two);
    return 0;
                                
}
List<List<int>> getInput()
{
    return File.ReadAllLines("input.txt").Select(s => s.Select(c => (int.Parse(c.ToString()))).ToList()).ToList();
}
int star2(List<List<int>> oct)
{
    var same = false;
    var steps = 0;
    while(!same)
    {
        oct = star1(oct, 1).Item2;
        steps++;
        if(!oct.SelectMany(x => x).Any(o => o != oct[0][0]))
            break;
    }
    steps += (9 - oct.First().First())%9;
    return steps;
}
(int, List<List<int>>) star1(List<List<int>> oct, int steps)
{
    var flashes = 0;
    for (int i = 0; i < steps; i++)
    {
        for (int x = 0; x < oct.Count; x++)
            for (int y = 0; y < oct.Count; y++)
                flashes += incOct(oct, x, y);  
        oct = oct.Select(l => l = l.Select(o => o = o > 9 ? 0 : o).ToList()).ToList();
    }
   return (flashes, oct);           
}
int incOct(List<List<int>> oct, int x, int y)
{
    oct[x][y]++;
    var flashes = 0;
    if(oct[x][y] == 10)
    {
        flashes++;
        foreach (var adj in getAdj(x, y).Where(c => isInside(c, oct.Count)))
            flashes += incOct(oct, adj.Item1, adj.Item2);
    }
    return flashes;
}
List<(int, int)> getAdj(int x, int y)
{
    return new (int, int)[8]{(x-1, y-1)
                            ,(x-1, y)
                            ,(x-1, y+1)
                            ,(x, y-1)
                            ,(x, y+1)
                            ,(x+1, y-1)
                            ,(x+1, y)
                            ,(x+1, y+1)}.ToList();
}
bool isInside((int, int) coord, int size)
{
    return coord.Item1 >= 0 &&
           coord.Item2 >= 0 &&
           coord.Item1 <  size &&
           coord.Item2 <  size;
}
main();