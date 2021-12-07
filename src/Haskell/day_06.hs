import           Data.List (group, sort)

main = do
  contents <- readFile "../../inputs/input_06.txt"
  let parsed = parse contents
  print $ solve 80 parsed
  print $ solve 256 parsed

parse :: [Char] -> [Int]
parse = map readInt . words . map commaToSpace
  where
    commaToSpace x
      | x == ',' = ' '
      | otherwise = x
    readInt = read

next :: [Int] -> [Int]
next l = (take 6 $ drop 1 $ l) ++ [l !! 7 + head l] ++ [last l] ++ [head l]

initialize :: [Int] -> [Int]
initialize = map (pred . length) . group . sort . (++ [0 .. 8])

solve :: Int -> [Int] -> Int
solve n = sum . (!! n) . iterate next . initialize
