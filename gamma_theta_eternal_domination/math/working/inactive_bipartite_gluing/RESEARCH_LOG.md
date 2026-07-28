# Research log: inactive bipartite gluing

## 2026-07-28 07:05 PDT

- Fixed the exact static target after the candidate all-length inactive
  theorem: decide whether bipartiteness of \(H'[R]\), together with static
  deletion equality, pure triangles, C-108 ridge covariance, and a full
  active root, forces a three-coloring using at most two colors on \(R\).
- Implemented a standard-library streaming search over canonical nauty
  graphs and all ridge-covariant markings.

## 2026-07-28 07:18 PDT

- Found the nine-vertex static countermodel `HEhbtjK` with
  \(A=\{1,2,5,7,8\}\) and \(R=\{0,3,4,6\}\).
- Verified that \(H'[R]\cong C_4\), the full active triangle is \(158\),
  and both deletion three-colorings use all three colors on \(R\).
- Identified \(H'\cong L(K_{3,3})\), giving direct proofs of the
  common-neighbor and pure-triangle conditions.

## 2026-07-28 07:42 PDT

- Added the target \(x=9\), adjacent in the complement exactly to \(R\).
- Exact evaluation gave
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,4,4)\).
- Located the unique dominating pair \(\{5,9\}\).  This makes the equality
  boundary explicit and prevents any misuse as a conjecture
  counterexample.
- Verified that every marked target successor dominates.  The 58
  dominating triples are deleted in rounds \(36,22\); every deletion
  facet has rank two.
- Extracted the literal adaptive two-attack refutation of the full root:
  attack 9, then attack 0 after responses by 1 or 5, and attack 3 after
  the response by 8.

## 2026-07-28 08:06 PDT

- Completed the canonical discovery sweep through order ten after adding
  the global \(\gamma=3\) condition.  No extension survived among
  2,108,079 order-ten candidate graphs and the complete smaller streams.
- This is recorded only as `OBSERVED_BOUNDED_ABSENCE`; no independent
  coverage certificate was produced.
- Froze the explicit static refutation as `PROVED`, minimum-order language
  as `OBSERVED`, and the equality-specific gluing statement as `OPEN`.
