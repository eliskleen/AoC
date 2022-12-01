using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Day16.Classes
{
    public class Packet
    {
        public int version { get; set; }
        public int typeId { get; set; }
        public int Length { get => this.getLenght(); set => length = value;}
        private int length;
        public int lengthTypeId { get; set; }
        public List<Packet> subPackets { get; set; }
        public long literalValue {get => getValue();}
        private long val;


        public Packet(string binary)
        {
            this.subPackets = new List<Packet>();
            this.version = Convert.ToInt32(binary.Substring(0, 3), 2);
            this.typeId = Convert.ToInt32(binary.Substring(3, 3), 2);
            binary = binary.Remove(0, 6);
            //Console.WriteLine(typeId);
            if(typeId == 4)
            { 
                binary = createLitteralValues(binary);
                return;
            }
            //else we have subpackets!!!
            this.lengthTypeId = Convert.ToInt32(binary[0].ToString(), 2);
            binary = binary.Remove(0, 1); //remove lengthTypeId
            if(lengthTypeId == 1) //we know the number of subpackets
            {
                var num = Convert.ToInt32(binary.Substring(0, 11), 2);
                binary = binary.Remove(0, 11);
                //Console.WriteLine(num);
                for(int i = 0; i < num; i++)
                {
                    var p = new Packet(binary);
                    subPackets.Add(p);
                    binary = binary.Remove(0, p.Length);
                }
                return;
            }
            //else we know how many bith the sub packets take up
            var usedLength = 0;
            var lengthToUse = Convert.ToInt32(binary.Substring(0, 15),2);
            binary = binary.Remove(0, 15);
            while(usedLength < lengthToUse)
            {    
                var subPacket = new Packet(binary);
                subPackets.Add(subPacket);
                binary = binary.Remove(0, subPacket.Length);
                usedLength += subPacket.Length;
            } 
            return;

        }
        public List<Packet> getAllSubPackets()
        {
            if(typeId == 4)
                return new Packet[0].ToList();
            var list = new List<Packet>();
            //list.AddRange(subPackets);
            foreach (var p in this.subPackets)
            {
                list.Add(p);
                var sub = p.getAllSubPackets();
                //Console.WriteLine("here");
                list.AddRange(sub);
            }
            return list;
        }
        string createLitteralValues(string binary)
        {
            length = 6;
            var current = "";
            //Console.WriteLine(binary);
            while(!binary[0].Equals('0'))
            {
                current += binary.Substring(1, 4); 
                binary = binary.Remove(0, 5);
                length+=5;
            }
            current += binary.Substring(1, 4); 
            binary = binary.Remove(0, 5);
            length+=5;
            //Console.WriteLine(current);

            val = Convert.ToInt64(current, 2);
            return binary;
        }
        long getValue()
        {
            switch (typeId)
            {
                case 4:
                    return val;
                case 0:
                    return subPackets.Sum(p => p.literalValue);
                case 1:
                    return subPackets.Aggregate(1, (long acc, Packet p) => acc * p.literalValue);
                case 2:
                    return subPackets.Min(p => p.literalValue);
                case 3:
                    return subPackets.Max(p => p.literalValue);
                case 5:
                    return subPackets[0].literalValue > subPackets[1].literalValue ? 1 : 0;
                case 6:
                    return subPackets[0].literalValue < subPackets[1].literalValue ? 1 : 0;
                case 7:
                    return subPackets[0].literalValue == subPackets[1].literalValue ? 1 : 0;
                default:
                    break;
            }
            return 0;
               
        }
        int getLenght()
        {
            if(typeId == 4)
                return length; //(6 + literalValues.Count*5);
            
            var lengthOfLengthType = lengthTypeId == 1 ? 11 : 15;
            return (7 + lengthOfLengthType + subPackets.Sum(p => p.Length));
            
        }
    }
}