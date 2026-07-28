# Research log: first cross-clause attack

- **2026-07-28 PDT.** Reconstructed the C-119/C-120/C-124
  unit--clause--unit geometry with distinct omitted types \(u,v\) and
  shared collision color \(w\).  Kept family-response and static-response
  lists separate.

- **2026-07-28 PDT.** Classified the four physical parity types.  An
  intersection of the two supporting components can contain only
  singleton-\(w\) vertices, so a coincident physical pin is necessarily
  even--even.  The shared anchor \(w\) is \(G\)-complete to both free
  components.

- **2026-07-28 PDT.** Derived the retained singleton defect-ridge lemma.
  For an odd pin \(L(s)=\{v\}\), every common complement neighbor of
  \(w,s\) is reached by the unique move of the third anchor \(u\), and all
  such defects form a \(G\)-clique with literal family exchanges.

- **2026-07-28 PDT.** Proved that the two odd--odd defect ridges are
  disjoint.  A common defect would have list \(\{u,v\}\); the length-two
  path through that defect puts the singleton-\(v\) and singleton-\(u\)
  pins on the same side of one frozen-\(w\) component, contradicting the
  combined C-120/C-124 parity-coherence theorem.

- **2026-07-28 PDT.** Audited the relation to C-121.  Only the one-edge,
  one-edge odd--odd pattern is the family \(Y_3\), and C-121 additionally
  needs an induced complement path and exact static lists.  Chords,
  static list enlargement, even arms, and anchor-only ridges remain
  explicit escapes.

- **2026-07-28 PDT.** Replayed `FDzro` as the exact gamma-two literal
  one-clause control with two anchor-only defect ridges, and `FCZbg` as an
  equality control for the retained ridge-exchange mechanism.  A small
  exact-subfamily scan found no one-clause control in the few selected
  equality graphs tested; this has no coverage status and is not a claim.

