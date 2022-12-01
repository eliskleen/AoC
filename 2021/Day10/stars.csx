var pairs = new (char, char)[4]{('(', ')'),
                                    ('[', ']'),
                                    ('{', '}'),
                                    ('<', '>')}.ToList();
long main()
{
    var lines = File.ReadAllLines("input.txt").ToList();
    var points = new (char, int)[4]{(')', 3),
                                    (']', 57),
                                    ('}', 1197),
                                    ('>', 25137)}.ToList();
    
    var one = star1(lines, points);
    var two = star2(lines);
    Console.WriteLine(one + " " + two);
    return 0;
}
long star2(List<string> lines)
{
    var points = new (char, int)[4]{(')', 1),
                                    (']', 2),
                                    ('}', 3),
                                    ('>', 4)}.ToList();
    var tsum = new List<long>();
    long sum = 0;
    var completer = "";
    var completers = new List<string>();
    foreach (var line in lines)
    {
        getFirstIncorrect(line, out completer);
        if(completer.Equals(""))
            continue;
        sum = 0;
        foreach (var c in completer)
        {
            sum *= 5;
            sum += points.Find(p => p.Item1.Equals(c)).Item2;
        }
        tsum.Add(sum);
    }
    tsum.Sort();
    return tsum[(tsum.Count-1)/2];
}
int star1(List<string> lines, List<(char, int)> points)
{
    var c = "";
    var incorrect = lines.Select(l => getFirstIncorrect(l, out c)).ToList();
    incorrect.RemoveAll(i => i.Equals(' '));
    var sum = incorrect.Select(s => points.First(p => p.Item1.Equals(s)).Item2).Sum();
    return sum;
}
char getFirstIncorrect(string line, out string completer)
{
    completer = "";
    var stack = new Stack<char>();
    foreach (var c in line)
    {
        if(isOpening(c))
        {
            stack.Push(c);
            continue;
        }
        if(!stack.Peek().Equals(getOpening(c)))
            return c;
        stack.Pop();
    }
    while(stack.Count != 0)
        completer += getClosing(stack.Pop());
    return ' ';
}
bool isOpening(char c)
{
    return "([{<".Contains(c);
}
char getOpening(char c)
{
    return pairs.Find(p => p.Item2.Equals(c)).Item1;
}
char getClosing(char c)
{
       return pairs.Find(p => p.Item1.Equals(c)).Item2;
}
main();