# Independent audit: exceptional spherical-code partial results

Date: 2026-10-04 UTC  
Target: rank 552, problem 30001065 / OWR-2090-018  
Decision: **PASS for the scoped partial results and the proposed status `unsolved`, `5/5`.**

Neither of the two unrestricted universal-optimality conjectures is resolved by
this packet. No blocking error was found in the frozen proofs or certificates.
This is an independent AI-assisted mathematical/code audit, not human peer
review or formal proof-assistant verification. No novelty or priority conclusion
is implied.

## 1. Frozen material and reproducibility

The reviewed author manifest has SHA-256:

    66b9a66708d98e240528d2680d8faea6cb0b1ff01d6f229efb7412dbacb4e1f4

All eight entries in that manifest were verified; together with the manifest,
there are exactly nine author files. The author verifier was executed without
modification, and its complete output was byte-identical to `CHECK_RESULTS.json`.
The replay output is retained here as `author_replay.json`.

An additional verifier, `independent_verify.py`, was written without importing or
executing the author verifier. It independently reconstructs the mathematics,
using different matrix and interval-certificate algorithms. It uses Python 3
and SymPy 1.14.0 with exact integer/rational arithmetic. Its output is
`INDEPENDENT_RESULTS.json`. Its only input beyond code is the frozen public
packet. In particular, its interval subdivision paths are untrusted hints:
it checks their coverage and every claimed sign.

The author files were not edited. The audit makes no remote changes. Raw source
PDFs, complete source extractions, credentials, conversation material, and
unrelated data are not included in the audit deliverables. The accompanying
`MANIFEST.sha256` hashes the audit deliverables separately from the author packet.

## 2. Source and problem-identity gate

The original question on printed p.2539 of Schürmann's contribution in
[Oberwolfach Report 44/2008](https://ems.press/journals/owr/articles/2090) concerns
40 points in dimension 10 and 64 points in dimension 14, compared with every
same-size configuration on the same unit sphere. The surrounding definition
uses squared Euclidean distance and completely monotonic potentials on `(0,4]`.
The adjacent balanced/group-balanced question is distinct. The original passage
and surrounding contribution were read, not inferred from a title.

The full relevant construction and competitor discussion in
[BBCGKS, arXiv:math/0611451v3](https://arxiv.org/abs/math/0611451v3), §1.2 and
§4.1–4.2, was read. The parity construction, Table 12 finite-field Gram rule,
and signed one-parameter family agree with the packet. The paper explicitly
leaves the full-potential comparison against that family unproved. Its discussion
of additional competitors precludes turning that family comparison into a
classification of all configurations.

The following proof passages were also checked:

- [Cohn–Kumar](https://arxiv.org/abs/math/0607446), the sharp-design theorem,
  p.106 potential reduction, and Proposition 4.1 with its proof and equality
  conditions on pp.119–121.
- [Cohn–Woo](https://arxiv.org/abs/1103.0485), Lemmas 9–10 and Corollary 11,
  their complete proofs, and the warning that the sufficient polynomial
  strengthening need not follow from universal optimality.
- [Boyvalenkov–Dragnev–Hardin–Saff–Stoyanova](https://arxiv.org/abs/1503.07228v1),
  §4.3–4.4, including the LP-universality definition and complete proofs of
  Theorems 4.10–4.11. Prior non-LP-universality for both target codes is correctly
  credited. The present quartic-attainment argument does not depend on their
  numerical table.
- [DLMF 18.10.4](https://dlmf.nist.gov/18.10.E4), including its parameter
  restriction. With its parameter `(n-3)/2`, the probability normalization is
  exactly the coordinate distribution used by the packet.
- [Cohn–de Laat–Leijenhorst](https://arxiv.org/abs/2403.16874), Theorem 1.1 and
  the complete §4 proof of Theorem 4.1. Its universal theorem is for 288 points
  in dimension 16. It supplies no universal theorem for either present target.
- [T-avoiding codes, version 2](https://arxiv.org/abs/2501.13906v2), the model
  definitions and listed families were screened. The revision date of
  17 May 2026 is correct. These restricted comparison classes do not close the
  unrestricted problem here.

All seven locally inspected source PDFs matched the sizes and hashes recorded
in the frozen source-hash file. The original catalogue endpoint was not
independently recovered during this audit; the mathematical target is securely
identified from the original report. A fresh fetch of Cohn's harmonic-optima
page failed, so its current contents are not treated as independently verified
by this audit. Literature checks found no contradictory resolution, but this is
not an exhaustive proof of the absence of one. No publication-priority gate is
claimed.

## 3. Independent exact reconstruction

### Both configurations

The 40 vectors were independently enumerated by edge subsets and parity tests.
The 64-point Gram was independently assembled using binary polynomial
multiplication and reduction modulo `z^3+z+1`, rather than the author's
shift-and-add field implementation.

The following were checked on the complete matrices, not a sample:

- Symmetry, unit diagonal after normalization, all off-diagonal valencies,
  and no coincident points
- The quadratic identities `H40^2=24 H40` and `H64^2=32 H64`
- Exact ranks 10 and 14 by a separate rank computation
- Zero row sums, zero full third moment, and every shell-balance identity

For a symmetric matrix, the quadratic identities give only the eigenvalues
zero and a positive value. They therefore establish PSD, and the trace fixes
rank. This is a complete realization argument for C64; no approximate
factorization, guessed association scheme, or unproved transitivity is used.
The tensor/frame consequences are precisely the first three sphere moments.
The fourth Gegenbauer moments are positive, ruling out a fourth design degree.
The asserted cubic-potential optimality follows from the tensor lower bounds,
with the diagonal subtraction and unordered-pair factor treated correctly.

### All 104 tangent-frame bounds

For each of the 40 and 64 vertices separately, the independent verifier forms
the full tangent Gram matrix, finds a basis by exact row reduction, and checks
all leading principal minors of the basis Gram. Its rank is exactly `n-1`.
The nearest-shell bound matrix on that basis is formed from the full shell.

Instead of repeating the author's positive-pivot elimination, the independent
verifier computes its exact characteristic polynomial. Every coefficient of
`det(x I + M)` is nonnegative. Since `M` is real symmetric, a negative eigenvalue
would give a positive root of that polynomial, which is impossible when its
leading coefficient is one and all coefficients are nonnegative. This proves
PSD, including singular cases. The ranks are 6 for every C40 bound matrix and
7 for every C64 bound matrix. The output retains every basis and the complete
characteristic-polynomial coefficient list.

The exact one-point Hessian matrices for powers 1, 2, and 3 were additionally
computed directly for every vertex and checked against
`k*2^(k-1)` times the tangent metric. Thus the low-degree positive Hessians are
not merely inferred from a numerical spectrum.

### Rival family and interval certificates

The tensor-grid inner products, all projection norms, all cross inner products,
and all permutation-pair inner products were independently enumerated. This
recovers the eight pair multiplicities and the total of 780 unordered pairs.
The projection formula and its dimension agree with the source construction.

Power-gap polynomials were independently expanded by repeated polynomial
multiplication. The degrees zero through two agree exactly with the stated
identities. For each power 3 through 99, the saved dyadic paths were converted
into intervals. Their sorted endpoints were checked to form a disjoint,
complete cover, with no gaps or overlaps.

On each leaf, a direct affine substitution into the independently expanded
polynomial was made, followed by a fresh power-to-Bernstein conversion. This
does not use de Casteljau subdivision or the author's Bernstein-generation
routine. Every Bernstein coefficient was strictly positive. All 97 polynomials,
351 leaves, and maximum depth 9 were reproduced. A digest of each full positive
coefficient sequence is retained in the independent output; the sequences can
be regenerated from the script.

The three exact rational inequalities starting the power tail at 100 passed.
No assertion for higher powers is inferred from a finite run: the monotonicity
argument described below is essential.

## 4. Analytic and all-parameter challenges

### Potential class, singularities, and infinite sums

The nonnegative expansion in powers of `1+t` is valid for the exact class in
the question. Put `h(u)=g(u-1)`. Interior absolute monotonicity makes every
derivative nonnegative and increasing, so its limit at zero is finite and
extends to a right derivative. Taylor's inequality gives
`h^(m)(u)/m! <= h(r)/(r-u)^m` when `0<=u<r<2`.
For `u<r/2`, the Taylor remainder about zero is bounded by
`h(r)*(u/(r-u))^(m+1)`, and tends to zero. Thus the expansion equals the
function near zero. The same derivative estimates give interior analyticity,
and analytic continuation along the real interval gives equality throughout
`[0,2)`. Smaller compact intervals also give differentiated convergence.

This supplies the analytic step behind the finite/infinite-power reduction;
it is not an appeal to a finite set of test potentials. At every fixed
nondegenerate configuration, the finitely many inner products are strictly
below 1. Energies and the needed derivatives are therefore finite and the
series operations are justified. Potentials singular at zero squared distance
are permitted: no value at a collision is used. No uniform convergence as the
family parameter approaches a collision is required.

### Parameter endpoints and equality

The parameter condition is `0<a^2<=1/27`. Zero is excluded. At the allowed
endpoint the height vanishes, but distinct permutations still have distinct
projections: their squared projection distance is
`18*a^2*(4-F) > 0`. A projection cannot equal a grid point because the possible
cross inner products have absolute value at most `1/sqrt(3)`, strictly below
one. Thus the endpoint still gives a genuine 40-point configuration.

For positive parameters, the finite certificate covers the larger interval
`[0,1/5]`, so it includes the entire admissible positive interval. For powers
at least 100, the target energy is strictly less than `481*(7/6)^k`.
The rival cross pairs dominate this bound above the split `a=13/75`; the
3-cycle pairs dominate it below the split. The checked ratios `176/175` and
`4458/4375` are greater than one, so their checked degree-100 inequalities
propagate to every larger degree. Omitted energy terms are nonnegative.

For negative parameters, expansion of the two cross-pair terms gives exactly
`192 sum_(j odd) binom(k,j)(3^j-3)|a|^j`. Every summand is nonnegative for every
integer `k`, because `3^j>=3` for all positive odd `j`. This is an algebraic
all-degree argument, not a bounded sign experiment.

Consequently every power gap of degree at least three is strictly positive
at every admissible signed parameter. A nonnegative convergent combination
has zero gap only when every positive coefficient multiplies a zero gap.
This proves exactly the stated equality classification: all affine potentials
tie; a genuine quadratic ties exactly at `a^2=5/162`; every potential with a
nonzero higher-degree coefficient has a strict gap. There is no hidden
cancellation or additional equality case from an infinite series.

## 5. One-point strictness and the all-degree LP obstruction

### One-point result

Shell balance proves stationarity. The displayed great-circle Hessian has the
correct acceleration and signs. For powers at least four, the other shells
have nonpositive inner products, so discarding their contributions yields a
valid lower bound. The nearest-shell bounds give positive quartic brackets
`8/7` and `3/2`; the bracket increases with the power. Together with the
positive low-degree Hessians, every nonconstant power gives a positive
quadratic form in every nonzero tangent direction.

The nonnegative differentiated expansion then gives a positive-definite Hessian
for every nonconstant allowed potential. Smoothness and stationarity imply a
strict local minimum. The zero eigenvalues in the auxiliary nearest-shell
bound matrices do not produce zero Hessian directions: the scalar bracket
is strictly positive. This proof does not concern collective motions, which
have different Hessian blocks and include rotational zero modes, or distant
one-point relocations. The frozen packet preserves that distinction.

### All degrees in the LP argument

The independent moment computation uses the finite binomial expansion of the
Laplace integral, rather than the author's Gegenbauer recurrence. It reproduces
all degree-1 through degree-7 values. In particular, the only zeros in that
range are degrees 1, 2, and 3.

The coordinate in the integral is on the sphere in `R^(n-1)`, giving moments
with denominator factors `n+2j-3`. For every degree at least 8, taking absolute
values and using a base in `[0,1]` gives the fourth-power expectation in the
packet. The resulting uniform bounds are `19/858` and
`25307617/3458057057`, with positive margins `3/22` and
`266239598/494008151`. Hence every higher moment is strictly positive;
there is no uncontrolled high-degree range.

LP sharpness requires both contact at every inner product and complementary
slackness against the nonnegative Gegenbauer moments. All coefficients of
degree at least four must therefore vanish. A cubic minorant of `(1+t)^4`
would leave a nonnegative quartic difference having at least three distinct
interior double roots. This is impossible. Allowing an arbitrary constant
coefficient does not affect the argument.

The conclusion is exactly the absence of an attained sharp *polynomial*
two-point certificate for the quartic potential. It is not a positive
relaxation-gap theorem, an obstruction to every infinite-series or
higher-point certificate, or evidence of a counterexample to universal
optimality. Prior non-LP-universality is acknowledged appropriately.

## 6. Hermite reduction and remaining gap

The finite Hermite reduction is valid on the spherical inner-product interval.
It uses the general interpolation lemmas, rather than transferring a
projective-space optimality theorem. Even node multiplicities make the
remainder nonnegative, and the divided differences have nonnegative
coefficients in the Newton basis. The first four basis polynomials have
nonnegative ordinary monomial coefficients and degree at most three, so the
tensor argument applies.

All six remaining target energies were independently recomputed from the
pair distributions. They are the stated four inequalities for C40 and two
for C64. Their unrestricted validity remains unproved. Several basis
polynomials lie outside the original potential cone, so this is a sufficient
strengthening only. Failing one of these inequalities would not, by itself,
refute universal optimality.

## 7. Final disposition and limitations

- Accept the three principal scoped claims: full-potential dominance over
  the explicit BBCGKS rival family, one-point strict local stability for both
  codes, and the all-degree polynomial quartic LP sharp-certificate obstruction.
- Accept the cubic global cases and the sufficient, still-incomplete Hermite
  route, with their existing limitations.
- Accept `unsolved` and `5/5` as five substantive mathematical approaches.
  This does not certify five separate conversations or model invocations.
- Reject any upgrade to a solved status, unrestricted universal optimality,
  classification of all competitors, collective local stability, novelty,
  external peer review, or formal verification.

No mandatory correction to the frozen author packet is requested. Any later
change to it requires a fresh hash check and review of the affected claims.

## Reproduction

From this audit directory, with the unchanged author packet in `../public`:

```sh
python3 ../public/verify.py > /tmp/exceptional-author-replay.json
cmp ../public/CHECK_RESULTS.json /tmp/exceptional-author-replay.json
python3 independent_verify.py ../public > /tmp/exceptional-independent-replay.json
cmp INDEPENDENT_RESULTS.json /tmp/exceptional-independent-replay.json
sha256sum -c MANIFEST.sha256
(cd ../public && sha256sum -c MANIFEST.sha256)
```

The independent checker adds a SymPy dependency for its alternative exact
matrix computations. The original verifier remains standard-library-only.
