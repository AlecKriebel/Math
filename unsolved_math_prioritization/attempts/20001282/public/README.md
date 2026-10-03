# Kuperberg's fixed-combinatorial-type question

Problem 20001282 / AIM-CONVEX_GEOMETRY-0014, rank 509. Research checkpoint: 2026-10-03.

**Outcome: partial answer to the original compound question, pending independent audit. No novelty claim.**

- The general absence of local minima, except cube/octahedron types, follows from the local machinery in a 2026 Chen–Li–Xi–Xu preprint. The note spells out why the argument applies within fixed face types.
- For every centrally symmetric realization of the hexagonal-bipyramid or dual hexagonal-prism type, an exact three-parameter formula gives one critical affine orbit, a strict maximum of value 12. The formula includes the nonproduct realizations omitted by a planar-product calculation.
- Uniqueness and maximality of critical points for all other face types remain unresolved here.

For the complete normalized bipyramid chart,

\[
B_{p,q,r}=\operatorname{conv}\{\pm e_1,\pm e_2,\pm e_3,\pm(p,q,r)\},
\]

with p,q>0, |r|<p+q−1 and |p−q|+|r|<1,

\[
P(B_{p,q,r})=\frac43(p+q+1)
\left(4-\frac{(p+q-1)^2+r^2/3}{pq}\right).
\]

The only critical point is (1,1,0), with Hessian diag(−2/3,−2,−8/3) in coordinates (p+q,p−q,r). The exact range is (32/3,12]. The maximum 12 was already announced in Alexander's 2017 BIRS lecture.

## Contents

- [PROOF.md](PROOF.md): original target, source-attributed general obstruction, full chart and critical-point proof.
- [RESEARCH_LOG.md](RESEARCH_LOG.md): five substantive approaches and their exact scope.
- [SOURCE_GATE.md](SOURCE_GATE.md): primary-source recovery, literature/duplicate checks, and publication limits.
- [check_exact.py](check_exact.py), [exact_results.json](exact_results.json): standard-library rational verification of 81 interior primal/polar hulls and the Hessian.
- [FROZEN_AUTHOR_MANIFEST.json](FROZEN_AUTHOR_MANIFEST.json): hashes of the frozen author package.

Run `python3 check_exact.py`. The finite computations corroborate the displayed identities and incidences; the universal arguments are in PROOF.md.
