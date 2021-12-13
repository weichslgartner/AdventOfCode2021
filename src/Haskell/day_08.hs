import           Data.List.Split (splitOn)
import qualified Data.Map        as Map
import qualified Data.Set        as Set
import           Data.Maybe           (fromMaybe)

type EncodingMap = Map.Map String Int

main = do
  contents <- readFile "../../inputs/input_08_test2.txt"
  let input = parse contents
  print $ part_1 input
  print $ part_2 input

parse :: [Char] -> [[[String]]]
parse = map (splitOn ["|"]) . map words . lines

part_1 :: [[[String]]] -> Int
part_1 = length . filter isSimple . map length . concat . map (!! 1)

-- map (\lambda x -> encode x initMap)

part_2  lines =  encode_lines  Map.empty ( (map (!! 0)) $ lines)

-- isSimple  = flip (elem) Map.keys initMap
isSimple = flip (elem) (Map.keys initMap)

initMap = Map.fromList [(2, 1), (4, 4), (3, 7), (7, 8)]

unsafeMaybe (Just x) = x
unsafeMaybe Nothing = error "look up failes"

encode_lines:: EncodingMap -> [[String]] -> EncodingMap
encode_lines  m w = foldr encode_words   m w

encode_words :: [String] -> EncodingMap   -> EncodingMap
encode_words  w m = foldr encode_word  m w

encode_word :: String -> EncodingMap -> EncodingMap
encode_word  w m
  | length w `elem` (Map.keys initMap) =
    Map.insert w (unsafeMaybe (Map.lookup (length w) initMap)) m
  | otherwise = Map.insert w (-1) m
