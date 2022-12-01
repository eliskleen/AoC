var lines = File.ReadAllLines("input1.txt").ToList();
var depth = lines.FindAll(s => s.Contains("up") || s.Contains("down"));
var forward = lines.FindAll(s => s.Contains("forward"));
var neg = depth.FindAll(s => s.Contains("u"))
               .Select(s => int.Parse(s.Split(' ').Last()))
               .Sum();
var pos = depth.FindAll(s => s.Contains("d"))
               .Select(s => int.Parse(s.Split(' ').Last()))
               .Sum(); 
var sumForward = forward.Select(s => int.Parse(s.Split(' ').Last())).Sum();
Console.WriteLine((pos-neg) * sumForward);