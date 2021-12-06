{-# LANGUAGE ParallelListComp #-}

import qualified Data.Map as Map

type Point = (Int, Int)

type Segment = (Point, Point)

type PointCnt = Map.Map Point Int

main = do
  contents <- readFile "../../inputs/input_05_test.txt"
  let b = map (parse . words) $ lines $ map commaToSpace contents
  print $
    Map.size $
    Map.filter (> 1) $ addLines Map.empty $ map (toPoints) $ filter (isLine) b
  print $ Map.size $ Map.filter (> 1) $ addLines Map.empty $ map (toPoints) $ b
  where
    commaToSpace x
      | x == ',' = ' '
      | otherwise = x

parse :: [String] -> Segment
parse [x0, y0, _, x1, y1] = ((read x0, read y0), (read x1, read y1))

addLines :: PointCnt -> [[Point]] -> PointCnt
addLines = foldr insertLine
  where
    insertPoint p d = Map.insertWith (+) p 1 d
    insertLine l d = foldr insertPoint d l

isHorizontal :: Segment -> Bool
isHorizontal ((x0, y0), (x1, y1)) = y0 == y1

isVertical :: Segment -> Bool
isVertical ((x0, y0), (x1, y1)) = x0 == x1

isLine :: Segment -> Bool
isLine s = isHorizontal s || isVertical s

toPoints :: Segment -> [Point]
toPoints ((x0, y0), (x1, y1))
  | isHorizontal ((x0, y0), (x1, y1)) =
    [(x, y0) | x <- [min x0 x1 .. max x0 x1]]
  | isVertical ((x0, y0), (x1, y1)) = [(x0, y) | y <- [min y0 y1 .. max y0 y1]]
  | otherwise =
    [(x, y) | x <- [min x0 x1 .. max x0 x1] | y <- [min y0 y1 .. max y0 y1]]
