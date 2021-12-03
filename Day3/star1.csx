using System;
var lines = File.ReadAllLines("input.txt").ToList();
var ints = lines.Select(s => s        
                .Select(ss => int.Parse(ss.ToString()))
                .ToList())
                .ToList();
var sums = ints.SelectMany(x => x
                           .Select((v, i) => new {Value = v, Index = (i % ints.First().Count)})).ToList()
                           .GroupBy(x => x.Index).ToList()
                           .Select(y => y.Sum(z => z.Value)).ToList();

var strs = sums.Select(s => s > ints.Count/2 ? "1" : "0").ToList();

var gamma = Convert.ToInt32(
       string.Join("", strs), 2);
var epsilon = Convert.ToInt32(
       string.Join("", strs.Select(s => s == "1" ? "0" : "1")), 2);
Console.WriteLine(gamma*epsilon);

