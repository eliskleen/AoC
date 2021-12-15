using System.Diagnostics;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Day15.Classes
{
    public class Graph
    {
        public Coord[,] grid { get; set; } 
        public Graph(List<string> lines, bool replicate = false)
        {
            grid = new Coord[lines[0].Count(), lines.Count()];
            int x = 0, y = 0;
            var newGrid = new Coord[lines[0].Count() * 5, lines.Count()*5];
            foreach (var line in lines)
            {
                x = 0;
                foreach (var c in line.ToList())
                {
                    grid[x, y] = new Coord(x, y, int.Parse(c.ToString()));
                    newGrid[x, y] = grid[x, y];
                    x++;
                }
                y++;
            }
            if(!replicate)
                return;
            
            for(int repy = 0; repy < 5; repy++)
            {
                for(int repx = 0; repx < 5; repx++)
                {
                    if(repx == 0 && repy == 0)
                        continue;
                    for (int i = 0; i < grid.GetLength(0); i++)
                    {
                        for (int j = 0; j < grid.GetLength(1); j++)
                        {
                            x = i + (repx*grid.GetLength(0));
                            y = j + (repy*grid.GetLength(1));
                            var getx = repx > 0 ? x-grid.GetLength(0) : x;
                            var gety = repx == 0 ? y-grid.GetLength(1) : y;
                            //y = y > 9 ? y-10 : y;
                            //Console.WriteLine(x + "," + y + "," + repx);
                            var newRisk = (newGrid[getx, gety].risk + 1);
                            var c = new Coord(x, y, newRisk > 9 ? 1 : newRisk);
                            newGrid[x, y] = c;
                            //Console.WriteLine(x);
                        }
                    }
                }
            }
            grid = newGrid;
        }
        public double guessCost(Coord p, Coord q) 
        {
        return Math.Sqrt(Math.Pow((p.x - q.x), 2) + Math.Pow((p.y - q.y), 2));
        }
        public List<DirectedEdge> GetDirectedEdges(Coord p)
        {
            var ret = new List<DirectedEdge>();
            Coord found;
            var coords = new (int, int)[4]{(p.x-1, p.y)
                                          ,(p.x+1, p.y)
                                          ,(p.x, p.y-1)
                                          ,(p.x, p.y+1)}.ToList();
            foreach (var c in coords)
                if(isInside(c.Item1, c.Item2))
                {
                    found = grid[c.Item1, c.Item2];
                    ret.Add(new DirectedEdge(p, found));
                }
            return ret;
        }
        bool isInside(int x, int y)
        {
            return x >= 0 && y >= 0
                && x < grid.GetLength(0)
                && y < grid.GetLength(1);
        }
    }
}