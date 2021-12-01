main = do  
    contents <- readFile "../../inputs/input_01.txt"
    let ints = map readInt . words $ contents 
    print $ part1 $ ints 
    print $ part2 $ ints

readInt :: String -> Int
readInt = read

part1 :: [Int] -> Int
part1 l = sum $ map fromEnum ( zipWith (\x y-> x > y) (tail l) (init l) )    
part2 :: [Int] -> Int
part2 l =  part1 $ map (\(a,b,c) -> a+b+c) $ zip3  (drop 2 l) (drop 1 l) (l)
