# Exact generic-rank upper theorem for the four-port K2P maps

## Theorem

For each of the 4,379 distinct four-port `MapDescriptor`s in the corrected
K2P universe, the generic Jacobian rank is equal to the rank in its exact
nonzero-minor certificate.  The rank histogram is

| rank | descriptor count |
|---:|---:|
| 8 | 647 |
| 10 | 810 |
| 12 | 1,167 |
| 13 | 420 |
| 14 | 1,007 |
| 15 | 72 |
| 16 | 256 |

The result is algebraic over the rationals.  It therefore restricts to the
principal physical domain \(\mathcal D_+\), which is a nonempty open set and
contains every rational point used by the lower-minor and vector-field
independence certificates.

## 1. Universal polynomial vector fields

Write the edge-sector parameters as \(x_1,\ldots,x_{2E}\) and the inheritance
parameters as \(\lambda_1,\ldots,\lambda_r\), where \(r\leq2\).  For every edge
parameter choose an arbitrary multilinear polynomial \(A_i(\lambda)\).  For
every inheritance parameter choose a polynomial \(C_j\) multilinear in all
inheritance parameters except \(\lambda_j\).  Consider

\[
 V(x_i)=x_iA_i(\lambda),\qquad
 V(\lambda_j)=\lambda_j(1-\lambda_j)C_j(\lambda_{\ne j}).
\]

Every coordinate pullback is a sparse integer polynomial.  Expanding
\(J_fV\) and equating monomial coefficients gives an integer matrix \(A\) in
the unknown coefficients of the \(A_i,C_j\).  Consequently

\[
 Ac=0 \quad\Longleftrightarrow\quad J_fV_c=0
\]

as a polynomial identity, not merely at a sampled point.

Let \(E\) be exact evaluation of these vector fields at the certified rational
interior point.  Linear algebra gives

\[
 \dim E(\ker A)=\operatorname{rank}\!\begin{bmatrix}A\\E\end{bmatrix}
 -\operatorname{rank}(A).
\]

If this number is \(d\), then a \(d\)-minor of the evaluated field matrix is
nonzero.  The fields are therefore generically independent and
\(\operatorname{rank}J_f\leq p-d\).  All ranks in this argument are computed
over \(\mathbb Q\).  Together with the stored nonzero Jacobian minor of size
\(p-d\), this proves equality.

This single ansatz proves exact rank for 3,515 descriptors.

## 2. The 864 exceptional descriptors

The base ansatz leaves the following exact gaps:

| exact rank | base upper | edge classes | descriptors | port orbits |
|---:|---:|---:|---:|---:|
| 8 | 10 | 6 | 142 | 13 |
| 8 | 10 | 7 | 110 | 11 |
| 10 | 12 | 7 | 60 | 6 |
| 10 | 12 | 8 | 60 | 6 |
| 13 | 14 | 7 | 308 | 23 |
| 13 | 14 | 8 | 112 | 10 |
| 15 | 16 | 8 | 72 | 6 |

An exact implementation of the \(S_4\) port action, together with the
reticulation-variable permutation/complement action already used by the
corrected canonicalizer, partitions these descriptors into 75 orbits.

For each representative, exact evaluation identifies one or two edge-only
kernel supports outside the universal-field span.  This step only chooses a
candidate support.  The upper proof is an explicit polynomial log-field

\[
 V(x_i)=x_iW_i(x,\lambda),\qquad V(\lambda_j)=0,
\]

whose coefficient vector is obtained as the primitive cofactor/nullspace
vector of a rank-\((s-1)\) symbolic submatrix on a support of size \(s\).
Every stored field is then multiplied through all 36 rows of the full
Jacobian, using sparse integer polynomial arithmetic.  Acceptance requires
the residual to be identically zero coefficient by coefficient.  Finally,
exact rational evaluation proves that the stored fields enlarge the universal
field span to dimension \(p-r_{\rm exact}\).

The two-variable cases are binomial identities.  The high-rank cases use ten
edge variables; after removal of their common primitive factor, their stored
expanded fields remain small and independently replayable.

## 3. Port transport

Relabelling the four observed ports permutes the 36 Fourier coordinates.  It
also permutes edge classes.  Permuting reticulation variables and replacing a
variable by \(1-\lambda\) are biregular affine coordinate changes.  Thus

\[
 f' = P_{\rm out}\,f\circ P_{\rm par}
\]

with invertible Jacobians for both coordinate changes, and generic rank is
preserved.  The coverage ledger records, for each of the 864 exceptional
descriptors, a representative and a port permutation.  Exact descriptor
transformation reproduces the member descriptor byte-for-byte; no
graph-isomorphism guess is used.

## 4. Replay and falsification

The full replay independently recomputes the universal coefficient systems
for all 3,515 base descriptors, checks all 75 representative polynomial
identities, checks exact independence, and checks all 864 transports.  It
passes with zero unresolved descriptors.

Seven adversarial mutations are required to fail closed: omitted coverage,
duplicated coverage, an altered syzygy coefficient, a reassigned
representative certificate, a broken port transport, a false rank claim, and
replacement of a representative's symbolic polynomial fields by sampled-point
Jacobian evidence.  The seventh mutation is installed in a complete,
coherently resealed disposable certificate package and is rejected by the
production verifier at the exact symbolic-field-dimension gate.  All seven
are rejected; an unrelated traceback, wrong diagnostic, signal exit, or stale
success artifact cannot qualify as rejection evidence.

Before any disposable copy is made, the suite verifies `MANIFEST.sha256` and
`manifest.json` against every one of the 94 authoritative proof/code inputs
and runs the complete 4,379-descriptor production replay on that package in
place, requiring byte identity with the stored replay and explicitly checking
`descriptor_count=4379`, `zero_unresolved=true`, and `base_recomputed=true`.
The complete mutant starts with the package's canonical PASS replay; the
production verifier must remove it before reaching the exact semantic failure,
and the report binds its absence.  The mutation report is excluded from this
nested manifest because it
qualifies the manifest; the outer theorem-release lock binds both files
without a circular commitment.
