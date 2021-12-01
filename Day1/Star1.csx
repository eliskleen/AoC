using System;

var lines = File.ReadAllLines("1.txt");
var inc = Enumerable.Range(1, lines.Length-1)
                    .Select(i => int.Parse(lines[i-1]) < int.Parse(lines[i]))
                    .ToList()
                    .Count(s => s == true);
Console.WriteLine(inc);
/*
var prev =lines[0];
foreach (var line in lines)
{
   if(int.Parse(line)  > int.Parse(prev))
        inc++;
    prev = line;
}
Console.WriteLine(inc);*/