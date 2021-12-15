using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Day15.Classes
{
    public class DirectedEdge
    {
        public Coord to { get; set; }
        public Coord from { get; set; }
        public int weight { get; set; }
        public DirectedEdge(Coord from, Coord to)
        {
            this.from = from;
            this.to = to;
            this.weight = to.risk;
        }
    }
}