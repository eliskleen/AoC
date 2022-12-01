
using System.Collections;
long star1(int steps, string str)
{
    var state = new Dictionary<string, long>();
    var charCount = new Dictionary<char, long>();
    for (int i = 0; i < str.Length-1; i++)
    {
       var pair = "" + str[i] + str[i+1];
       state[pair] = state.ContainsKey(pair) ? state[pair] + 1 : 1; 
    }
    foreach (var p in str)
        charCount[p] = charCount.ContainsKey(p) ? charCount[p] + 1 : 1;
        

    for (int i = 0; i < steps; i++)
        state = step(state, charCount);
    var max = charCount.Values.Max();
    var min = charCount.Values.Min();
    return  max-min;
}
Dictionary<string, long> step(Dictionary<string, long> state, Dictionary<char, long> charCount)
{
    var newState = new Dictionary<string, long>();
    foreach (var kvp in state)
    {
        var newCh = inserters[kvp.Key];
        charCount[newCh] = charCount.ContainsKey(newCh) ? 
                           charCount[newCh] + kvp.Value 
                         : kvp.Value;
        var pair1 = "" + kvp.Key[0] + inserters[kvp.Key];
        var pair2 = "" + inserters[kvp.Key] + kvp.Key[1];
        newState[pair1] = newState.ContainsKey(pair1) ? newState[pair1] + kvp.Value : kvp.Value;
        newState[pair2] = newState.ContainsKey(pair2) ? newState[pair2] + kvp.Value : kvp.Value;
    }
    return newState;
}

var inserters = new Dictionary<string, char>();
long main()
{
    var lines = File.ReadAllLines("input.txt").ToList();
    var str = lines[0];
    lines.RemoveRange(0, 2);
    
    foreach (var line in lines)
    {
        var split = line.Split(' ');
        inserters.Add(split.First(), split.Last()[0]);
    }
    var watch = new Stopwatch();
    watch.Start();
    Console.WriteLine(star1(40, str));
    watch.Stop();
    Console.WriteLine(watch.ElapsedMilliseconds);
    return 0;
}

main();