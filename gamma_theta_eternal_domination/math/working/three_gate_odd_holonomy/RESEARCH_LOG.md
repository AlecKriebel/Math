# Research log: three-gate odd holonomy

## 2026-07-28 PDT

- Read the accepted C-098 through C-103 source notes and hostile reviews,
  together with the response-2SAT and connector-parity prerequisites.
- Encoded cyclic dead-boundary networks with arbitrary literal one-guard
  closure, arbitrary extra edges/vertices, optional exact two-list typing,
  and optional \(\gamma\geq3\).
- Observed an exact parity split in the tested three-, four-, and five-gate
  instances: even total connector parity was SAT, odd parity was SAT after
  deleting \(\gamma\geq3\), and odd parity was UNSAT with
  \(\gamma\geq3\).  These remain discovery observations, not a theorem.
- Added complete minimal tight-gate gadgets (original cross clause, even
  same-sign physicalization path, failed incidence, and physical cap).
  The tested parity behavior persisted.
- Extracted 23-clause unit-propagation cores for a common complement
  neighbor of the canonical critical pair.  Converted both forced list
  inclusions into the explicit symmetric one-guard attack trees in
  Theorem 2.1 of `NOTE.md`.
- Proved that, in the exact-two-list branch, every outside witness of the
  critical pair has the third type.  This is the first local transition
  needed by a possible odd-cycle descent.
- Identified the exact unresolved branch: a dynamic almost-cap can be
  physicalized at the literal level, but its two clause edges need not
  transport.  The C-098 repair operation can create further tight gates,
  and no well-founded shortening measure is yet proved.
- Froze the gamma-dropped control `KBn]r]vj]lnZ`.  A standalone verifier
  reconstructs
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3)\), the
  181-state greatest eternal triple-family, all 1,629 attack obligations,
  the exact two-lists, three dead boundaries, odd connector parity, and
  the three critical dominating pairs.
- No universal \(k=3\) theorem, counterexample, frontier increase, or
  conjecture resolution is claimed.
