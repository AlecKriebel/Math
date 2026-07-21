# Independent finite group check for the elementary wreath-product lemma.

# Three blocks: {1,2,3}, {4,5,6}, {7,8,9}.
W := Group(
  (1,2), (2,3),
  (4,5), (5,6),
  (7,8), (8,9),
  (1,4)(2,5)(3,6),
  (4,7)(5,8)(6,9)
);;

if Size(W) <> 1296 then
  Error("incorrect wreath-product order");
fi;

SortCycleType := permutation ->
  Reversed(SortedList(CycleLengths(permutation, [1..9])));;

needed := [
  [9],
  [2,1,1,1,1,1,1,1],
  [2,2,2,2,1]
];;

survivors := [];;
for class in ConjugacyClassesSubgroups(W) do
  H := Representative(class);;
  types := Set(Elements(H), SortCycleType);;
  contains_all := true;;
  for required_type in needed do
    if not required_type in types then
      contains_all := false;;
    fi;
  od;
  if contains_all then
    Add(survivors, H);
  fi;
od;

if Length(survivors) <> 1 or Size(survivors[1]) <> 1296 then
  Error("a proper subgroup survived the three cycle types");
fi;

Print("PASS: among all subgroups of S3 wr S3, only the full group contains\n");
Print("      cycle types (9), (2,1^7), and (2^4,1).\n");
