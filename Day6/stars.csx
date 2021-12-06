long main()
{
    var wath = new Stopwatch();
    wath.Start();

    var lines = File.ReadAllLines("input.txt").ToList();
    var fish = lines[0].Split(',')
                       .ToList()
                       .ConvertAll(int.Parse);
    star2(fish, 80);
    star2(fish, 256);
    wath.Stop();
    Console.WriteLine(wath.ElapsedMilliseconds);
    return wath.ElapsedMilliseconds;
}
void star2(List<int> fishList, float days)
{
   var fish = new long[9];
   foreach (var f in fishList)
       fish[f]++;
    var newFish = new long[9];
    for(int i = 0; i < days; i++)
    {
        var zeros = newFish[0];
        for (int j = 8; j > 0; j--)
            newFish[(j-1)] = fish[j];
        newFish[6] += zeros;
        newFish[8] = zeros;
        Array.Copy(newFish, fish, 9);
    }
    long sum = 0;//fish.Sum();
    for (int j = 8; j >= 0; j--)
            sum += fish[j];
    Console.WriteLine(sum);
}
//wont use this but this is the sol for star1
int star1(List<int> fish, int days)
{
    for (int i = 0; i < days; i++)
    {
        int spawned = fish.Count(f => f == 0);
        fish = fish.Select(f => f-1).ToList();
        fish.RemoveAll(f => f == -1);
        for(int j = 0; j < spawned; j++)
        {
            fish.Add(8);
            fish.Add(6);
        }
    }
    Console.WriteLine(fish.Count); 
    return fish.Count;
}
long sum = 0;
var times = 30;
for(int i = 0; i< times; i++)
    sum += main();
//this gives avarage = 0ms and about 15000 ticks
Console.WriteLine("Avarage of "+times+ " runs: "+sum/times);