var lines = File.ReadAllLines("input1.txt").ToList();
int aim = 0, depth = 0, hori = 0;;
var val = 0;
foreach (var line in lines)
{
    val = int.Parse(line.Split(' ').Last());
    if(line.Contains("f"))
    {
        hori += val;
        depth += aim*val;
        continue;
    }
    if(line.Contains("u"))
        val *= -1;
    aim += val;
}
Console.WriteLine(hori*depth);