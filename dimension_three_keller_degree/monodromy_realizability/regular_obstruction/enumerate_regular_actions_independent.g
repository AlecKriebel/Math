# GAP 4.16.0 with TransGrp 3.6.5
#
# Run, for example, as:
#   gap -A -q enumerate_regular_actions_independent.g
#
# TransitiveGroup(n,i) is GAP's i-th representative, up to conjugacy in S_n,
# of a transitive permutation group of degree n.  Thus the identifier nTi
# records an action, not just an abstract group.

if LoadPackage("transgrp") = fail then
    Error("the GAP package TransGrp is required");
fi;

# Keep every TSV record on one physical line even when GAP names are long.
SizeScreen([4096, 4096]);

Print("# GAP ", GAPInfo.Version,
      "; TransGrp ", PackageInfo("transgrp")[1].Version, "\n");
Print("degree\tindex\tid\torder\tstabilizer_order\tregular\tgap_name",
      "\tstructure_description\n");

for n in [2..10] do
    for i in [1..NrTransitiveGroups(n)] do
        g := TransitiveGroup(n, i);
        stab := Stabilizer(g, 1);
        regular := IsRegular(g, [1..n]);

        # Two independent checks of regularity in this transitive action.
        if regular <> (Size(stab) = 1) then
            Error("IsRegular disagrees with the point-stabilizer test");
        fi;
        if regular <> (Size(g) = n) then
            Error("IsRegular disagrees with the order test");
        fi;

        Print(n, "\t", i, "\t", n, "T", i, "\t",
              Size(g), "\t", Size(stab), "\t", regular, "\t",
              Name(g), "\t", StructureDescription(g), "\n");
    od;
od;

QUIT;
