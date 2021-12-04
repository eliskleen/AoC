class Board
{
    int size;
    List<number> board;
    public Board(List<int> nums, int size)
    {
        this.size = size;
        board = new Board.number[size*size].ToList();
        int row = 0, col = 0;
        foreach (var num in nums)
        {
           board[row*size + col] = new number(num); 
           col++;
           row = col == size ? row +1: row;
           col = col < size ? col : 0;
        }
    }
    public bool? markNum(int num)
    {
        return this.board.FirstOrDefault(s => s.n == num)?.setMarked(true);
    }
    public bool hasWon()
    {
       for(int i = 0; i<size; i++)
       {
           bool row = true, col = true;
           for(int j = 0; j<size; j++)
           {
               //check if a row is marked
               if(board[i*size+j].marked == false)
                    row = false;
               if(board[j*size+i].marked == false)
                    col = false; 
           }
           if(col || row)
            return true;
       }
       return false;
    }
    public List<int> getUnmarkedNums()
    {
        return this.board.Where(b => b.marked == false)
                         .Select(b => b.n)
                         .ToList();
    }

    private class number
    {
        public int n { get; private set;}
        public bool marked { get; private set;}
        public number(int _n)
        {
            this.n = _n;
            marked = false;
        }
        public bool setMarked(bool mark)
        {
            this.marked = mark;
            return this.marked;
        }
    }
}

void star1(List<Board> boards, List<int> nums)
{
    foreach (var number in nums)
    {  
        boards.ForEach(b => b.markNum(number));
        var won = boards.FirstOrDefault(b => b.hasWon());
        if(won != null)
        {
            Console.WriteLine("First:");
            Console.WriteLine(won.getUnmarkedNums().Sum() * number); 
            Console.WriteLine("------");
            break;
        }
    }
}
void star2(List<Board> boards, List<int> nums)
{
    foreach (var num in nums)
    {
        boards.ForEach(b => b.markNum(num));
        if(boards.Count == 1 && boards.First().hasWon())
        {
            Console.WriteLine("Sec:");
            Console.WriteLine(boards.First().getUnmarkedNums().Sum()*num);
            break;
        }
        boards.RemoveAll(b => b.hasWon());
    }
}

var lines = File.ReadAllLines("input.txt").ToList();
var nums = lines[0].Split(',')
                   .ToList()
                   .ConvertAll(int.Parse);

List<List<int>> numBoards = new List<List<int>>();
lines.RemoveAt(0);
var boardNum = -1;
foreach (var line in lines)
{
    if(line == "")
    {
        boardNum++;
        numBoards.Add(new List<int>());
        continue;
    }
    var split = line.Split(' ')
                   .ToList();

    split.RemoveAll(s => s == "");
                   //.ConvertAll(int.Parse);
    var ints = split.ConvertAll(int.Parse); 
    numBoards[boardNum].AddRange(ints);
}
List<Board> boards = new List<Board>();
foreach (var b in numBoards)
    boards.Add(new Board(b, 5));   
star1(boards, nums);
star2(boards, nums);



