void traverseLine(List<int> line, List<List<int>> board)
{
    var signx = line[2] > line[0] ? 1 : -1;
    var signy = line[3] > line[1] ? 1 : -1;
    var diffx = (line[2] - line[0])*signx;
    var diffy = (line[3] - line[1])*signy;

    var points = new List<(int, int)>();
    if(diffx == diffy)
        for(int i = 0; i <= diffx; i++)
            board[line[0]+(i*signx)][line[1]+(i*signy)]++;
    else
        traverseStraight(line, board);
}
void traverseStraight(List<int> line, List<List<int>> board)
{
    var signx = line[2] > line[0] ? 1 : -1;
    var signy = line[3] > line[1] ? 1 : -1;
    var diffx = (line[2] - line[0])*signx;
    var diffy = (line[3] - line[1])*signy;
    if(diffx == 0)
        for(int i = 0; i <= diffy; i++)
            board[line[0]][line[1]+(i*signy)]++;
    if(diffy == 0)   
        for(int i = 0; i <= diffx; i++)
            board[line[0]+(i*signx)][line[1]]++;
}
void star1(List<List<int>> lines, List<List<int>> board)
{
    lines.ForEach(l => traverseStraight(l, board));
    var overlapping = board.SelectMany(x => x)
                       .ToList()
                       .FindAll(s => s >= 2)
                       .ToList()
                       .Count;
    Console.WriteLine(overlapping);
    Console.WriteLine("----");
}
void star2(List<List<int>> lines, List<List<int>> board)
{
    lines.ForEach(l => traverseLine(l, board));
    var overlapping = board.SelectMany(x => x)
                       .ToList()
                       .FindAll(s => s >= 2)
                       .ToList()
                       .Count;
    Console.WriteLine(overlapping);
}
List<int> getNums(string str)
{
    var ret = new List<string>();
    var split = str.Split(',');
    ret.Add(split[0]);
    ret.Add(split[1].Split(' ')[0]);
    ret.Add(split[1].Split(' ').Last());
    ret.Add(split[2]);
    return ret.ConvertAll(int.Parse);
}
var fileLines = File.ReadAllLines("input1.txt").ToList();
var lines = new List<List<int>>();
foreach (var line in fileLines)
    lines.Add(getNums(line));
var max = lines.SelectMany(x => x).Max();
var board = new List<List<int>>();
for(int i = 0; i<= max; i++)
    board.Add(new int[max+1].ToList());
star1(lines, board);
board = new List<List<int>>();
for(int i = 0; i<= max; i++)
    board.Add(new int[max+1].ToList());
star2(lines, board);