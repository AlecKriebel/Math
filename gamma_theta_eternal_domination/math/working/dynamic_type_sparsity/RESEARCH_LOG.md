# Research log: dynamic-type sparsity

## 2026-07-28 PDT

- Audited accepted C-079, C-082, C-094, and the sealed-cap theorem in
  C-110.
- Began with the proposed conclusion that dynamic exact-two-list ports
  cannot occur in all three omitted-color types.
- Applied C-094 to one dynamic type-\(i\) port.  Its first
  physicalization edge has one dynamic and one physical endpoint in
  \(W_i\).  C-082 supplies an outside \(i\)-positive cap, and C-079 seals
  that cap against every other \(i\)-positive outside vertex.
- Found the stronger two-pair contradiction: if the sealed cap has list
  \(\{i,j\}\) and omits \(k\), the gamma witness for \(\{j,z\}\) is forced
  to be anchor \(k\), while the pair \(\{k,z\}\) has no possible common
  complement neighbor.  Thus one sealed positive cap is already
  impossible.
- Concluded the candidate universal physicality theorem: every exact
  two-list port is complement-adjacent to its omitted anchor, and
  \(L(t)=N_G(t)\cap S\) for every outside vertex.
- The direct SAT discovery formula independently returned UNSAT with one
  forced dynamic type through order 16 and with two through order 18.
  These bounded runs are recorded only as `OBSERVED`.
- Dropping to \(\gamma=2\) produced a six-vertex sharpness control
  `EFnG`.  A standalone verifier checks
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3)\), its 12-state
  family, all 36 obligations, exact two-lists of all three types, and one
  dynamic type.
- No response-2-CNF satisfiability or clique coloring is claimed.  The
  remaining no-full \(k=3\) problem is now entirely physical at the
  reference anchors but may still carry global cross-clause holonomy.
