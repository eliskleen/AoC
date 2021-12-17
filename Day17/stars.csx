using System.Numerics;
using System.Data.SqlTypes;
int xmin = 0, xmax = 0;
int ymin = 0, ymax = 0;

long main()
{
    var watch = new Stopwatch();
    watch.Start();
    var line = File.ReadAllLines("input.txt").ToList()[0];
    var xs = line.Split('=')[1].Split(',')[0].Split("..").ToList().ConvertAll(int.Parse);
    var ys = line.Split('=')[2].Split("..").ToList().ConvertAll(int.Parse);
    xmin = xs[0]; 
    xmax = xs[1];
    ymin = ys.Min();
    ymax = ys.Max();
    stars();
    watch.Stop();
    Console.WriteLine(watch.ElapsedMilliseconds);
    return 0;

}
(int, int) fx(int x, int vel, int t)
{
    for(int i = 0; i < t; i++)
    {
        x += vel;
        vel--;
        if(vel == 0)
            return (x, 0);
        
    }
    return (x, vel);
}
(bool, int, int) hitsX(int x, int vel)
{
    var t = 0;
    while(x <= xmax)
    {
        (x, vel) = fx(x, vel, 1);
        t++;
        if(x>= xmin && x<= xmax)
            return(true, t, vel);
        if(vel == 0)
            return(false, 0, 0);
    }
    return(false, t, 0);
}
bool hitsXIn(int x, int vel, int t)
{
    var res = fx(x, vel, t);
    if(res.Item1 >= xmin && res.Item1 <= xmax)
        return true;
    return false; 
}
bool hitsYIn(int y, int vel, int t)
{
    var res = fy(y, vel, t);
    return res.Item1 >= ymin && res.Item1 <= ymax;
}
(bool, int) hitsY(int vel)
{
    var y = 0;
    var t = 0;
    while(y > ymin)
    {
        y += vel;
        vel--;
        t++;
        if(y >= ymin && y <= ymax)
            return(true, t);
    }
    return(false, 0);
}
(int, int, int) fy(int y, int vel, int t)
{
    int ymax = y;
    for(int i = 0; i < t; i++)
    {
        y += vel;
        var smaller = Convert.ToInt32(ymax < y);
        var bigger = Convert.ToInt32(ymax >= y);
        ymax = smaller*y + bigger*ymax;
        vel--;
    }
    return (y, ymax, vel);
}

int getHeight(int vel)
{
    var max = 0;
    var y = 0;
    while(vel > 0)
    {
        y += vel;
        max = max < y ? y : max;
        vel--;
    }
    return max;
}
int stars()
{
    int maxYvel = 140; //this is weird
    var foundMax = 0;
    var foundHits = new Dictionary<(int, int), int>();
    (bool, int, int) hitx;
    for(int i = ymin; i<= maxYvel; i++)
    {
        var hity = hitsY(i);
        if(hity.Item1)
        {
            for(int xVel = 1; xVel <=xmax; xVel++)
            {
                hitx = hitsX(0, xVel);
                if(hitx.Item1 
                &&(hitsXIn(0, xVel, hity.Item2) || hitsYIn(0, i, hitx.Item2)))
                {
                    foundHits[(xVel, i)] = 1;
                    foundMax = getHeight(i) > foundMax ? getHeight(i) : foundMax;
                }
            }
        }
    }
    Console.WriteLine(foundMax);
    Console.WriteLine(foundHits.Count);
    Console.WriteLine("Max yvel: " + foundHits.Max(kvp => kvp.Key.Item2));
    return 0;

}
main();