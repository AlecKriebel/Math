# Independent adversarial audit: family 142 algebraic mechanism

Audit timestamp: 2026-10-07T04:27:52Z (2026-10-06, America/Los_Angeles).

The assigned original target is uniform deterministic polynomial-bit-time complete
factorization and prescribed-degree irreducible construction over explicitly
represented finite fields, without randomness, GRH, or integer factorization.
This audit concerns the *upstream prime-field proof's new algebraic mechanism*;
it does not review the extension-field reduction, Shoup construction reduction,
analytic companions, priority, or a complete follow-on publication package.

## Source identification and actual scope

Read-only upstream clone: `/Users/alec/Desktop/math`, verified at commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, with an empty `git status --short`.
I read the repository and Lean READMEs, the family-142 README, and all of
`build/sections/02-finite-fields.tex` through `07-odd-split.tex` in
`preprints/Deterministic-Polynomial-Factorization-over-Prime-Fields-October-4-2026`.
No upstream files were changed. The six SHA-256 hashes, in section order, are:

```
02 a55ede868711f34fcca8c3adb788611e0c1bed4653bef1e568f67467fbe5dde2
03 25c456356962e8ccc68e22e2b7c81feb4f0dc854fba9e0f3bdcb8cfb0f762d2f
04 59a8b0d3e550838ef2cb507e2d06984bf21862d97d93f689e49488cf21e5a1d9
05 a1291e26082593224df707cc5914976c0e764378bf633b87c2e5f3fde6d62094
06 cf4edc99584ef070d2a7f24c9f217bc525c0b27a3f3aa422e9aeeb3ea4cef169
07 b77810b3c92751113f2da014d96227970a5f8b89bdb21dac34d17c69a2abb02b
```

This was a source-level proof audit and limited exact computation. I did not
reproduce a complete norm-solver execution or formally verify these sections.
The family-142 catalogue entry has no Lean link, and a targeted search of
`lean/formalization.yaml` found no family-142/prime-field-factorization entry.
This is evidence of the identified scope only, not a proof that no relevant
formal declaration exists anywhere in the repository. No Lean build was run
for this audit, and no formal-verification claim is made.

## Verdict

**No concrete counterexample or substantive algebraic proof defect was found
in the audited sections.** This is limited positive evidence, not certification
of the entire prime-field theorem or of the follow-on target.

The remaining pivotal dependency for an unconditional application is the
validated provision of the primary-group data used by the driver. These
sections assume the data at their stated interfaces. Their proofs do not
independently establish the companion zero-free results or the primary-data
construction. They must not be cited as an independent unconditional proof
of the overall prime-field theorem. The follow-on manuscript must state the
full upstream dependency chain and the actual extent of its validation.

## Falsification attempts and conclusions

### 1. Function/divisor conventions and norm signs

The point action is `Y -> zeta Y`; the function action is its inverse.
Consequently `div(sigma h) = sigma div(h)`, and at a ramification point
`b/(sigma b)` has leading value `zeta^(v_P(b))`. This agrees with the minus
sign in the stated label formula. In the norm solver the symbol `rho` is the
inverse of this function action, but its powers give the same cyclic norm.
For odd q, `Norm(Y)=F`; this sign is essential and is explicitly restricted
to odd q. I found no sign reversal in class division or separation.

### 2. The augmented modules T_t and their Frobenius filtration

The relation subgroup is exactly `([W'], lambda^t W')`. Thus multiplication
by `lambda^t` kills T_t. The injection into T_(t+1) has image equal to the
`lambda^t`-kernel: if `(d,W)` is killed, the second coordinate gives
`W=lambda W'` by injectivity on the *integral infinity lattice*. This does
not presume injectivity of the lattice's map into the Jacobian.

Ramification generators are obtained from Hilbert 90 and an invariant
divisor. At every geometric unramified orbit the invariant coefficients are
equal; at a branch point the residue coefficient may be reduced modulo q
using pullback. The relation `sum epsilon_i=0` follows from `div(Y)` and the
degree-zero infinity divisor in the source. Equal labels therefore imply
that the *pair* is zero, which is stronger than simply a zero Jacobian class.

Frobenius fixes T_1 because all branch points and infinity points are
K-rational. If A lowers the lambda-kernel filtration by f >= 1, the terms
of `(1+A)^q-1` lower it by at least `f+q-1`: intermediate binomial
coefficients are divisible by q, and `q=u lambda^(q-1)`. The last term
lowers by qf. The claimed exponent `q^r` therefore kills T_m for
`m=1+(q-1)r`. A fixed pair differs from its Frobenius image by a relation
with second coordinate zero; lattice injectivity then forces the relation
to vanish. Thus the conclusion about *every* chosen geometric division
being k-rational follows, rather than merely existence of a special chain.

The finite-field descent proof separately handles rational representatives
and rational functions. Its norm constant can be removed because the norm
on a finite constant-field extension is surjective. Hilbert 90 then gives
an invariant divisor representative. No assertion about representatives
was silently inferred only from a rational Jacobian point.

### 3. Forced separation and its inductive invariant

The lattice obstruction is `Ne in lambda^(m-1)Lambda` but not
`lambda^m Lambda`. At the first test `lambda d_1=[W_1]` is known. Only
after equal labels make `(d_t,W_t)` zero does the relation
`d_t=[W_(t+1)]` become available. This supplies the next invariant because
`lambda d_(t+1)=d_t`. The source correctly avoids assuming
`lambda d_t=[W_t]` at every level in advance. At the last level equal labels
would require the forbidden additional *integral* lattice division.

I tried the possible failure where infinity classes have a kernel in the
Jacobian: the retained second coordinate prevents that kernel from bypassing
the final obstruction. I also checked all choices of gamma: changing gamma
shifts every label by the same scalar, and the sum-generator relation makes
this harmless.

### 4. The promised norm solver

The promise first gives an abstract splitting of the cyclic algebra;
the unknown norm solution is used only to prove that existence. All actual
local models are given explicitly. At ramified places,
`V'=Y^(-w)V` has qth power `G/F^w`; its residue is a qth power by total
ramification. At an unramified place with `q` not dividing `v(G)`, a
nonsplit unramified degree-q extension would force norm valuations to be
divisible by q, so the residue of F must be a qth power. Infinity is split
because the normalized leading coefficient of F is one. I checked the
wraparound entries and negative w in both matrix models.

The coefficient trace identity works because every nonidentity standard
monomial has matrix trace zero and q is invertible. In the unramified
scaled order it proves maximality by integral trace pairings. The completed
orders descend because their finite bounded congruences can be approximated
over the ordinary local ring; an ordinary larger order would complete to
a larger completed order. For the existence argument an ordinary maximal
order is `End` of a lattice, and these finitely differing lattices glue.

The projective-line splitting proof given in the source works over the
original field. In particular saturation of a maximal-degree line map has
no zeros, and twisting by `-d-1` forces quotient degrees <= d and vanishing
extension groups. This is enough to show the infinity evaluation image is
a conjugated full parabolic matrix algebra; the algorithm does not need
to find the bundle splitting.

For that parabolic algebra, the matrix trace pairing kernel is precisely
the strictly upper block part, even in characteristics dividing a block
size. Its common column kernel is the first block. Any rank-one matrix
`v w` with v there belongs to the algebra; normalizing `w v=1` makes it
idempotent. Lifting it to a global section gives constant characteristic
polynomial `T^(q-1)(T-1)`. Hence the qth power kills the nilpotent part
and is the desired rank-one projection. The last linear solve `Ve=he`
has rank q because nonzero elements of the field L act injectively.

The uniform ansatz has `q^2(M(d_H+1)+1)` scalar unknowns, with
`d_H <= N+2D`, `M=10q^2(N+D+1)`. Finite conditions and infinity conditions
are bounded by `O(q^2 M(d_H+1))` scalar equations. The modulus used in a
local group has k-dimension <= `(3M+3)d_H`. The characteristic condition
ensures that the root routine's scalar grids are valid and that derivative
square-free decomposition has no inseparable remainder. Denominator growth
for b^s is bounded by `H^(Ms) B^(s-1)` and linear degree growth per
multiplication; solving the final cleared system uses minors of polynomial
degree. These are genuine fixed polynomial bounds in q,N,D and log|k|,
not a bound that treats q as constant.

### 5. Divisors and functions without support factorization

The affine coordinate ring is Dedekind because the square-free curve is
smooth, and is free over k[X] with the given Y-basis. Fractional ideals
between `HO` and `H^(-1)O` are represented in a space of dimension
`2q deg H`. Products, sums/intersections and inversion have finite linear
conditions. Inversion is well-defined modulo HO because `HI` is integral.
Compression uses multiplication-by-X characteristic polynomials on residue
quotients; their multiplicities give the correct pushforward, including
residue extension degrees and ramification.

The Riemann--Roch ansatz bound follows because a nonzero degree-<q leading
polynomial cannot vanish at every qth root of unity at infinity. Reduction
by a function in `L(D+g infinity_0)` yields absolute degree <= 2g. The
local precision bound follows from a global pole/zero-degree bound for each
nonzero numerator and denominator.

The simultaneous divisor-product operation uses an algebra norm and a grid
of `s(b-1)+1` scalars. At any fixed finite closed point, the bad candidates
for each ideal have degree <= b-1; some grid member attains all minimal
valuations. The attaining candidate may depend on the point, which is
sufficient for equality of the generated ideal. It is unnecessary to find
one candidate attaining all minima at every point simultaneously.

Large infinity coefficients are not materialized in Riemann--Roch. Binary
addition/doubling keeps each divisor reduced and records a multiplication/
inversion circuit. Leaf valuations and leading coefficients propagate
through the circuit; the final valuation at a branch point is zero. The
integer valuations may be exponentially large, but their bit lengths grow
polynomially with the circuit. This avoids the false substitution of
polynomial-in-absolute-coefficient cost for polynomial-in-binary-size cost.

### 6. Odd splitting and simultaneous execution

The binomial defining the working field is irreducible: every root has
exact q-primary order `q^(s_K+r)`, and lifting the exponent makes the
minimal extension degree `q^r`. The extension degree is <= N(q-1), and
`m <= q^r <= N`. The reduced divisors have absolute degree <= 2g; the
norm solver receives numerator/denominator degree <= 2g. The scalar-grid
size for the simultaneous sum is bounded by `N(4qg)`, which is polynomial
in N,q and below the declared large-characteristic cutoff.

The field cardinality is the same in every surviving root component.
Rational-function and polynomial operations branch only through scalar
coefficient zero tests. Divergent degrees, ranks, valuations or pivot choices
therefore supply a root subset rather than invalidly inverting a zero
divisor. Inner partitions in UnitRoot are handled by gcd/Chinese remainder
operations and remain compatible with the outer dynamic evaluation.
An outer split is a subset of roots originally in F_p, so its monic gcd
is indeed defined over F_p even when calculated over the working field.

## Independently reproducible finite checks

`geometric_checks.py` uses only the Python standard library and fixed
deterministic test cases. Running it produced `geometric_checks_results.json`:

- 381 parabolic fiber-idempotent tests: every ordered block composition of
  ranks 1 through 7, three finite characteristics (2,3,5), and a nontrivial
  invertible conjugation. It recomputes the trace kernel, common column
  kernel, rank-one idempotent, and its membership in the algebra by linear
  algebra. Cases where p divides the rank or a block size are included.
- 324 local matrix tests for q=3,5,7, including w=-4 through 4 and nontrivial
  wraparound constants: the commutation relation and exact qth powers hold.
- 48 exact rational-integer infinity-lattice tests for q=3,5,7,11 and r=1
  through 4: the required m-1 divisions are integral, and the next one is
  not integral.

All passed. These do not validate symbolic arbitrary-input local precision,
the complete norm-solver code, or the analytic dependencies. They are bounded
falsification attempts for the delicate mechanisms, accompanying the proof
audit above.

Checkpoint completion estimates for this assigned audit: mathematical audit
100%; complete publication-package review 0% (outside this assignment).
These estimates are not claims that the global research target is resolved.
