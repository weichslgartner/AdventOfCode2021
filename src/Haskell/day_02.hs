{-# LANGUAGE MultiWayIf #-}

data Command = Up Int | Down Int | Forward Int deriving Show

commval :: Command -> Int
commval (Up i) = i 
commval (Down i) = i 
commval (Forward i) = i 
f (Forward _ ) = True
f _ = False
u (Up _) = True
u _ = False
d (Down _) = True
d _ = False

main = do
    contents <- readFile "../../inputs/input_02.txt"
    let comm =  map parseLine . lines $ contents
    print $ part1 $ comm
    print $ part2 (depths (forwards comm) (scanl (+) 0 (aims comm) )) $ forwards comm
 
aims :: [Command] -> [Int]
aims comm =  map (\x -> if 
                        | f(x) -> 0 
                        | otherwise -> commval x) comm

forwards :: [Command] -> [Int]
forwards comm =  map (\x -> if 
                        | f(x) -> commval x 
                        | otherwise -> 0) comm

depths :: [Int] -> [Int] -> [Int]
depths x y = zipWith (*)  x y

part1 :: [Command] -> Int
part1 comms = sum [commval(x) | x <- comms, f(x)]  * 
                (sum  [commval(x) | x <- comms, u(x)] + 
                 sum  [commval(x) | x <- comms, d(x)]) 

part2 :: [Int] -> [Int]-> Int
part2 x y = sum (x) * sum (y) 

parseLine :: String -> Command
parseLine = x . words 
    where 
    x ["forward", num] = Forward (read num)
    x ["up", num] = Up (- read num)
    x ["down", num] = Down (read num)





