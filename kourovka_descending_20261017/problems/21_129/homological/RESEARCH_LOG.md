# Homological/analytic family research log — Kourovka 21.129

Scope: only this folder; four residual pairs F4/H4, D6/E6, D7/E7, D8/E8. No external communication, Git changes, publishing, QUEUE, or PR work. Exact overall claim is in `../PROBLEM.md`. This family explores large-scale homological/spectral invariants, not ordinary Betti numbers as presumed quasi-isometry invariants.

## 2026-10-24T20:03Z — independent start

- Inputs: reviewed four-pair reduction and free-quotient filter; all eight `Q_T=P_T/Z(P_T)` map onto F2 and have unbounded virtual first Betti number. Cohomological dimensions agree within each pair.
- Falsifiable target: find a verified quasi-isometry invariant with different values on a residual pair, or a common geometric/analytic construction proving quasi-isometry and checked noncommensurability. No such claim is assumed.
- Mechanisms kept distinct: reduced L2 cohomology; spectral decay/Novikov–Shubin exponents; compact-support/coarse cohomology; more refined quantitative homology.
- Initial discovery completion estimate: **5%** (full question remains open in this effort).

## 2026-10-24T20:05Z — first filter checkpoint

- Verified DJL Theorem A for affine arrangements, together with Davis's 2015 repair of its spectral-sequence proof. Applied to an affine decone, it gives reduced L2 cohomology of Q_T in degree rank(T)−1 only. The top value is positive for all eight irreducible types.
- Consequently, support/nonvanishing of reduced L2 cohomology does not separate any residual pair. Restoring the Z factor makes every L2 Betti number of P_T vanish.
- Sauer Theorem 1.6 in the inspected paper proves Novikov–Shubin quasi-isometry invariance for an amenable class, not for these nonamenable groups. Using it here would be a false hypothesis transfer.
- New derivation being checked: a tensor-product heat-kernel identity forces the full combinatorial Laplacian decay exponent of Q×Z to equal 1 in both degrees adjoining a positive L2 Betti degree of Q. This may eliminate a tempting spectral filter even if wider invariance were supplied.
- Discovery completion estimate: **5%**; no residual implication proved. Homological filter audit about **35%** complete.

## 2026-10-24T20:14Z — completed filter-audit checkpoint

- Proved the exact product heat-trace identity and its asymptotics in SPECTRAL_FILTER.md. In normalized full-Laplacian convention, both top degrees of P_T have exponent 1; this does not identify the preceding boundary-map invariant. Scope adversary independently returned PASS, and root separately checked the proof.
- Proved that H_c^*(EQ_T;Z), forgetting Q_T-action, is free abelian of rank ℵ0 in degree d only, with zero multiplication. Root checked the ambient-flat term and poset orientation. Original DJLO Theorem 1 and Remark 6 independently back freeness and the ambient free group-ring term.
- Flagged an unused apparent local-rank typo in the 2015 repair: the Z×F2 three-line complement prevents reading its local group-ring cohomology as finite abelian rank. The claimed filter does not rely on that sentence.
- Exact standard-library computation validated all eight Coxeter-matrix orders and characteristic polynomials, their exponent lists, decone Poincare coefficients, and c_T values: 240, 5040, 1536, 5040, 19200, 368640, 276480, 127733760 in table order. H4 uses exact Q(√5) arithmetic and a hand root-selection proof.
- Sources cached and hashed: DJL2007, DJLO2010v2/published2011, Davis2015 repair, Sauer2004v2, Brieskorn1973. Brieskorn Theorem6(ii) formula checked visually in the scan. The retrieved DJLO arXiv PDF has a 2018 title-page compilation date; this is recorded as observed metadata, not its publication priority.
- Consolidated report in FAMILY_REPORT.md. No separation or positive quasi-isometry construction obtained. Lower-degree Q_T spectral tails still require both a valid nonamenable invariance theorem and a differing estimate; no further finite numerical extension is justified on present evidence.
- Discovery completion estimate: **5%**. Bounded filter-audit deliverable: **100%**, subject to final root review. No external communication, Git operation, publishing, QUEUE/PR action, or release.
