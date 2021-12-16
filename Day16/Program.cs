using System.Diagnostics;
using System;
using System.Collections.Generic;
using System.Linq;
using Day16.Classes;
using System.IO;

namespace Day16 // Note: actual namespace depends on the project name.
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var watch = new Stopwatch();
            watch.Start();
            var dir = Directory.GetCurrentDirectory();
            var input = File.ReadAllLines(dir + @"\input.txt").ToList()[0];
            var bin = Converter.getBinaryFromHex(input);
            //Console.WriteLine(bin);
            var packet = new Packet(bin);
            var packets = packet.getAllSubPackets();
            var sum = packet.version + packets.Sum(p => p.version);

            var value = packet.literalValue;
            watch.Stop();
            Console.WriteLine("Sum of versions: " + sum);
            Console.WriteLine("Value of top package: " + value);
            Console.WriteLine("Time: " + watch.ElapsedMilliseconds + "ms");
            Console.ReadKey();

        }

    }
}