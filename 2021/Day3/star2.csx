List<int> findRating(List<List<int>> list, int criteria)
{
    var len = list.First().Count;
    var i = 0;
    while(list.Count > 1 && i < len)
    {
        var sumBin = list.SelectMany(x => x
                              .Select((v, i) => new {Value = v, Index = (i % binary.First().Count)})).ToList()
                              .GroupBy(x => x.Index).ToList()
                              .Select(y => y.Sum(z => z.Value)).ToList();
        float thresh = ((float)list.Count/2);
        int common = (float)sumBin[i] >= thresh ? criteria : (criteria+1)%2;
        list.RemoveAll(s => s[i] != common);
        i++;
    }
    return list.First(); 
}
var lines = File.ReadAllLines("input.txt").ToList();
var wathc = new Stopwatch();
wathc.Start();
var binary = lines.Select(s => s        
                .Select(ss => int.Parse(ss.ToString()))
                .ToList())
                .ToList();
List<List<int>> oxygen = new List<List<int>>(binary);
List<List<int>> carbon = new List<List<int>>(binary);
var resOxy = findRating(oxygen, 1);
var resCarb = findRating(carbon, 0);
var epsilon = Convert.ToInt32(
                    string.Join("", 
                    resCarb.Select(s => s.ToString()))
                    ,2);
var gamma = Convert.ToInt32(
                    string.Join("", 
                    resOxy.Select(s => s.ToString()))
                    ,2);
wathc.Stop();
Console.WriteLine(wathc.ElapsedMilliseconds);
Console.WriteLine(gamma*epsilon);