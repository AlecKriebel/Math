# Research log: adjacent-pair repair dichotomy

- **2026-07-28 PDT — checkpoint 1.**  Audited the first auxiliary
  escape in the exact C-169 order-18 boundary.  The escaping vertex
  \(14\) is not a forced QQ1-core label; it is a later completion vertex.
  Its pair with \(u\) dominates only because the fixed-anchor repair
  migrated outside \(T=\{x,p,q\}\).  Therefore a sound all-order
  statement must quantify over arbitrary adjacent pairs and their full
  common-nonneighbor sets.  Estimated completion of this focused proof
  lane: **25%**.

- **2026-07-28 PDT — checkpoint 2.**  A short static augmentation audit
  found that the fixed 18-vertex graph can satisfy
  \(\gamma=\alpha=3\) after three vertices are added, but its named
  eternal states then disappear within two deletion rounds.  Full
  equality-plus-closure discovery formulas retaining the induced
  boundary were reported UNSAT through order 26.  These runs have no
  proof logs or coverage theorem and are retained only as diagnostics;
  they support no finite or all-order claim.  Estimated completion:
  **45%**.

- **2026-07-28 PDT — checkpoint 3.**  Extracted a size-independent human
  theorem.  For every adjacent pair \(ab\), membership of the central
  states \(\{a,b,w\}\), \(w\in W_{ab}\), is uniform.  If one is retained,
  the whole fan is a retained unique-exchange clique; if none is
  retained, independent completions and one unoccupied attack force
  both active orientations of \(ab\).  The proof never infers a graph
  nonedge from a missing response and permits witness reuse.  Estimated
  completion: **80%**.

- **2026-07-28 PDT — checkpoint 4.**  Added a standalone exhaustive
  checker for all greatest families through order six and all arbitrary
  eternal triple-subfamilies through order five, plus exact sharp
  equality controls for every branch.  The strict package replay passes.
  This candidate is ready for independent hostile review.  Estimated
  completion of this focused theorem package: **100%**.
