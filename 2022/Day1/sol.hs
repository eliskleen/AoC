import System.IO()
import Data.List
-- import Data.List.Split()
main :: IO()
main = do vals <- getVals "ex.txt"
        --   print (count vals [0])
          print (part1 vals)
        --   print (drop ((length (count vals [0])) - 1) (sort (count vals [0])))
        --   print (count vals [0])


-- part1 :: [String] -> Int
-- part1 v = (drop ((length (count v [0])) - 1) (sort (count v [0]))) !! 0
part1 :: [String] -> Int
part1 v = (drop (length cals -1) cals) !! 0 
    where
          len :: Int 
          len = length cals
          cals :: [Int]
          cals = sort (count v [0])

count :: [String] -> [Int] -> [Int]
count [] is = is
count (x:xs) is = count xs (newIs)
    where newIs = if x /= "" then (i+read(x):(drop 1 is)) else (0:is)
          i = head is
-- splitOn :: String -> String -> [String]
-- spli

getVals :: FilePath -> IO [String]
getVals path = do contents <- readFile path
                  return (lines contents)
