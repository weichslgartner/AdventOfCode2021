main = do
  contents <- readFile "../../inputs/input_07.txt"
  let parsed = parse contents
  print $ solve id parsed
  print $ solve (\n -> n * (n + 1) `div` 2) parsed

parse :: [Char] -> [Int]
parse = map readInt . words . map commaToSpace
  where
    commaToSpace x
      | x == ',' = ' '
      | otherwise = x
    readInt = read

solve :: (Int -> Int) -> [Int] -> Int
solve f l =
  minimum [sum $ map (\x -> f $ abs (x - i)) l | i <- [minimum l .. maximum l]]
