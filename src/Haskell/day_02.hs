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


part1 :: [Command] -> Int
part1 comms = sum [commval(x) | x <- comms, f(x)]  * (sum  [commval(x) | x <- comms, u(x)] + sum  [commval(x) | x <- comms, d(x)]) 

part2 :: [Command] -> Int
part2 comms = sum [commval(x) | x <- comms, f(x)]  * (sum  [commval(x) | x <- comms, u(x)] + sum  [commval(x) | x <- comms, d(x)]) 





parseLine :: String -> Command
parseLine = x . words 
    where 
    x ["forward", num] = Forward (read num)
    x ["up", num] = Up (-1* read num)
    x ["down", num] = Down (read num)