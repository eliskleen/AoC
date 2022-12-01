long main()
{
    var watch = new Stopwatch();
    watch.Start();
    var crabPos = File.ReadAllText("input.txt").Split(',').ToList().ConvertAll(int.Parse);
    stars(crabPos, dist);// ~18 ms on avarage to run
    stars(crabPos, weridSum); // ~28 ms on avarage to run
    watch.Stop();
    Console.WriteLine("Time: "+watch.ElapsedMilliseconds+" ms");
    return watch.ElapsedMilliseconds;

}
int weridSum(int a, int b)
{
    var sum = 0;
    var max = Math.Abs(a-b);
    var min = 1; 
    sum = ((max+min)*max)/2;
    return sum;
}
int dist(int a, int b)
{
    return Math.Abs(a-b);
}
void stars(List<int> crabPos, Func<int, int, int> calc)
{
    var cost = -1;
    var move = 0;
    for(int i = crabPos.Min(); i <=crabPos.Max(); i++)
    {
        var nCost = crabPos.Select(c => calc(c, i)).Sum();
        //if the cost increases we know the lats one was the best
        if(nCost > cost && cost != -1)
            break;
        if(cost == -1 || nCost < cost)
        {
            cost = nCost;
            move = i;
        }
    }
    Console.WriteLine("Cost: "+cost+" Pos: "+move);
}
long sum = 0;
var times = 1;
for(int i = 0; i< times; i++)
    sum += main();
Console.WriteLine("Avarage of "+times+ " runs: "+sum/times);