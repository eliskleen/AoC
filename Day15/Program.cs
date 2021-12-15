using System.Diagnostics;
using System;
using System.Collections.Generic;
using System.Linq;
using Day15.Classes;

namespace Day15 // Note: actual namespace depends on the project name.
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var watch = new Stopwatch();
            watch.Start();
            var pathFinder = new PathFinder(@"\input.txt", false, true);
            var start = pathFinder.graph.grid[0,0];
            var size = (pathFinder.graph.grid.GetLength(0), pathFinder.graph.grid.GetLength(1));
            var end = pathFinder.graph.grid[size.Item1-1, size.Item2-1];
            Console.WriteLine(pathFinder.getCost(start, end));
            watch.Stop();
            Console.WriteLine(watch.ElapsedMilliseconds);



            /*var dir = Directory.GetCurrentDirectory();
            var map = File.ReadAllLines(dir + @"\biggermap.txt").ToList();
            var grid = new Coord[map[0].Count(), map.Count()];
            int x = 0, y = 0;
            foreach (var line in map)
            {
                x = 0;
                foreach (var c in line.ToList())
                {
                    var pos = new Coord(x, y, int.Parse(c.ToString()));
                    if(!pathFinder.graph.grid[x, y].equals(pos))
                        Console.WriteLine("wrong at: " + pos.x + "," + pos.y + " " + pos.risk);
                    x++;
                }
                y++;
            }*/
            
        }
    }
}