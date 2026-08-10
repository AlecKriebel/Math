# Final hard-cover clean-room review

Status: **UNRESOLVED globally; VERIFIED for the complete schema-3 n=4
theta-2 equal-signature and p/q probe streams**

This remains a fail-closed review of the full local-containment theorem.  It
now contains one large, independently closed subgate:

- the corrected schema-3 n=4 theta-2 base stream has 132 fixed roots, 2,106
  path-bound states, 1,860 exact polynomial separations, 114 refinement
  states, and 132 labelled-isomorphism terminals;
- the path audit regenerates every child set for every raw provenance and
  finds no merge across fixed root cases or exact rooted graph IDs;
- the terminal audit independently reconstructs every graph, displayed
  switching, descendant mask, and exact pullback;
- the p/q probe extension has 23,400 graphs, 168,582 states and 168,582 path
  bindings;
- all 12,906 p children from 132 base paths and all 155,676 q children from
  exactly 1,302 allowed p paths are present;
- the probe terminal atlas contains 153,072 exact identity separations and
  15,510 labelled isomorphisms, with no T or unresolved terminal;
- no strict-sign assertion is needed: every separated probe relation has an
  independently regenerated polynomial that vanishes identically on the
  target and is nonzero on the source;
- actual-stream mutation suites reject missing or duplicate relations,
  altered port matching, reversed direction, inconsistent path binding,
  altered exact graph identity, a wrong polynomial, and a valid polynomial
  assigned to the wrong relation.

The main certificates are:

- `certificates/schema3_n4_theta2_full_audit.json`;
- `certificates/schema3_n4_theta2_terminal_records.jsonl.gz`;
- `certificates/schema3_n4_theta2_probe_structure_audit.json`;
- `certificates/schema3_n4_theta2_probe_algebra_audit.json`;
- `certificates/schema3_n4_theta2_probe_algebra_records.jsonl.gz`;
- `certificates/schema3_n4_theta2_probe_mutation_certificate.json`.

The superseded schema-2 n=4 stream remains **FALSE**.  Its exact audit finds
1,518 states lacking the fixed-root field, 276 merges across fixed roots and
target rooted graph IDs, 2,106 coverage/root mismatches, and 72 independently
regenerated child-set mismatches.  See
`certificates/quarantined_n4_theta2_schema_failure.json`.

The historical n=3 40,072-state stream also remains **FALSE** as a fixed-path
certificate.  It has 1,287 merged refined states with differing emitted child
sets and 2,118 raw paths with no emitted children.  See
`certificates/primary_path_binding_audit.json`.

The overall theorem is not yet verified because:

1. no merged corrected schema-3 n=3 stream is currently available for the
   same terminal and p/q replay;
2. the 776 n=4 and 110 n=3 unequal-but-necessary directed signature pairs
   are not included in the equal-signature theta-2 stream audited here;
3. this review verifies the supplied 132 n=4 theta-2 fixed roots but does not
   independently prove that those roots exhaust the complete primitive
   directed relation universe; and
4. all 132 accepted theta-2 base terminals are triangle-free, so this probe
   package does not certify coherence for inserting probes on a redirected
   triangle edge; and
5. cycle and cross-core directions still require their own completed
   graph-to-algebra streams.

Accordingly, this review promotes neither the global positive theorem nor a
strong-class counterexample.  It verifies a load-bearing n=4 theta-2 subgate
and keeps the landmark closure **UNRESOLVED**.
