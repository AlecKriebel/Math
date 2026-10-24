if LoadPackage("ctbllib") = fail then Error("CTblLib unavailable"); fi;
for name in ["A5","L3(2)","A6","3.A6"] do
  tab := CharacterTable(name);
  if tab=fail then Error("Missing ordinary character table"); fi;
  Print("ORDER:",name,":",Size(tab),"\n");
  for pair in Collected(List(Irr(tab), c -> c[1])) do
    Print("DEGREE:",name,":",pair[1],":",pair[2],"\n");
  od;
od;
QUIT_GAP(0);
