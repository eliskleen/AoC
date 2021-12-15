using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Day15.Classes
{
    public class Coord {
        public int x, y, risk;
        public Coord(int x, int y, int risk) {
            this.x = x;
            this.y = y;
            this.risk = risk;
        }
        public bool equals(Object o) {
            if (o == this) // equality of references
                return true;
            if (!(o is Coord))
                return false;
            Coord other = (Coord) o;
            return this.x == other.x && this.y == other.y && this.risk == other.risk;
        }

        public int hashCode() {
            return (this.x << 8) ^ this.y;
        }

    }
}
