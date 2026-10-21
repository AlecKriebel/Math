# Independent DT/DKST comparator audit

Audit time: 2026-10-07 05:49:51 UTC. Narrow audit completion: 100%.
Candidate inspected: `main.tex`, SHA-256
`b487be2a3233d56facde9713681733e5e6d7a8539ff6d78a94cf7d7db796f10f`.
Also read the project instructions and `research/ORIGINAL_REQUEST.txt`.
No earlier reviews, responses, research history, or conclusions were read.
No candidate files, Git state, or external individuals were affected.

## Demeter–Thiele

Checked [arXiv:0803.1268v1](https://arxiv.org/abs/0803.1268v1), the only
listed version, submitted 2008-03-08 23:26:13 UTC; inspected
[PDF](https://arxiv.org/pdf/0803.1268v1) and
[HTML](https://arxiv.org/html/0803.1268v1).

Section 6, footnote 36, PDF p.43, explicitly describes continuous-to-lattice
transfer using functions constant on side-1 lattice squares, followed by
orbit arrays `F(n,m)=f(T^n S^m x)` for lattice-to-system transfer. Its immediate
context is Theorem 6.2, whose pointwise conclusions concern the two-parameter
averages

\[
 N^{-2}\sum_{n,m=1}^{N} f(T^nS^m x)g(T^{-n}S^m x),\qquad
 N^{-2}\sum_{n,m=1}^{N} f(T^nS^m x)g(T^m x).
\]

The surrounding setting is commuting measure-preserving transformations on
a probability space and bounded inputs. Question 6.1 concerns ordinary
one-parameter commuting Cesàro averages. The triangular singular kernel
`F(x+t,y)G(x,y+t)/t` is proposed as a further analytic goal, not proved
bounded there. Theorem 6.3 is an oscillation estimate for a different
two-dimensional model, with a `J^(1/4)` factor, not unrestricted pointwise
`r`-variation for this triangular kernel.

## Durcik–Kovač–Škreb–Thiele

Checked [arXiv:1603.00631v3](https://arxiv.org/abs/1603.00631v3), submitted
2017-08-02 19:52:18 UTC, its [PDF](https://arxiv.org/pdf/1603.00631v3), and
its [HTML](https://arxiv.org/html/1603.00631v3). Theorem 1 gives, for arbitrary
commuting measure-preserving transformations on a sigma-finite space,

\[
 M_n(f,g)=n^{-1}\sum_{i=0}^{n-1}f(S^i x)g(T^i x),\qquad
 \sum_j\|M_{n_j}-M_{n_{j-1}}\|_2^2\le C\|f\|_4^2\|g\|_4^2.
\]

This is norm variation: the partition supremum is outside the output norm.
Section 5, PDF pp.24–25, uses area-1 skew-parallelogram embeddings,
phase-uniform boundary errors, then the `L²([0,1)²)` norm in phases
`(alpha,beta)`, followed by finite forward-orbit arrays. It treats positive
averaging kernels, not symmetric `1/n` Hilbert truncations. Corollary 3
controls only short pointwise variation for smooth continuous averages.

Also checked [v1](https://arxiv.org/abs/1603.00631v1), submitted
2016-03-02 09:42:38 UTC, and its
[PDF](https://arxiv.org/pdf/1603.00631v1). The same phase integration already
appears in Section 6, equations (6.10)–(6.13), pp.21–22. Its estimate was
weaker: norm jump exponent `alpha>8`, and norm variation exponent `rho>8`.

## Candidate comparison and verdict

The candidate's exact conclusion is `L³×L³ → L^(3/2)` full pointwise
`r`-variation, every `r>2`, for symmetric Hilbert sums under arbitrary
commuting invertible transformations. Neither checked comparator has the
same action/kernel/variation scope. No duplicate of that theorem was found
in either checked paper; this statement is confined to the sources examined
and is not an exhaustive proof of novelty.

The candidate accurately attributes both stages of classical transference
to DT and positive-area phase integration to DKST. Calling Sections 2–3 an
explicit proof of this consequence is reasonable; claiming invention of
these general reduction mechanisms would not be. The candidate currently
does not make that claim. Its restriction uses different fixed central
boxes and controls the singular-kernel error in whole pointwise variation;
the cited predecessors establish the provenance of the machinery rather
than this exact formula. No substantive correction is required within this
narrow audit. The upstream full annular theorem and its public priority
remain outside this delegated scope.

Version-date caution: the regenerated arXiv HTML displays a 2026 TeX date
for DKST. Use the arXiv submission history and original PDFs for chronology.
The [publisher metadata](https://doi.org/10.1017/etds.2017.48) independently
confirms online publication on 2017-08-17 and the journal citation
*Ergodic Theory Dynam. Systems* 39 (2019), 658–688.
