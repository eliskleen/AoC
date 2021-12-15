using System.Runtime.InteropServices;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.IO;

namespace Day15.Classes
{
    public class PathFinder
    {
        public Graph graph { get; set; }
        public PathFinder(string fileName, bool printGraph = false, bool replicate = false)
        {
            var dir = Directory.GetCurrentDirectory();
            var lines = File.ReadAllLines(dir + fileName).ToList();
            graph = new Graph(lines, replicate);
            if(!printGraph)
                return;
            for (int i = 0; i < graph.grid.GetLength(1); i++)
            {
                for (int j = 0; j < graph.grid.GetLength(0); j++)
                {
                    Console.Write(graph.grid[j, i].risk);
                }
                Console.WriteLine("");
            }
        }
        public int getCost(Coord start, Coord end)
        {
            var visited = new HashSet<Coord>();
            var pqueue = new PriorityQueue<PQEntry, double>();
            pqueue.Enqueue(new PQEntry(start, 0, int.MaxValue, null), int.MaxValue);
            while(pqueue.TryDequeue(out PQEntry? entry, out double guessedCost))
            {
                if(visited.Contains(entry.node))
                    continue;
                visited.Add(entry.node);
                if(entry.node.equals(end))
                    return entry.costToHere;
                foreach (var edge in graph.GetDirectedEdges(entry.node))
                {
                    var costToNext = entry.costToHere + edge.weight; 
                    var guessedCostToEnd = graph.guessCost(edge.to, end)
                                         + costToNext;  
                    pqueue.Enqueue(new PQEntry(edge.to, costToNext, guessedCostToEnd, entry), guessedCostToEnd);
                }
            }
            return -1;
        }
        LinkedList<Coord> extractPath(PQEntry entry)
        {
            var path = new LinkedList<Coord>();
            var current = entry;
            while(current.backPointer != null)
            {
                path.AddFirst(current.node);
                current = current.backPointer;
            }
            path.AddFirst(current.node);
            return path;
        }
        private class PQEntry {
            public Coord node;
            public int costToHere; // kostnad för hela vägen
            public PQEntry? backPointer;

            public double guessedCostToGoal; // kostnaden att gå till målet
            public PQEntry(Coord n, int c, double gc, PQEntry? bp) {
                this.node = n;
                this.costToHere = c;
                this.backPointer = bp;
                this.guessedCostToGoal = gc;
                //this(n, c, 0, bp);
            }
           /* public PQEntry(Coord n, Coord c, int cn, PQEntry bp) {
                node = n;
                costToHere = c;
                guessedCostToGoal = cn;
                backPointer = bp;
            }*/

        }
    }
}