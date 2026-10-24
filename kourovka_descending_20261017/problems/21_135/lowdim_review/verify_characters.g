LoadPackage("ctbllib");;
t:=CharacterTable("3.A6");;
degs:=List(Irr(t),DegreeOfCharacter);;
Print("VERSION ",GAPInfo.Version,"\n");
Print("GROUP ",Identifier(t)," ORDER ",Size(t)," DEGREES ",degs,"\n");
Assert(0,Position(degs,6)<>fail);
cs:=Filtered(Irr(t),x->DegreeOfCharacter(x)=3);;
Print("DEGREE3_COUNT ",Length(cs),"\n");
for chi in cs do
 sym:=Symmetrizations(t,[chi],2)[1];
 Print("SYM2_DEGREE ",DegreeOfCharacter(sym)," NORM ",ScalarProduct(t,sym,sym),"\n");
 Assert(0,DegreeOfCharacter(sym)=6 and ScalarProduct(t,sym,sym)=1);
od;
a:=CharacterTable("A5");;
Print("A5_DEGREES ",List(Irr(a),DegreeOfCharacter),"\n");
Assert(0,List(Irr(a),DegreeOfCharacter)=[1,3,3,4,5]);
QUIT_GAP(0);
