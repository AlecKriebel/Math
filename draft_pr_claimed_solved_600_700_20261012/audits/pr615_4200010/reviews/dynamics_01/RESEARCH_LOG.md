# Independent dynamics review log: PR #615 / problem 4200010

Scope: independently test the frozen candidate's skew shift, Koopman claims,
invariant measurable subsets, suspension, Lyapunov estimates, and source scope.
No original files, Git state, PR, queue, or publication records are modified.
No external individuals or other shard agents are contacted.

## 2026-10-13 03:06:44 UTC — checkpoint (completion estimate: 15%)

Read the frozen proof and validation code. The target is an autonomous smooth
Hamiltonian on an unrestricted compact symplectic four-manifold with a positive
Liouville-volume region outside both the almost-periodic and positive-exponent
regions. Record the exact convention: almost periodicity means precompact
orbits for every vector in the full restricted L2 Koopman representation.
The finite author's checks cannot establish the measure-theoretic assertions.
The frozen previous audit was available and read, but no live reviewer input
is used; all mathematical deductions and the new executable checks below are
re-derived independently without importing either verification program.

## 2026-10-13 03:07:35 UTC — checkpoint (completion estimate: 45%)

The torus map, frame gluing, real Hamiltonian cutoff, full tangent derivative,
and volume calculations survive direct re-derivation. Independently opened
Knill's 2000 primary HTML and problem-list PDF; the printed existential
question has no stated ambient Euclidean or mechanical restriction. Its weak
mixing sentence is explicitly a separate guess. Knill's 2016 section on
integrability explicitly associates almost periodicity with pure discrete
Koopman spectrum, corroborating the candidate's convention. This later text
does not settle historical priority or retrospectively sharpen the old wording.

New checkable strengthening to derive: the suspension observable has exact
continuous-time correlation max(1-|s|,0). This provides a spectral falsification
test extending the candidate's integer-time orthogonality argument.

## 2026-10-13 03:11:02 UTC — checkpoint (completion estimate: 80%)

New independent code passed 7,036 exact checks with Q(sqrt(2)) arithmetic and
no imports from author or prior audit programs. Reproduced all fractional-time
correlation cells and the transverse derivative. The invariant-subset
classification is valid after rational-time Fubini and strong continuity.
Re-derived maximal-good-region existence by countable disjointification and
L2 tail approximation. A compactly supported clock bump makes the orthogonal
witness smooth, avoiding any reliance on the L2 seam discontinuity. The
Bohr trajectory test gives pairwise uniform separation 2 for integer shifts.
The global energy-dependent frame derivative proves zero exponents on all M.

## 2026-10-13 03:14:38 UTC — final checkpoint (completion estimate: 100%)

Completed REVIEW.md, independent_reproduction.py, and RESULTS.json. Verdict:
the frozen theorem is mathematically sound for its explicit unrestricted
smooth symplectic and full-Koopman almost-periodicity convention. No mandatory
mathematical repair found. Strongest verified result includes global zero
exponents, a band of ambient measure 1/4 excluding every positive invariant
almost-periodic region, per-energy ergodicity and continuous spectral witness,
and failure of Bohr almost periodicity for every trajectory in the band.
Historical novelty and unstated stronger ambient categories are not certified.
Only authored review artifacts were written, all within the assigned folder.
