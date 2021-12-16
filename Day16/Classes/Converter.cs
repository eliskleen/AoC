using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Day16.Classes
{
    public static class Converter
    {
        static Dictionary<char, string> swaps =new Dictionary<char, string> {{'A', "10"}
                                                  ,{'B', "11"}
                                                  ,{'C', "12"}
                                                  ,{'D', "13"}
                                                  ,{'E', "14"}
                                                  ,{'F', "15"}};
        public static string getBinaryFromHex(string str)
        {
            var ret = "";
            var val = 0;
            foreach (var ch in str)
            {
                if(swaps.ContainsKey(ch))
                {
                    val = int.Parse(swaps[ch]);
                    ret += Convert.ToString(val, 2).PadLeft(4, '0');
                    continue;
                }
                val = int.Parse(ch.ToString());
                ret += Convert.ToString(val, 2).PadLeft(4, '0');
            }
            return ret;
        }
    }
}