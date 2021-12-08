import           Data.List.Split (splitOn)

main = do
  contents <- readFile "../../inputs/input_08.txt"
  let input = parse contents
  print $ part_1 input

parse :: [Char] -> [[[String]]]
parse = map (splitOn ["|"]) . map words . lines

part_1 :: [[[String]]] -> Int
part_1 = length . filter isSimple . map length . concat . map (!! 1)

isSimple x
  | x == 2 = True
  | x == 3 = True
  | x == 4 = True
  | x == 7 = True
  | otherwise = False
