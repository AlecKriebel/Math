# Actual permutation group, independent of the character-table library.
g := Group((1,2,3),(1,2,3,4,5),(6,7,8),(6,7,8,9,10),(1,2)(6,7));;
expected := [[1,2],[4,4],[5,4],[6,2],[16,2],[18,2],[20,4],[24,2],[25,2],[30,2]];;
if Size(g) <> 7200 then Error("wrong group order"); fi;
degrees := CharacterDegrees(g);;
if degrees <> expected then Error("degree list disagrees"); fi;
if Size(SolvableRadical(g)) <> 1 then Error("group is not radical-free"); fi;
if Gcd(List(degrees,pair->pair[2])) <> 2 then Error("wrong content"); fi;
f := OutputTextFile("artifacts/diagonal_outer_check.json",false);;
SetPrintFormattingStatus(f,false);;
AppendTo(f,"{\"order\":7200,\"radical_order\":1,\"content\":2,\"degrees\":",degrees,",\"method\":\"Actual permutation group computation; no CTblLib table lookup\"}\n");
CloseStream(f);;
Print("DIAGONAL_OUTER_COMPLETE\n");
QUIT;
