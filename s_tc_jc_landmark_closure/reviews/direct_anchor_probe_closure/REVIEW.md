# Review verdict: direct-anchor probe closure

Terminal verdict: **VERIFIED**.

The 62 direct anchors are not exact members of the existing 144 path-bound
terminal families because their selected-port counts differ.  The missing
families were therefore compiled directly, without enumerating arbitrary
networks.

The compilation is complete for the stated scope:

- all 62 anchors have unique canonical maps: 34 labelled isomorphisms and 28
  ordinary triangle redirections;
- all 2,642 theorem-forced `A+p` relations are classified;
- all 18,224 theorem-forced `A+p+q` relations above the 314 surviving
  one-port parents are classified;
- every non-isomorphic/non-`T` relation has an exact graph-derived JC
  separator;
- every strict separator is nonzero on the complete target open cube by an
  independently replayed factor/Bernstein certificate;
- every surviving child transport restricts to its unique parent transport;
- all twelve adversarial mutations are rejected; and
- the package depends only on tracked inputs and verifies without any
  untracked `primary/certificates/probe_extension_*` file.

No exact obstruction, non-`T` overlap, or one-sided generic containment was
found in this bounded direct-anchor extension universe.

This verdict removes the direct-anchor promotion gap identified in
`reviews/final_outcome_p_referee/REPORT.md`.  It does not address that
referee's separate objection concerning independent generation of the full
upstream n3 directed-relation universe.
