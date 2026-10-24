if LoadPackage("ctbllib") = fail then Error("CTblLib missing"); fi;
for name in ["A5", "A6", "A7", "L3(2)", "U4(2)", "U3(3)", "U4(3)", "J2", "L3(4)", "2.A7", "3.A7", "6.A7"] do
 t:=CharacterTable(name);;
 if t=fail then Error("Missing ordinary table"); fi;
 Print("TABLE:",name,":",Size(t),"\n");
 for dm in Collected(List(Irr(t),c->c[1])) do Print("DEG:",name,":",dm[1],":",dm[2],"\n"); od;
od;
QUIT_GAP(0);
