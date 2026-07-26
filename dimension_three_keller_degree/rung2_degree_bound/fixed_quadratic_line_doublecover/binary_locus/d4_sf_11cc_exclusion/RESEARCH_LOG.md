# Research log — `D4-SF-11CC`

## 2026-07-26 UTC

- Chose the rational representative
  \(h=p^2-4pq+q^2,\ R=h(p+q)\) for the isolated squarefree
  \(\kappa=16\) orbit.
- The first restricted calculation suggested that \(E_5\) and \(E_4\)
  collapse the contact plane, but it had set binary lower summands to
  zero.  The result was not promoted.
- Recomputed \(E_6\) with arbitrary binary cubic parts of the first two
  components, an arbitrary binary quadratic part of the third, general
  quadratic first and second components, and a general linear part.
  The same contact plane is forced.
- Found a genuine pivot issue in the first lower solve:
  \(\Delta=m^2-4mn+n^2\).  The generic rank is seven, the two nonzero
  conic directions have rank six, and the origin has rank five.
- Recomputed both boundary charts from scratch.  The conic chart has a
  nonzero constant \(E_5\) coefficient over \(\mathbb Q(\sqrt3)\); the
  zero chart reaches the two square \(E_4\) obstructions and becomes
  binary.
- Added exact SymPy and independent PARI/GP implementations with terminal
  marker `D4_SF_11CC_FULL_STRICT_PASS`.
- Status remains candidate until a hostile agent reconstructs the
  component split and plane exit independently.
