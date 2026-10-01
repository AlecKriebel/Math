# Independent analytic first pass — sealed before historical diagnostics

Sealed at 2026-10-01T18:31:28Z. Audit completion estimate: 55%.

Input: frozen PR 21 head `096aacd71a1dc6dd3a73bea3c1055877dc8c0451`, problem
30001696, `source_snapshot/PROOF.md`, SHA-256
`58809f3edaa2930f1111ba823b1ce50c8e328dd8388b2e19323600ede3d04305`.
Before this seal I read only the input proof, snapshot manifest, applicable
AGENTS.md, and the two primary sources below. I did not read the historical
review, historical diagnostic code/results, root conclusions, or sibling reports.
No new attempt at the central open problem is made here: this is an independent
verification and attempted falsification of the candidate's analytic mechanism.

## Claim and success criterion

The audited analytic claim is universal in integers `d >= 2`, `0 <= i <= d-2`:
the bounded-sign-variation subset `C_i` of the sphere is semialgebraically
homeomorphic to the standard disk neighborhood `D_E` of a linear `i`-sphere,
and hence to `S^i x D^(d-i-1)`. A successful audit requires mathematical
arguments for the whole parameter range, including all coordinate-zero strata;
finite calculations alone cannot establish this claim. The separate
semialgebraic-to-PL theorem is outside this family's assigned analytic scope.

My first-pass verdict is **analytic mechanism verified, conditional only on the
stated classical strict variation-diminishing theorem**, for the nontrivial
range. I also give a direct determinant proof of that theorem below, so the
analytic conclusion need not depend on trusting its bibliographic formulation.
No analytic counterexample or circular use of the desired product structure
was found. Historical priority, overall publication suitability, and the PL
transfer have not been decided by this pass.

## 1. Zero-sensitive geometry

For a nonzero vector, delete all zero coordinates to define `s^-`; maximize
over independent sign completions of the zero coordinates to define `s^+`.
The minimum over sign completions is `s^-`: fill leading/trailing zeros with
the nearest nonzero sign, equal-sign gaps with that sign, and opposite-sign
gaps using a single transition. This covers arbitrary zero-block lengths,
including vectors with only one nonzero coordinate.

Consequently membership in a facet with at most `i` switches is equivalent to
`s^- <= i`; lower-dimensional faces are included exactly when such a
completion exists. The excluded set is open: any excluded vector contains an
alternating subsequence of `i+2` nonzero coordinates, whose signs persist in a
small neighborhood. Thus `K_i` is closed relative to the punctured space and
`C_i` is compact. This assertion does not claim `K_i` is closed in all of
`R^d` while omitting its origin.

At a point of the sphere, signs at nonzero coordinates are locally fixed.
Every nearby vector's retained sign pattern extends to a completion of the
original zero coordinates. If all completions have at most `i` changes, that
point has a neighborhood in `C_i`. Conversely a forbidden completion can be
realized by arbitrarily small, nonzero perturbations of every zero coordinate;
renormalizing by a positive factor preserves signs and tends to the original
point. Hence `int_S(C_i) = {s^+ <= i}`. Here interior is in the full ambient
sphere, including when the point has zero coordinates. The boundary is the
difference `C_i \ int_S(C_i)`. All these sets are finite unions of strata
specified by polynomial coordinate signs and are semialgebraic.

The all-zero vector is explicitly excluded: its `s^+` would be `d-1` and
neither sphere normalization nor the strict-flow assertion is defined there.

## 2. Polynomial eigenspaces and algebraic coordinates

Write `N=d-1`. The evaluation map from polynomials of degree at most `N` to
values at `0,...,N` is an isomorphism, by the root bound (or Vandermonde
determinant). For a polynomial `p`, the formula

`Lp(x) = (N-x)p(x+1) + x p(x-1)`

is valid at all evaluation nodes, including endpoints where the out-of-range
term has zero coefficient. For the monomial `x^k`, its degree-`k+1` terms
cancel, and its degree-`k` coefficient is `N-2k`. Thus the operator is
triangular on the monomial basis, with pairwise distinct rational diagonal
entries. Solving downwards produces a unique monic rational polynomial of
each degree `k` with eigenvalue `N-2k`; no division by zero occurs because
the diagonal differences are nonzero. These `N+1` polynomials form a basis.

With `w_j=binomial(N,j)`, all `w_j>0`, including `w_0=w_N=1`. The identity
`w_j(N-j)=w_(j+1)(j+1)` makes `J=D L D^-1` symmetric with adjacent entries
`sqrt((j+1)(N-j))>0`, zero otherwise. Its eigenvectors are `D` times these
evaluations. Orthogonality follows from symmetry and distinct eigenvalues;
normalization uses square roots of positive algebraic numbers, so an
orthonormal algebraic basis exists. In particular, the first `r=i+1`
eigenvectors span exactly `D eval(P_(r-1))`, independent of monic scaling or
sign choices. This identification is needed for the separation argument.

## 3. Strict total positivity — all compounds, all times

For a `k`-subset `I=(i_1<...<i_k)`, the exterior derivative is the sum of
terms obtained by replacing one basis vector with its image under `J`.
Any surviving off-diagonal term moves an occupied index one step into an
unoccupied neighbor. An adjacent vacant target is at the same position in
the ordered tuple, so the reordering sign is positive. A replacement into
an already occupied index vanishes. There are no jumps over other indices,
since `J` is tridiagonal. This proves all off-diagonal additive-compound
entries are nonnegative, with exactly the positive neighbor-move edges.

For `1 <= k < d`, the graph is connected: repeatedly move the leftmost
occupied index that is greater than its target position left into a vacancy;
this reaches `{0,...,k-1}`. All moves have reverse moves, so any two subsets
are connected in both directions. The diagonal is actually zero here, but
the general Metzler shift argument would also work. A positive product along
a path contributes to a corresponding entry of a power of the compound.
The exponential power series therefore gives every entry strictly positive
for every `t>0`; diagonal entries also have their identity contribution.

Differentiating `wedge^k exp(tJ)` gives the same constant-coefficient ODE
as `exp(t J^[k])` and the same identity initial condition. Uniqueness gives
the compound exponential identity. Its ordered wedge entries are precisely
the minors with increasing row and column orders. Thus every proper-size
minor is strictly positive. The last compound is the determinant,
`exp(t trace J)=1`. This is strict TP, not merely TN or entrywise positivity.

## 4. Strict variation diminution — independent determinant proof

Let `A` be a strictly TP `n x n` matrix and let `x != 0` have `m=s^-(x)`.
If `m=n-1`, the desired inequality is automatic. Otherwise split the
nonzero input coordinates into its `q=m+1` successive same-sign blocks.
For each block form a column `B_b = sum_j |x_j| A_:j`, summing only over
that block. Each block is nonempty, the block supports are strictly ordered,
and all its weights are positive. Multilinearity of determinants shows every
`q x q` row minor of the `n x q` matrix `B` is a sum of positive `q x q`
minors of `A` times positive weights, hence is strictly positive. Also
`Ax = B c`, where the entries of `c` are the nonzero signs of the blocks.

Suppose some completion of `Ax` contains an alternating subsequence at
`q+1=m+2` row indices. Restrict `B` and `Ax` to those rows. The cofactor
identity gives

`sum_(l=0)^q (-1)^l det(B with row l deleted) (Ax)_l = 0`.

All the determinants are positive. The alternating completion makes all
nonzero summands have the same sign. At least one selected output value is
nonzero: if `q` rows vanished, the nonsingular `q x q` row submatrix of `B`
would force `c=0`, impossible. The displayed sum therefore cannot vanish.
This contradiction proves `s^+(Ax) <= m` for arbitrary input zeros and
arbitrary output zeros. It also proves the relevant rectangular full-rank
column-space variation lemma without appealing to an oscillation theorem.

Applied to `exp(tJ)` this sends every `C_i` into its full ambient-sphere
interior at positive time. Nonzeroness is preserved by invertibility;
normalization is by a positive scalar and changes no sign variation.

The primary published formulation was checked: Margaliot–Sontag,
Automatica 101 (2019), p. 4, Theorem 3, equation (10), uses exactly
`s^+(Ax) <= s^-(x)` for nonzero inputs and TP matrices. Their Appendix
Proposition 1 (p. 12) and Theorem 11 (pp. 12–13) provide a proof through
cofactor determinants/strict sign regularity. Schwarz, Pacific J. Math.
32 (1970), pp. 214–215, Theorem 4, equation (4.1), states the corresponding
flow inequality. Schwarz uses **STP** for all strictly positive minors and
**TP** for the modern TN notion; confusing these would invalidate trapping.
His pp. 213–214, Theorem 3 supplies the tridiagonal criterion. These primary
checks match the stronger hypotheses proved above.

## 5. Separation for every E and F vector

In the nontrivial range `1 <= r <= N`, both `E` and `F` have positive
dimension. A nonzero `E` vector is a positive diagonal scaling of
`p(0),...,p(N)` for a polynomial of degree at most `r-1`. If its completion
contained `r+1` alternating nodes `j_0<...<j_r`, the coefficient of
degree `r` in its interpolating polynomial would be

`sum_l p(j_l) / product_(h != l)(j_l-j_h)`.

This coefficient is zero by the degree bound. The denominator signs are
`(-1)^(r-l)`, while the completed numerator signs alternate. Every nonzero
summand has a common sign. The polynomial cannot vanish at all `r+1`
distinct nodes. This is a contradiction, proving `s^+ <= r-1` even when
there are many consecutive zeros or endpoint zeros. Thus `S(E)` lies in
the interior; it is not merely a subset of the closed set.

If a nonzero `z in F` had `m=s^-(z) <= r-1`, place one simple root of a
polynomial strictly between each successive pair of opposite-sign nonzero
blocks. Use no other roots. The roots can be rational, including where
there is a zero-coordinate gap. Its degree is `m`; choosing its global sign
makes `p(j)` agree with every nonzero `z_j`. No chosen root lies at such a
node. For `y_j=sqrt(w_j)p(j)`, `y in E` and every nonzero contribution to
`<y,z>` is strictly positive. This contradicts orthogonality. Hence every
nonzero `F` vector has `s^- >= r`, so `S(F)` is disjoint from `C_i`.

This argument handles sparse support and does not presume an eigenvector
has no zero entries. In particular, `r=1` uses a nonzero constant and a
same-sign vector; `r=N` uses a degree-at-most `N-1` polynomial and a
one-dimensional `F`. All dimensions are covered without numerical sampling.

## 6. Global cross-section and algebraic parameter

The orthogonal rank-one matrices `P_k` have algebraic entries. Therefore
`M_a=sum_(k=0)^N a^k P_k` is a polynomial matrix in positive real `a`;
it is invertible with eigenvalues `a^k>0`. The normalized maps satisfy
`Psi_a Psi_b=Psi_(ab)`. The relation with the linear exponential is
`a=exp(-2t)`; the scalar `exp(Nt)` cancels. In particular, positive time
means `0<a<1`, with the direction of trapping correctly reversed.

For a vector with nonzero `E,F` components and spectral coefficients `c_k`,

`R(Psi_a x)^2 = [sum_(k>=r) c_k^2 a^(2k)] / [sum_(k<r) c_k^2 a^(2k)]`.

Both sums are strictly positive. Logarithmic differentiation of `R` gives
the `a^(2k)c_k^2` weighted mean of `k` in `F` minus that in `E`. It is
between `r-(r-1)=1` and `N-0=N`. Integration relative to `a=1` proves the
stated two-sided power bounds on `Sigma`. This remains valid with arbitrary
zero spectral coefficients; no strictly positive coefficient is required.
For `N=1`, the two bounds coincide and `R(Psi_a s)=a` exactly.

More generally for any fixed `x` the same integrated bounds multiplied by
`R(x)` show that `R(Psi_a x)` increases strictly from zero to infinity.
Thus there is a unique `b>0` with ratio one. Set `s=Psi_b x`, `a=b^-1`.
The unique root varies continuously: fix two parameters bracketing a root;
continuity preserves the strict inequalities at nearby `x`, and the bracket
can be arbitrarily narrowed. This proves the full inverse's continuity,
not just orbitwise bijectivity. The map and inverse are semialgebraic
because their graphs are related by swapping factors of a semialgebraic
graph. The round section itself identifies with `S(E) x S(F)` via
`(u,v) -> (u+v)/sqrt(2)`.

## 7. Hitting graph and the core extension

Compactness and the strict `E/F` separation give a positive uniform angular
neighborhood of `S(E)` in the interior and of `S(F)` outside `C_i`.
Indeed for a sphere point with ratio `R`, the component norms are
`1/sqrt(1+R^2)` and `R/sqrt(1+R^2)`. Consequently small/large ratios give
uniform, rather than direction-dependent, proximity to those two spheres.
The power bounds on `Sigma` supply uniform small/large orbit parameters.

If an orbit's parameter `a_2` belongs to `C_i`, every `a_1<a_2` is in its
interior by applying `Psi_(a_1/a_2)` and strict trapping. Thus membership
is a nonempty initial interval. Closedness and uniform exclusion near `F`
make it `(0,beta(s)]` with finite positive endpoint. The endpoint cannot
be interior by maximality, so it is on the boundary. Every lower point is
interior and every higher point is outside. This supplies the exact boundary
graph without assuming a preexisting collar or manifold classification.

Given an endpoint, choose one lower and one higher parameter. Interior and
the open complement persist under small changes in `s`, bracketing nearby
endpoints. This proves continuity of `beta`; its graph is the inverse image
of the semialgebraic boundary under `Gamma`, so it is semialgebraic. Compact
`Sigma` now gives `0<min beta <= max beta<infinity`.

Choose an algebraic (for example rational) `epsilon` strictly between zero
and `min(1,min beta)`, so semialgebraicity can even be understood over real
algebraic constants. The two-piece linear rescaling of orbit parameter has
strictly positive slope and agrees at the cutoff. It maps `(0,beta]` onto
`(0,1]` continuously, bijectively, and semialgebraically. Parameters `a<=1`
are exactly the orbit points of `D_E` by strict ratio monotonicity.

The extension is actually the identity on the common open neighborhood
`R<epsilon^N` of the core: a parameter in `[epsilon,1]` has ratio at least
`epsilon^N`, and a parameter at least one has ratio at least one. On that
neighborhood the parameter is less than epsilon, hence is fixed. The same
holds for the inverse. This establishes continuity across every point of
`S(E)` despite possible direction-dependent limiting spectral coordinates.
The product map `(u,v)->(u+v)/sqrt(1+||v||^2)`, `||v||<=1`, has the stated
inverse, since the `E` component is never zero on `D_E`.

## Parameter and boundary ledger

* `i=0`, any `d>=2`: `E` is the positive constant-polynomial line, so its
  sphere consists of two interior points; `F` excludes every same-sign
  nonzero vector. `S^0 x D^(d-1)` has the requisite two components.
* `d=2,N=1,i=0`: both component spaces are lines; `Sigma` is four points;
  ratio equals `a` exactly. The construction applies without differentiation
  degeneracy, connected-section assumptions, or higher-dimensional spheres.
* `i=d-2`: `r=N`, `F` is a line and `S(F)=S^0`; `Sigma` has two components.
  Every proof works componentwise and uniformly on their compact union.
* `i=d-1`: this is the whole sphere, because every word has at most `d-1`
  switches. The claimed `S^(d-1) x D^0` is immediate. `F=0`; cross-section,
  hitting graph, ratio, and cutoff are neither needed nor defined here.
* `d=1,i=0`: two vertices give `S^0 x D^0`; `N=0` and no ratio argument is
  applied. Negative `i` or `i>=d` are not part of the target statement.
* Zero physical coordinates, zero spectral coordinates, zero blocks, sparse
  support, and nonzero vector requirements have been checked explicitly.

## Primary-source records

Retrieved 2026-10-01 via web browsing and downloaded only to ignored
`_scratch/`, not vendored into first-party audit artifacts.

* Margaliot–Sontag, final Automatica 101 (2019), pp. 1–14:
  https://www.sontaglab.org/FTPDIR/margaliot_sontag_totally_positive_automatica2019.pdf
  PDF 799638 bytes; SHA-256
  `ab9ea56fa37e50647dbf810acb73bb4108a0090395aff9f1e9e28f8835adb5a9`.
  Definition 1 p. 2; Theorem 3 and equation (10) p. 4; Appendix Proposition 1
  p. 12 and Theorem 11 pp. 12–13. This is the exact source linked by the proof.
* Schwarz, Pacific Journal of Mathematics 32 (1970), pp. 203–229
  (download contains journal front matter):
  https://msp.org/pjm/1970/32-1/pjm-v32-n1-p20-s.pdf
  PDF 2505044 bytes; SHA-256
  `841d59bd256621ec9417f6ab672f3019fe9e0a72437d46880acf08246bd25282`.
  Theorem 3 pp. 213–214, Theorem 4 pp. 214–215; compound sign formula
  pp. 205–209. The terminology distinction is material.

## Next falsification phase

After sealing, reproduce both original diagnostic scripts in ignored copies
under their suitable Python runtimes, record exact hashes and assertions,
and add distinct controls: reject TN-only identity as a strict trap; reject
nontridiagonal positive generators via a negative wedge entry/minor; break
compound connectivity by cutting an edge; exercise maximally sparse physical
inputs and zero-coefficient polynomial/spectral cases; independently verify
the polynomial spectrum and exact ratio bounds including `N=1`; test
direction-dependent naive core rescaling as a negative control. These tests
will diagnose implementation or hypothesis errors, not replace the universal
arguments above.
