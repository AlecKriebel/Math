LoadPackage("ctbllib");;
allnames := Reversed(AllCharacterTableNames());;
output := OutputTextFile("adversary/independent_library_scan.ndjson", false);;
SetPrintFormattingStatus(output, false);;
count := 0;;
for tableName in allnames do
  table := CharacterTable(tableName);;
  if IsOrdinaryTable(table) and Size(table) <= 10^8 then
    degrees := Collected(List(Irr(table), character -> character[1]));;
    if Sum(degrees, pair -> pair[1]^2 * pair[2]) <> Size(table) then
      Error("degree-square checksum failed");
    fi;
    positions := ClassPositionsOfSolvableRadical(table);;
    radicalOrder := Sum(positions, position -> SizesConjugacyClasses(table)[position]);;
    AppendTo(output, "[\"", tableName, "\",", Size(table), ",", degrees,
             ",", radicalOrder, "]\n");
    count := count + 1;
  fi;
od;
CloseStream(output);;
Print("INDEPENDENT_COMPLETE ", Length(allnames), " names, ", count, " retained rows\n");
QUIT;
