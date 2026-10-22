# Independent tensor/marginal adversarial review of PR170

**Verdict within this assigned family: PASS. No blocking mathematical defect
found.** The claimed negative conclusion for the real binary-tensor Gram
locus of the closed Frobenius unit ball is supported by an independently
written proof. The explicit positive four-factor obstruction and scoped
printed-source caution also pass exact independent checks. This review makes
no novelty, priority or present literature-status conclusion.

## Exact audited claim and scope

For $n\ge3$, no real polynomial in determinant coordinates alone describes
the entire locus $G_n$ by one nonnegativity condition inside either the
closed cube $C_n=[0,1/4]^n$ or the stated convex hull $H_n$. The higher
factor argument uses coordinate-zero faces of these closed domains. This
review does not extend that conclusion to a problem that removes all zero
coordinates or changes the normalization.

## Independent findings

1. **Polygon necessity: verified.** The real Schmidt decomposition,
   commuting smaller-eigenvector projections, and Bessel inequality give
   the marginal polygon inequalities without a hidden assumption on the
   remaining tensor factors. Zero Schmidt eigenvalues are handled before
   selecting a pair, and repeated eigenvalues allow arbitrary orthonormal
   eigenbases.
2. **Trace reduction: verified.** At trace $s$, normalized determinants
   divide by $s^2$. The logarithmic ratio derivative is positive when the
   numerator determinant is strictly smaller than the denominator
   determinant. A failed trace-one polygon therefore cannot become feasible
   at a smaller allowed trace. Zero numerators are identically zero; lower
   discriminant endpoints follow by continuity; $d_i=1/4$ forces $s=1$.
3. **Exact real $G_3$: verified on the closed domain.** The four
   nonnegative even-parity weights yield a real norm-one tensor with diagonal
   marginals and the intended smaller eigenvalues. Zero weights, triangle
   equalities, all-zero determinants and repeated endpoint eigenvalues cause
   no exception. Necessity and this construction prove exactness.
4. **Zero-determinant slices: verified for every number of factors.** A
   zero real Gram determinant is equivalent to a rank-at-most-one
   flattening. After normalizing the factored vector, all retained Gram
   matrices and the norm are identical. Repeated peeling and unit-vector
   extension prove equality of the closed slice, not merely inclusion.
5. **Convex hull and local neighborhoods: verified independently.** The
   marginal polygon implies the determinant polygon. A perturbation argument
   classifies all vertices of $H_n$, each realized by a real subset-GHZ
   tensor or a product tensor. The two determinant slack computations are
   strictly positive at the boundary and reflected interior patches used in
   the polynomial argument. Restricting $H_n$ to the zero face gives
   exactly $H_3$.
6. **Single-polynomial conclusion: verified.** The true boundary plane
   forces odd exact multiplicity in the pulled-back polynomial. Its
   coordinate reflection forces the same multiplicity on a plane through
   the locus interior, which requires even multiplicity. Nonzero residual
   factors on suitable open patches justify the sign arguments even when a
   defining polynomial vanishes at some interior points. Exact face
   restrictions transfer the contradiction to all $n\ge3$.
7. **Positive rational $n=4$ witness: verified.** All four coordinates
   and all hull slacks are strictly positive. The source products evaluate
   to the displayed exact values and $Q_1-Q_2>0$, while rational inverse
   eigenvalue bounds violate the necessary polygon by a strict margin. The
   trace reduction rules out every norm-at-most-one realization.
8. **Printed-source caution: verified, with additional evidence.** Visual
   inspection confirms the printed secondary sign. Unit real GHZ is
   excluded by the union as printed, with the submitted $Q_1,Q_2$ and pair
   values. An independently checked, explicitly realized open-cube tuple
   $(99/400,99/400,99/400)$ is also excluded, so the issue is not only a
   determinant endpoint. No silent correction or general conclusion about
   the paper's other results is used.

## Evidence and falsification controls

`DERIVATION.md` contains the full proofs. `controls.py` is an independent
standard-library implementation with no language `assert` statements. It
checks actual rational tensor Gram matrices, 65 closed-grid parity targets,
five-factor extensions, 219 convex-hull vertices, an interior-hull
nonmember, and exact source arithmetic. `CONTROLS_RESULT.json` records two
passing baseline executions and twenty explicit rejections: ten meaningful
false variants tested in both ordinary and optimized Python. These finite
controls supplement the proof and are not presented as a proof of a
universal assertion.

## Independence and source boundaries

Only `COUNTEREXAMPLE.md` and `source_record.json` from the original frozen
submission, plus the specified primary HSS and Seigal PDFs, supplied
scientific inputs. The author's verifier, reviews or results; ROOT and
sibling conclusions; and PR body/comments were not consulted. The initial
receipt and the first substantive reconstructed assessment were separately
frozen at mode 0444 with SHA256 seals before final conclusions. Primary
source bodies, extractions and the visual render remain private and are
excluded from the own-output public allowlist.

The primary facts about the earlier polygon theorem and real construction
were checked in [HSS version 2](https://arxiv.org/pdf/quant-ph/0209085v2).
The cube normalization, convex-hull statement and printed product/sign
displays were checked in [Seigal's published
PDF](https://seigal.github.io/seigal2018gram.pdf), particularly printed
pp.352--354. No broader literature search was made.

## Exact remaining gap

There is no remaining mathematical gap in this assigned spectral/realization
audit. Historical novelty and current status remain unassessed. The result
should retain its credit to the earlier polygon theorem and real
construction, its closed-domain scope, and its narrow description of the
printed formula issue. No external communication, Git mutation or remote
publication was performed by this family.
