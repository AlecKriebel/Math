a:=Group((1,2,3,4,5),(1,2,3));;
b:=Group((6,7,8,9,10),(6,7,8));;
e:=Group(Concatenation(GeneratorsOfGroup(a),GeneratorsOfGroup(b),[(1,2)(6,7)]));;
if Size(a)<>60 or Size(b)<>60 or Size(e)<>7200 then Error("Wrong group"); fi;
Print("ORDER:",Size(e),"\n");
for pair in Collected(List(Irr(CharacterTable(e)),c->c[1])) do
 Print("DEGREE:",pair[1],":",pair[2],"\n");
od;
QUIT_GAP(0);
