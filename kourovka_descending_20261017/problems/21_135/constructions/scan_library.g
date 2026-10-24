LoadPackage("ctbllib");;
names:=AllCharacterTableNames();;
out:=OutputTextFile("artifacts/library_scan.ndjson",false);;
SetPrintFormattingStatus(out,false);;
for name in names do
  tbl:=CharacterTable(name);;
  if IsOrdinaryTable(tbl) and Size(tbl)<=10^8 then
    deg:=CharacterDegrees(tbl);;
    radpos:=ClassPositionsOfSolvableRadical(tbl);;
    rad:=Sum(SizesConjugacyClasses(tbl){radpos});;
    AppendTo(out,"[\"",name,"\",",Size(tbl),",",deg,",",rad,"]\n");
  fi;
od;
CloseStream(out);;
Print("COMPLETE ",Length(names)," library names\n");
QUIT;
