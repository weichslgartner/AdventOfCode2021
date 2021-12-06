{-# LANGUAGE ParallelListComp #-}

import qualified Data.Map as Map

type Point = (Int, Int)

type Segment = (Point, Point)

type PointCnt = Map.Map Point Int

main = do
  contents <- readFile "../../inputs/input_05.txt"
  let segments = map (parse . words) $ lines $ map commaToSpace contents
  print $ solve $ filter isLine segments
  print $ solve $ segments
  where
    commaToSpace x
      | x == ',' = ' '
      | otherwise = x


solve segments = Map.size $ Map.filter (> 1) $ addLines Map.empty $ map (toPoints) $ segments

parse :: [String] -> Segment
parse [x0, y0, _, x1, y1] = ((read x0, read y0), (read x1, read y1))

addLines :: PointCnt -> [[Point]] -> PointCnt
addLines pcnt points = foldr insertLine pcnt points

insertLine :: [Point] -> PointCnt -> PointCnt
insertLine points pcnt = foldr insertPoint pcnt points

insertPoint :: Point -> PointCnt -> PointCnt
insertPoint point m = Map.insertWith (+) point 1 m

isHorizontal :: Segment -> Bool
isHorizontal ((x0, y0), (x1, y1)) = y0 == y1

isVertical :: Segment -> Bool
isVertical ((x0, y0), (x1, y1)) = x0 == x1

isLine :: Segment -> Bool
isLine s = isHorizontal s || isVertical s

makeRange :: Int -> Int -> [Int]
makeRange src dest
  | src == dest = [src]
  | src < dest = [src .. dest]
  | otherwise = [src,src - 1 .. dest]

toPoints :: Segment -> [Point]
toPoints ((x0, y0), (x1, y1))
  | isHorizontal ((x0, y0), (x1, y1)) = [(x, y0) | x <- makeRange x0 x1]
  | isVertical ((x0, y0), (x1, y1)) = [(x0, y) | y <- makeRange y0 y1]
  | otherwise = [(x, y) | x <- makeRange x0 x1 | y <- makeRange y0 y1]
