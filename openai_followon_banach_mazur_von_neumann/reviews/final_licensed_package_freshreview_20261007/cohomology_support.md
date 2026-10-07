# Fresh cohomology and algebraic-reconstruction support review

Timestamp: 2026-10-07T15:38:44Z. Scoped review completion estimate: 100%.
This is support for the independent complete-package review, not a separate
complete-package verdict. No production file was changed, no Git action was
taken, and no external individual was contacted.

## Inputs and independence

I read `research/PROJECT_BRIEF.txt` first, then the current
`manuscript/main.tex`, then extracted and read all five actual upstream
manuscript sections from the final upload archive. I did not read prior
favorable review reports or their check scripts before reconstruction.
I also consulted the supplied Roydor primary reading text for Corollary 2.4,
Lemma 2.5, Proposition 2.13, Lemma 3.1, and the statement and opening of
Theorem 3.2; the separate Roydor support reviewer remains responsible for
the full source audit of that article.

Exact reviewed input hashes:

- `manuscript/main.tex`, 22,215 bytes, SHA-256
  `46a02c0cd03f798459a9cfd8fb1cd5e03c4e599208a2a53750d3b218b7e96dc4`.
- `publication/upload-kit/source-and-verification.zip`, 617,532 bytes, SHA-256
  `c237465073726cf0da83abfa3e0251f15a30541dac693f35885694df632c7bb0`.

Archived source inspected:
`sources/upstream/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026/build/sections/01-introduction.tex`
through `05-cohomology.tex`. These are actual theorem and proof sections,
not a favorable audit summary or ComparatorChallenges statement.
The source extraction and initial original checks were confined to
`tmp/final_licensed_package_freshreview_20261007/cohomology_support/`.
The final reviewer subsequently preserved the original check script and JSON
in the durable evidence directory; their mathematical contents are unchanged.

## Result and exact verification limit

I found no substantive mathematical gap in the scoped arguments. I
independently reconstructed the actual-image bounded cohomology assembly,
the internal random-walk/Liouville/rigidity chain, the involutive deformation
argument, and the full-carrier odd-degree reconstruction. The strongest
checked result is that the current proof gives the claimed ordinary
complex algebra-space and predual local Jordan rigidity from the attributed
family-295 vanishing theorem and the explicitly cited Roydor geometric
results, with only the two fixed source algebras `P` and `E` receiving
deformation thresholds.

The new internal source mechanisms were checked directly from their
proofs. The classical imported results (including Popa's ultrapower
freeness, Johnson–Kadison–Ringrose normal reduction, and classical
non-type-II1 vanishing) remain cited mathematical dependencies. I did not
independently rederive those full external theorems or audit their original
articles. No fresh Lean kernel build or axiom query was performed; absence
of one is neither a failure finding nor verification evidence. The original
finite computations below check algebraic identities and combinatorics;
they do not prove infinite-dimensional vanishing.

## Actual-image ordinary bounded H2 and H3

The archived introduction defines every `C_b^k(M,M)` as all bounded
complex multilinear maps with the ordinary multilinear norm. It neither
restricts to normal maps nor requires complete boundedness. Its quotient
uses the actual image of the usual Hochschild differential. Theorem 1.1
asserts an actual bounded primitive for every cocycle and every `k >= 2`.
The follow-on manuscript uses the same formula and conventions.

I checked the passage back from the separately normal tracial stage to
that precise assertion:

1. For the averaging step, the map `P` is a contraction on cochains and
   the pointwise ultraweak limit is multilinear and bounded. The common
   norm bound controls the tails in `P`, so `PF = F` really follows. The
   proof does not presume that `P` commutes with the differential.
2. The source's direct continuity proof uses a faithful finite trace,
   truncation to small two-sided supports, normality, and random signs.
   Orthogonal two-sided supports bound every signed input sum by `R`;
   Hilbert-space sign orthogonality contradicts a nonvanishing output
   2-norm. Thus the stated modulus does not need positivity, complete
   boundedness, trivial center, or separability.
3. That modulus survives unitary averaging and the ultraweak cluster
   limit by lower semicontinuity. The Liouville theorem therefore applies
   to each last-input slice despite the limit's possible failure of
   normality.
4. Averaging the original cocycle equation gives exactly
   `0 = dh + (-1)^(k+1) f`. Hence `g = (-1)^k h` is a primitive with
   norm at most the original normal cocycle norm. Both degrees 2 and 3
   are included with their correct signs.
5. For arbitrary tracial type-II1 algebras, each finite set of inputs has
   a countably generated subalgebra containing those inputs and the
   finitely many cocycle values. Adjoining matrix systems of every finite
   size excludes every finite type-I homogeneous central summand. The
   tracial representation gives separable predual. Conditional expectation
   gives a genuine cocycle on that subalgebra. Eventual exactness on each
   fixed tuple, not nested choices of subalgebras, supplies the limiting
   primitive.
6. For arbitrary centers without a faithful tracial state, the center is
   partitioned by supports of normal states. Composing the faithful
   center states with the center-valued trace gives faithful tracial
   states on the pieces. The explicit central homotopy corrects mixed
   inputs; its norm bound is uniform in the central projection. Uniform
   bounds on the resulting primitives permit the bounded central product
   even for an uncountable partition. The one complementary non-type-II1
   summand only contributes one finite primitive norm.
7. Normal reduction writes the original arbitrary bounded cocycle as a
   normal cocycle plus an actual bounded coboundary. Adding the assembled
   primitive gives an actual bounded primitive, rather than a limit only
   in the closure of the coboundaries.

This is sufficient for the follow-on open-mapping argument:
`d:C_b^2/Z^2 -> Z^3` is a bounded bijection of Banach spaces, and
`d:C_b^1 -> Z^2` is onto. Choosing constants strictly above the quotient
inverse bounds avoids assuming norm-minimizing representatives or bounded
linear selections. Degree-three vanishing supplies an actual onto map;
reduced cohomology would not suffice here.

## Internal upstream Liouville reconstruction and attacks

I read and reconstructed Sections 2–4 rather than treating their theorem
statements as certification.

- The distinguished-letter argument groups all other labels with the
  coefficient algebra. In a reduced word of path variables, the
  distinguished-letter string is reduced. Expanding every coefficient
  into its scalar and centered parts produces alternating centered
  coefficient and free-word blocks. A nonempty distinguished block
  remains in every term, so every tested trace is zero.
- Finite free requirements can be met simultaneously in a factor
  ultrapower and returned to one coordinate. The central separable case
  uses countably many measurable fiberwise dense unitary sections and
  the first successful tuple on measurable sets. This step depends on
  separable direct-integral theory only at the separable stage, before
  compactness removes separability.
- At each walk stage all tests are finite, despite their enormous
  sizes. With `p_(ell+1) = p_ell^2`, the four failure bounds are,
  respectively, of orders `ell sqrt(p_ell)`, `K_ell^-1`,
  `K_ell^-2`, and `ell exp(-p_ell^-1/2)`. Each tends to zero.
  The base dense-atom component retains positive weight. Distinct
  formal labels representing the same element do not invalidate the
  sampling argument: the chosen finite tests hold for their evaluated
  values too.
- In the Liouville argument, forward and reverse endpoint approximants
  use disjoint halves of the increment string. Their independence is
  valid; independence of `G` and `G^-1` is never asserted. Symmetry makes
  reversed inverse increments identically distributed. Concatenated
  signed blocks are independent precisely when unsigned indices are
  distinct, which is the restriction used in the proof.
- For each fixed number of blocks the endpoint-conditioning event has
  positive probability. Its mass may decay arbitrarily rapidly with
  that number. Choosing the walk time only after fixing that number
  makes the diagonal intersection argument valid without an unjustified
  uniform conditioning lower bound.
- The coordinatewise map on the tracial ultrapower is well-defined
  because the uniform ball modulus preserves the 2-norm null ideal.
  Quotient-norm representatives give the same property on the next
  ultrapower. This prevents an implicit assumption of normality of
  the harmonic limit or of its ultrapower map.
- Haagerup's length estimate controls errors in operator norm. The
  repeated-index discard concerns surviving reduced words; repetitions
  canceled away have already been collected in their coefficients.
  The coefficient bound `3^L r^(-q/2)` and the `O(r^(q-1))` repeated
  words give squared 2-norm `O(r^-1)`. Summing length bounds for the
  finitely many lengths yields operator-norm error tending to zero.
- Every ordered block `z(z* z)^d` reduces to a nonempty word with
  positive endpoint signs. Boundaries between blocks cannot cancel.
  Thus no scalar term appears, and the first-letter identities apply
  to every retained word. Adjoints have negative endpoint signs.
- The Catalan computation counts exactly the leading assignments with
  `d` distinct labels, namely `C_d (r)_d`. Lower-label assignments
  are `O(r^(d-1))`. The limiting positive element has the stated
  Marchenko–Pastur distribution on `[0,4]`, whose lack of a zero atom
  gives unitary polar part in the finite faithfully tracial algebra.
- The polar approximation respects the literal ordered products.
  Polynomial approximation is in norm at fixed regularization; removal
  of regularization uses only the established ball 2-continuity and
  contractions. It does not commute noncommuting factors.
- The final sine-polynomial argument controls `(a-b)e` on each short
  spectral arc. The trace weights every bound by `tau(e)`, so the
  number of arcs causes no growing factor. Coefficients `a,b` need
  not commute with the unitary or be free from its generators.

I did not find an unsupported transfer of the central difficulty inside
this chain. Popa's imported finite-freeness mechanism remains an explicit
classical dependency, as stated in the verification limit above.

## Involutive deformation and opposite orientation

The cochain symmetries have signs `S_1 = +reverse-star`,
`S_2 = +reverse-star`, and `S_3 = -reverse-star`.
Reversing the differential gives `d S_n = S_(n+1) d` in the positive
degrees used. Since the involutions are conjugate-linear isometries,
averaging is a real-linear norm contraction but still produces complex
multilinear cochains. Averaging a primitive of a symmetric 2-cocycle
therefore gives a complex-linear star-preserving primitive.

I independently expanded the transport calculation. For `g = id+h`,
`b = g^-1`, and `mu = m+Delta`,

`g mu(bx,by) - xy = [(Delta-dh) + h Delta - m(h·,h·)](bx,by)`.

The first-order sign is the required negative `dh`. Associativity gives
`d Delta = Delta(Delta(x,y),z) - Delta(x,Delta(y,z))`, hence quadratic
defect. With `||h|| <= 2L delta`, the inverse-square factor at most 4
gives `D = 8K + 8L + 16L^2`. The chosen initial threshold makes
`delta_n <= 2^-n delta_0`, `sum ||h_n|| <= 1/4`, and the product of
the `g_n` convergent with distance to the identity below one half.
The same fixed differential is used throughout. No moving-corner
cohomology constant enters the iteration.

For the target algebra, centrality of `q` makes
`y diamond z = q yz + (1-q) zy` the direct sum of the target product
and its opposite. It is associative, involutive, unital, and has the
original C*-norm. Pullback through the star-preserving block map `F`
gives the symmetric product required by the deformation lemma. The
resulting star-isomorphism `F Phi^-1` into `(W,diamond)` is a Jordan
star-isomorphism to the original `W`. The argument therefore respects
the geometric inability to detect opposite orientation.

## Full carriers, centers, and odd finite degrees

The source full-carrier condition has a direct quantitative proof.
Let `w=c_D(k)` and `z=theta^-1(w)`. The approximate-order estimate for
`T^-1`, together with the two norm approximation errors, gives

`h-z <= [2(1+t) r(t) + gamma(t)] 1`.

The bracket tends to zero. Compression by `1-z` turns the left side
into the projection `h(1-z)` because `z` is central. A projection
bounded above by a scalar strictly less than one is zero. Hence
`h <= z`; full carrier forces `z=1` and then `w=1`. Applying this to
the complement is valid because `T` is unital. There is no fiber or
separability assumption in this proof.

For `O`, the projection `e` has degree `n-1` and its complement degree
one in every odd finite homogeneous summand. Both have full carrier,
and `E=eOe` halves, including the direct product with unbounded finite
degrees. The compression estimates yield target projections `q` and
`1-q` with full carrier. The complementary corner is abelian by the
commutative geometric result; a full abelian projection forces `D` to
be type I. Rigidity of the single fixed `E` supplies exact
`J:E -> qDq`.

For a full projection, `Z(D) -> Z(qDq)` by compression is an onto
star-isomorphism. The exact `J` preserves centers, so it gives
`beta:Z(O) -> Z(D)`. Jordan star-isomorphisms and their inverses are
positive order isomorphisms; therefore they preserve all existing
bounded positive suprema and all central projection joins. The images
`w_n=beta(z_n)` thus partition the whole target, rather than only a
selected measurable or separable part of it.

On `w_n`, the target corner is homogeneous of degree `n-1`.
Jordan homomorphism/antihomomorphism decomposition preserves that
finite degree. Its `n-1` equivalent abelian pieces have carrier `w_n`
in `D`, since `q` is full. The projection `w_n(1-q)` is abelian and
also has carrier `w_n`. In a type-I von Neumann algebra, abelian
projections with equal central carrier are equivalent. These pieces
therefore sum to exactly `n` equivalent abelian projections filling
`w_n`, which gives homogeneous type `I_n` with center prescribed by
`beta`. Finite homogeneous classification gives the source-target
isomorphism on that summand. Bounded central products assemble them.
This proves equality of every finite odd degree without cancellation
of infinite cardinal ranks, measurable fibers, or countable-density
assumptions on the center.

## Fixed sources and mandatory boundary cases

The decomposition `M=A+P+O` has only three central pieces. `A` is
handled by the commutative geometric result. `P` halves: finite
homogeneous type-I degrees are even, all infinite cardinal type-I
pieces halve, and type-II/type-III pieces halve. `E=eOe` is the second
fixed source. Universal cohomology applies to `P` and `E` as von
Neumann algebras. Nothing is inferred merely by restricting the
cohomology of `M` to a noncentral moving corner.

Thus only at most two deformation constants are needed. All remaining
normalization, center, compression, carrier, and approximate-multiplication
errors tend to zero with initial distortion. Their finite number gives
one positive threshold depending on `M`, simultaneously for all target
algebras and all odd finite degrees. There is no universal numerical
threshold claim and no need to attain the Banach–Mazur infimum.

The argument covers zero summands by omission and the zero algebra by
the stated distance convention. A Banach predual isomorphism adjoints
to an algebra-space isomorphism with exactly the same norms. Symmetry
of Banach–Mazur distance puts its direction into the displayed
algebra inequality. Exact Jordan star-isomorphisms are normal by order
and induce canonical predual isometries. Ordinary and completely
bounded distances have not been interchanged.

## Original checkable finite artifacts

Run from the project root:

```sh
python3 reviews/final_licensed_package_freshreview_20261007/independent_checks.py
```

The durable companion `reviews/final_licensed_package_freshreview_20261007/independent_checks.json` records all assertions passing:

- Central homotopy identity on `C^2` with coefficient module `z C^2`,
  exhaustively for every cochain coefficient basis and every input
  basis tuple in degrees 1–6: 4, 16, 64, 256, 1,024, and 4,096
  comparisons. This explicitly attacks the mixed-input correction.
- Exact rational transport-defect identity on all 16 `M_2` matrix-unit
  input pairs, using a nonzero transpose perturbation for `h`.
- Exact rational associativity-defect identity on all 64 `M_2`
  matrix-unit triples, using an explicitly transported associative
  multiplication.
- Exhaustive Catalan leading-label counts for `d=1,...,4` and
  `r=1,...,5`, with leading count exactly `C_d (r)_d` in every case.
- 16,509 exhaustive three-label ordered-block configurations of
  lengths through 7: every reduction is nonempty with positive
  endpoint signs.

These artifacts were written from scratch for this review. They are
falsifiable finite supplements to the proof reconstruction, not a
claim of formal or infinite-dimensional certification.
