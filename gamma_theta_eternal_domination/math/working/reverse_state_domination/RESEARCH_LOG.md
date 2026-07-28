# Research log: reverse endpoint domination

- **2026-07-28 PDT.** Isolated the question whether an active edge
  \(u\triangleright x\) can have a non-dominating reverse configuration
  at a maximum independent endpoint.  Found a six-vertex contradiction:
  a missed vertex \(r\), an independent completion \(\{u,r,a\}\), and
  C-108 produce a retained state \(\{x,r,a\}\); its forced response at
  one of the two remaining endpoint vertices produces a state that misses
  the other.  The proof does not use reverse inactivity, so it establishes
  the stronger one-way theorem in `NOTE.md`.
- **2026-07-28 PDT.** Added an exhaustive local-edge sanity checker with
  separate handling of \(a=p\), \(a=q\), and a genuinely new completion
  vertex.  The checker is explicitly not a graph-universe certificate.
- **2026-07-28 PDT.** Generalized the argument from triples to every
  \(k\).  If the reverse endpoint misses \(r\), an independent completion
  \(\{u,r\}\cup A\) and C-108 retain \(\{x,r\}\cup A\).  Sequential
  attacks on \(Q-A\) then have one more target than there are guards in
  \(A-Q\).  A hostile reviewer independently checked the occupancy,
  identity, and counting argument before the candidate was revised.
