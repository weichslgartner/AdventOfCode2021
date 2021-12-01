main = do  
    contents <- readFile "../../inputs/input_01.txt"
    print $ part1  $ map readInt . words $ contents 

readInt :: String -> Int
readInt = read

part1 :: [Int] -> Int
part1 l = sum $ map fromEnum ( zipWith (\x y-> x > y) (tail l) (init l) )    
