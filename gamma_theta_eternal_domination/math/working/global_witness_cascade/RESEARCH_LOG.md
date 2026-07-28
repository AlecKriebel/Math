# Research log: global witness cascade

## 2026-07-28 PDT

- Read accepted C-079, C-082, C-100, C-103, C-104, C-105 and the
  provisional paired-repair gamma-two control.
- Forced common complement neighbors at all three critical pairs of the
  shortest boundary.  All eight physical/dynamic incidence masks are SAT
  in the weak dead-boundary encoding.
- Repeated the sweep with the complete three tight-gate gadgets.  Exactly
  the all-dynamic mask is SAT; every mask containing a physical critical
  witness is UNSAT.
- Generated an ASCII DRAT proof for one physical-witness instance and
  trimmed it to 40 input clauses plus one core lemma.  The core is unit
  propagation complete and translated into the self-contained attack tree
  now given as Theorem 2.1 of `NOTE.md`.
- Proved the cyclic corollary: under \(\gamma=3\), all three critical
  witnesses are dynamic and have the three distinct forced response types.
- Applied C-082 and C-079 to the next gamma witnesses.  Each dynamic
  type-\(i\) witness forces a physical type-\(i\) mate and then a sealed
  \(i\)-positive cap \(z_i\).
- Proved the cross-color cap incompatibility, including all collisions.
  A common complement neighbor of distinct \(z_i,z_j\) cannot be outside
  (it would omit two colors despite having an exact two-list), so it is
  forced to be the third anchor.  This forces both cap lists to be
  \(\{i,j\}\); two pairs contradict each other.  If two caps collide,
  the collided cap and the third cap have no possible common complement
  neighbor at all.  Hence the complete canonical three-gate geometry is
  impossible under \(\gamma=3\) in the unit-free no-full branch.
- Built the exact 21-vertex all-dynamic control
  `TBn]r]vj]lnZ~^~n~z~^z|~nz~^j~~t~~n^~`.  A standalone verifier checks
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3)\), an 843-state
  eternal family, a 1,237-state greatest triple kernel, and all 15,174
  attack obligations.
- Time-boxed and terminated a greedy fixed-order gamma-pair-core
  minimization after it began spending most of its time on SAT
  relaxations.  No claim depends on that incomplete lane.
- Remaining target: force an incompatible cross-color interaction among
  the three sealed cap triangles, or construct a gamma-three equality
  control showing that this stronger recurrence also fails.
