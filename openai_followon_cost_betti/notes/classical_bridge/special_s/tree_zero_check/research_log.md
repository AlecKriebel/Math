# Research log: regular-tree zero eigenvalue check

- **2026-10-07 04:34 UTC — Checkpoint; local claim completion: 100%.**
  Independently derived the rooted-level estimate `M_{n+2} >= M_n` for
  `n >= 1` from the zero-adjacency equation at each intervening child.
  At the root, `M_2 >= d/(d-1) M_0`. Choosing a root at any nonzero
  coordinate forces a fixed positive square mass on infinitely many
  disjoint even spheres, contradicting square summability. The proof
  covers complex functions and `d = 2`; no external input or spectral
  results were used. Checkable proof is in `proof.md`. Exact gap: none
  for injectivity; no claim of a bounded inverse has been made.

- **2026-10-07 04:37 UTC — Checkpoint; graph/operator audit completion: 100%.**
  Adversarially checked the graph acyclicity argument, coordinate
  conventions, adjoints, inversion conjugation, and applicability inside
  an ambient group. No substantive flaw found. Verified why deleting
  isolated zero labels cannot create free cancellation. Verified the
  explicit identities `(JTJ)*=JT*J` and `(T*)*=T`, and the ambient-group
  extension by the appropriate coset decompositions. Recorded a finite
  cyclic-group counterexample to dropping the free-generation hypothesis
  in `graph_operator_audit.md`. Suggested only that the proof make its
  adjoint identities explicit to avoid an ambiguous generic inference.
