using System;
var stopwatch = new Stopwatch();
var lines = File.ReadAllLines("1.txt").ToList();
stopwatch.Start();
var ints = lines.ConvertAll(int.Parse).ToList();
var sums = Enumerable.Range(0, ints.Count-2)
                     .Select(i => ints[i] + ints[i+1] + ints[i+2])
                     .ToList();
var incs = Enumerable.Range(1, sums.Count-1)
                     .Select(i => sums[i] > sums[i-1])
                     .ToList()
                     .Count(s => s == true);
stopwatch.Stop();
Console.WriteLine(incs);
Console.WriteLine(stopwatch.ElapsedMilliseconds);
