# Independent audit of repeated running-LCM phase tails

## Publication edition

These AI-assisted authored documents and their independent internal AI audit are unrefereed. Acceptance is limited to the stated partial analytic result. No external human peer review, journal acceptance, formal proof-assistant certification, exhaustive priority search, or novelty certification is claimed.

This prose-only edition preserves the complete mathematical arguments. References below to programs, finite-check results, and original packet integrity describe the historical verification record of 10 October 2026. Programs, detailed outputs and original executable packets are not distributed here; this edition is not an executable reproduction package. The source comparison is to the retained hash-pinned manuscript, not a verified latest online revision. Edition preparation added no scholarly-source retrieval or inspection.

## Decision and exact scope

**ACCEPT as a partial analytic theorem, with no required mathematical correction.**

The audited candidate is the original `PHASE_TAILS.md`, SHA-256
`de5404972fdadbe2bdb0c0f61cf4baab12c04cfa1e3345c3755d000a07c3ddfb`.
Its frozen packet manifest has SHA-256
`0b7ad35f73f6f9b0030d7b01d17a952bc3ca26662306c757957c502cfbdadebe`.
All eleven member hashes and byte counts match. This audit has not changed that packet.

The accepted statements concern a fixed finite set of **distinct primes with at least
two elements**, its actual repeated running-LCM series, and the normalization in
candidate equation (1). They are:

1. The phase-dependent asymptotic in Theorem 1, with error little-o of
   `a^(|P|-1)` along the full integer sequence, including near phase faces.
2. The presence of a nondegenerate interval of positive subsequential limits on
   every fixed arithmetic progression in Theorem 3.
3. The explicit three-prime oscillation and polynomial/quasipolynomial obstructions
   in Corollaries 4-6, including arbitrary index-by-index choices from a fixed
   finite polynomial family.
4. The certified finite-check values, with an independently established strict
   lower bound of `0.0127214469683` for the oscillation constant.

This is an independent ordinary-proof audit and independently authored finite
verification, not a proof-assistant certification, referee acceptance, or exhaustive
priority determination. It establishes neither irrationality nor a counterexample
for the residual repeated-summand problem. No novelty claim is certified.

## 1. Original quantity, cardinality, and multiplicities

Write `P = {p,q_1,...,q_s}`, where `p` is the smallest prime and `s >= 1`.
Let `S_P` contain every positive P-smooth integer, including 1. Set

\[
 H(t)=\prod_{r\in P}r^{\lfloor\log_r t\rfloor},\quad
 P_a=H(p^a),\quad
 X_a=\frac{P_a}{p}\sum_{n\in S_P,\ n\ge p^a}\frac1{H(n)}.
\]

Every member of the prefix through a cutoff divides `H(t)`. Conversely, the
prefix contains the largest allowed power of each prime. Thus its literal running
LCM is exactly `H(t)`. There is one summand for every smooth integer, irrespective
of whether the LCM changes at that integer. Since
`H(n) > n^(s+1)/product(P)`, comparison with the product of `s+1` geometric series
proves convergence without a density theorem.

The left endpoint of each shell is included. For `a >= 1`, the LCM immediately
before `p^a` is `P_a/p`: no power of another prime equals `p^a`, and the p-exponent
is then `a-1`. This justifies the strict-prefix normalization and its denominator
clearing. At `a=0`, `P_0/p=1/p`; integrality is not asserted there.

**The singleton exception is necessary.** If `P={p}`, then the smooth integers
are exactly `p^k`, the whole series equals `p/(p-1)`, and every normalized tail is

\[
 X_a=p^{a-1}\sum_{k\ge a}p^{-k}=\frac1{p-1}.
\]

It has no nondegenerate interval of limits and admits an exact constant polynomial
correction. The candidate excludes this case consistently. The empty prime set is
also outside its notation and statements. The proof for two primes is valid as a
tail theorem; it does not independently audit the cited two-prime transcendence
result.

## 2. Independent reconstruction of the shell formula

Put `lambda_j=log_p(q_j)>1`, `theta_j=1/lambda_j`, and
`x_a=({a theta_1},...,{a theta_s})`. For a p-free exponent vector `k >= 0`, let
`w=k dot lambda`. A nonnegative p-exponent places the corresponding number in
`[p^a,p^(a+1))` if and only if `w<a+1`; that exponent is uniquely
`a-floor(w)`. Its logarithm is `a+{w}`. In particular the zero vector contributes
the left endpoint `p^a`.

Writing `s_a` for the literal shell mass and `M_a=P_a s_a`, substitution yields

\[
 M_a=\sum_{k\ge0,\ k\cdot\lambda<a+1}
       \prod_{j=1}^s q_j^{-\lfloor(x_a)_j+\theta_j\{k\cdot\lambda\}\rfloor}.
\]

This is candidate equation (8), with neither omitted repetitions nor an extra p
factor. For three primes, Cook's integer shell numerator is a different
normalization: `m_a=(P_(a+1)/p)s_a`, so `m_a=(P_(a+1)/P_a) M_a/p`.
The candidate's use of both `M_a` and the numerical `m_a` is consistent with this.

As a literal check, for `P={2,3,5}` the seven integers in `[16,32)` have denominators

\[
 720,720,720,720,3600,10800,10800.
\]

Multiplication by `P_5/2=10800` gives `m_4=65`. Counting each denominator only
once gives 19; omitting the normalization factor 1/2 gives 130. Both are rejected
by the independent checker. The example is already in the prior manuscript and
is a normalization test, not a new result.

## 3. Uniform counting and the moving-phase asymptotic

### 3.1 Uniform interval discrepancy

For fixed positive `lambda_j` with `lambda_1` irrational, let
`T_T={k>=0:k dot lambda<T}`. Unit cubes anchored at its integer points cover the
nonnegative simplex of parameter T and lie in the simplex of parameter
`T+sum(lambda_j)`, apart from null boundaries. Thus

\[
 \#T_T=\frac{T^s}{s!\prod_j\lambda_j}+O(T^{s-1}).
\]

The geometric sum at every nonzero Fourier frequency of the rotation by
`lambda_1` is bounded independently of the initial phase. Continuous periodic
approximation, followed by a finite fine partition for interval indicators,
therefore gives, for each epsilon>0, a constant A_epsilon such that

\[
 \sup_{z,J}\left|\sum_{i=0}^{L-1}1_J(\{z+i\lambda_1\})-L|J|\right|
 \le\epsilon L+A_\epsilon.
\]

The supremum includes all intervals J and all initial phases z. This is stronger
than pointwise equidistribution and is the needed property for moving endpoints.
For every fixed `(k_2,...,k_s)`, the admissible `k_1` form an initial integer row.
There are `O(T^(s-1))` rows, also valid as a single row when `s=1`. Summing the
last bound over them, dividing by `T^s`, and then sending epsilon to zero gives

\[
 \sup_J\left|\#\{k\in T_T:\{k\cdot\lambda\}\in J\}
       -|J|\frac{T^s}{s!\prod_j\lambda_j}\right|=o(T^s).
\]

Strict versus non-strict interval endpoints cause no problem: the uniform
approximation controls boundary neighborhoods too. In this application nonzero
integer relations between `1,lambda_1,...,lambda_s` are also excluded by prime
factorization, although only one irrational coordinate is needed for the argument.
No reciprocal-log independence is being substituted for this fact.

### 3.2 Shell weights and boundary phases

For every `x` in the half-open cube, the weight

\[
 W_x(t)=\prod_j q_j^{-\lfloor x_j+\theta_jt\rfloor},\qquad 0\le t<1,
\]

has at most s jumps, values between `1/product(q_j)` and 1, and therefore at most
`s+1` constant pieces. The interval discrepancy bound controls it uniformly over
all x, including when a jump approaches either endpoint or several jumps coincide.
Consequently

\[
 M_a=\frac{a^s}{s!\prod_j\lambda_j}\int_0^1W_{x_a}(t)\,dt+o(a^s).
\]

Replacing `(a+1)^s` by `a^s` incurs only `O(a^(s-1))`. The little-o statement is
for this fixed P; it does not claim a rate or uniformity over varying prime sets.
Most importantly, no convergent phase subsequence is required at this stage.

### 3.3 Infinite tail and normalization

For integer `r>=0`, exact floor addition gives

\[
 \frac{P_a}{P_{a+r}}=p^{-r}\prod_jq_j^{-\lfloor(x_a)_j+r\theta_j\rfloor},
 \qquad X_a=\frac1p\sum_{r\ge0}\frac{P_a}{P_{a+r}}M_{a+r}.
\]

Multiplying the shell formula at `a+r` by this ratio joins the two floor terms.
For fixed r the resulting integral is precisely the candidate profile integral on
`[r,r+1)`, with prefactor `1/(p s! product(lambda_j))`.

Writing `Q=product(q_j)`, the bounds

\[
 M_b\le(b+1)^s,\qquad P_a/P_{a+r}\le Qp^{-(s+1)r}
\]

give the common summable majorant
`(Q/p) p^(-(s+1)r)(r+2)^s` after division by `a^s`, for `a>=1`.
The profile integral pieces have the same type of bound. Truncate both sums at a
fixed r, apply the uniform shell estimate there, and then let the truncation grow.
This proves the entire moving-phase asymptotic, rather than only its restriction
to phases separated from the cube faces.

## 4. Cube continuity is not torus continuity

The profile integral is

\[
 I(x)=\int_0^\infty p^{-\lfloor u\rfloor}
                  \prod_jq_j^{-\lfloor x_j+\theta_ju\rfloor}\,du.
\]

Its kernel is at most `p Q p^(-(s+1)u)`, uniformly on the closed cube. Under
convergence of x, pointwise convergence fails only when a limiting floor argument
is an integer, a countable set of u. Dominated convergence proves closed-cube
continuity. The integrand is positive, hence I is everywhere positive. Compactness
then supplies a strictly positive global minimum and a finite maximum.

At opposite j-faces, `I(x with x_j=1)=I(x with x_j=0)/q_j`. Identifying those faces
would therefore introduce a genuine jump. Any argument applying a continuous-image
theorem to the entire orbit torus would be wrong. The candidate correctly uses
continuity only inside a nonsingular lifted arc and uses the jumps explicitly.

## 5. Arithmetic-progression closure and the interval of limits

Fix integers `m>=1,r`. Let K be the closure of `nm theta` in the torus. The
annihilator is

\[
 \Lambda=\{h\in\mathbb Z^s:m h\cdot\theta\in\mathbb Z\}.
\]

A finite basis of this integer subgroup and Smith normal form show that its
annihilator in the torus is a finite union of subtori. The averages of each
character along `nm theta` are 1 for h in Lambda and 0 otherwise, by geometric
summation. They agree with Haar measure on that annihilator; approximation by
trigonometric polynomials identifies the closure and gives equidistribution there.
Translation gives the required coset `r theta+K`. Every nonempty relatively open
part has positive Haar measure and is visited infinitely often. This also proves
cofinality, rather than just closure of an initial finite segment.

Each `theta_j=log_(q_j)(p)` is irrational by unique factorization. If the identity
component `K^0` had constant j-coordinate, the j-projection of K would be finite,
because K has finitely many components. But it contains the irrational rotation
`nm theta_j`, a contradiction. Thus every coordinate projection of `K^0`, and of
each component coset, is the full circle.

The tangent space L is the nullspace of integer equations and therefore has a
rational basis. Its coordinate functionals are all nonzero. Choose a rational
vector outside their finitely many kernels and clear denominators; this yields an
integer vector `v in L` with every coordinate nonzero. This construction does not
assume K is the full torus.

There is a point z in a chosen component with every coordinate away from a face.
Indeed each forbidden coordinate fiber has empty relative interior; finitely many
cannot cover the component. The loop `z+t v` for `0<=t<=1` stays in that component
and returns to its initial point. Each coordinate crosses a face only finitely
often. At a crossing, the ratio of the right-hand to left-hand profile value is

\[
 \prod_{j\text{ crossing}}q_j^{\operatorname{sgn}(v_j)}.
\]

This sign is worth checking: an increasing coordinate wraps from 1 to 0 and its
value is multiplied by q_j. A decreasing coordinate gives its reciprocal.
Simultaneous crossings cause the factors to multiply.

If the profile were constant on every intervening open arc, its total change
around the loop would be multiplication by `product(q_j^v_j)`. Returning to the
same nonsingular point would force this product to be 1. Distinct primes and a
nonzero integer vector rule this out. At least one open arc is therefore
nonconstant. Choose two points in that arc with unequal values and the closed
subarc between them. Ordinary continuity and the intermediate value theorem give
a nondegenerate compact interval of positive profile values.

Every phase on this subarc can be approximated by indices in the specified
arithmetic progression, with indices tending to infinity: use the infinite visits
proved above and nested neighborhoods within the same nonsingular coordinate
chart. Profile continuity there and the full-sequence little-o error show that
each value is a subsequential limit of `X_a/a^s`.

This verifies the asserted **existence of an interval contained in the limit set**.
It does not identify the whole limit set as one interval, and the candidate does
not claim that. Neither rational independence of reciprocal logarithms nor a
quantitative equidistribution rate is needed.

## 6. Quantitative three-prime bound and correction families

For `{2,3,5}`, choose a point of a component with its 3-coordinate on the zero
face. If its 5-coordinate is interior at y, the two limiting integral values are
`I(0,y)` and `I(0,y)/3`. Monotonicity and the 5-face identity give
`I(0,y)>=I(0,0)/5`, hence a gap at least `2 I(0,0)/15`.

If both coordinates are on faces, equal crossing orientations give values
`I(0,0)` and `I(0,0)/15`; opposite orientations give `I(0,0)/3` and
`I(0,0)/5`. Their smaller possible gap is again `2 I(0,0)/15` and their smaller
ratio is `5/3`. The transverse tangent vector used above makes both cases valid
one-sided orbit limits. Dividing by `4 log_2(3) log_2(5)` proves the candidate's
progression-uniform bound

\[
 \limsup X_a/a^2-\liminf X_a/a^2
 \ge \frac{I(0,0)}{30\log_2 3\log_2 5},
 \qquad \frac{\limsup X_a/a^2}{\liminf X_a/a^2}\ge\frac53.
\]

Positivity of the lower limit follows from the compact-cube minimum established
above. The integrand of `I(0,0)` equals 1 on `[0,1)`, so `I(0,0)>=1`.
Independent exact rational enclosures prove

\[
 0.0127214469683<\frac{I(0,0)}{30\log_2 3\log_2 5}
                <0.0127214469684.
\]

For a fixed polynomial Q of degree at most s, `Q(a)/a^s` tends to one constant;
for greater degree its absolute value diverges. A single constant cannot be
within less than half the gap of both extreme subsequential limits. Applying this
on each fixed residue class proves the quasipolynomial assertion and its stated
three-prime lower bound.

For a finite family, omit higher-degree polynomials eventually, since the
normalized tails are bounded and such polynomials diverge. The remaining
normalized polynomials approach a finite set C. The interval of subsequential
limits contains a value c outside C, at some positive distance delta from C.
Along an associated subsequence, all approximation errors remain at least
delta/2 eventually. This proves the positive limsup of the minimum error. It
handles arbitrary index-dependent selection, not merely periodic selection.
If all polynomials have higher degree, the minimum error diverges directly.

The finite-family obstruction does not apply to an infinite family, to
index-dependent coefficients, or to arbitrary integer carry sequences. Nor does
it rule out other kinds of irrationality arguments.

## 7. Historically recorded independent exact verification and code review

The audit checker imports and executes **no candidate code**. It uses only the
standard library and exact integer or rational decisions.

* Small cases enumerate the exponent boxes, sort the resulting smooth integers,
  and update the literal LCM at every integer. Independently, recursive integer
  division counts all smooth integers before each consecutive prime-power event;
  multiplying each event interval's reciprocal height by its full count gives a
  second shell mass. The constructions agree for 104 shells and 991 occurrences
  over nine prime sets, including singleton, two-prime, three-prime, four-prime,
  and five-prime tests, and smallest primes 2, 3, and 5.
* All eleven candidate sample starts, from 10 through 800, were reconstructed
  using 28 shells and prime-event cumulative counts. Every actual-tail enclosure
  and profile enclosure overlaps its candidate counterpart, has width below
  `10^-18`, and has the same exact shell numerator and occurrence count.
* The independent tail remainder is bounded by
  `P_a/P_(a+h) * (4320/343)(a+h+1)^2`. This follows from
  `X_b <= (15/2)(b+1)^2 sum_(r>=0)(r+1)^2/8^r` and the exact geometric moment
  `sum (r+1)^2/8^r=576/343`.
* Profile quadrature orders actual integer prime powers. Each event interval has
  an exactly known constant kernel. Its logarithmic length is enclosed using
  `log(n/d)=sum_(k>=1) z^k/k`, `z=(n-d)/n in [0,1/2]`, with 230 terms and
  fixed-point scale `10^64`. Every operation is rounded outward. The omitted
  remainder is at most `1/(231*2^230)`; induction on the nonnegative powers
  proves the propagated endpoints are bounds. This is a different series from
  the candidate's atanh calculation.
* The independent profile remainder uses the valid looser global bound
  `I(x)<=sum_(r>=0)15*8^-r=120/7`. The gap constant is integrated through 32
  shells and enclosed to width below `10^-25`.
* The checker pins the supplied candidate manifest hash and verifies every
  member's bytes and digest. A changed manifest is rejected. Its substantive
  checks are explicit exceptions, not Python assertions removable by optimization.

The candidate checker itself was also read: its shell numerator, interval
endpoints, exact jump ordering, factor 1/2, atanh positive remainder, and tail
majorant are consistent. In particular its majorant in equation (17) follows
from the three geometric moments at ratio 1/8; the constant term is correct.
The independent checks validate the output without relying on that implementation.

Normal execution used all eleven sample starts. Both `-O` and `-OO` executions
used sample starts 10, 100, and 317, all nine small-support cases, and the full
gap-constant check. Their common output agrees exactly, and their corresponding
fields agree exactly with the full normal run.

Finite computations corroborate the formulas and constants. The proofs in
Sections 3-6 establish the asymptotic and infinite subsequence claims; no finite
sample or residue scan is promoted to an infinite conclusion.

## 8. Prior-work attribution and remaining problem

The original letter separates repeated summation from summation over distinct
LCM values. Its printed year is 1974 despite an OCR error reading 1874; the letter
itself is dated 1 January 1973. The retained PDF was rehashed, its text read, and
its page visually inspected. [Erdős's original letter](https://www.fq.math.ca/Scanned/12-4/letter.pdf).

The retained Cook manuscript, revised 5 October 2026, was independently rehashed
and its relevant definitions and comparisons inspected. Its Section 8 already
supplies the repeated-tail recurrence, strict-prefix normalization, and weighted
odd-part lattice formula (Lemma 8.3); Section 9 supplies quadratic bounds and
denominator clearing. Sections 5.5 and 12 explain why unbounded carries and
surviving boundary strips defeat proposed shortcuts. These are prior ingredients,
not new claims of the candidate. [Cook's manuscript](https://wcook04.github.io/plectis/papers/erdos269-running-lcm-reasoning-surface.pdf).

The candidate's phase asymptotic and progression interval result are more
specific than the inspected growth bounds. This comparison establishes neither
priority nor novelty across the literature. The manuscript describes incomplete
independent checking and attributes its two-prime reduction to Fan; its external
transcendence input is not audited or used here. Live PDF retrieval failed during
this audit; comparison is explicitly to the retained hash-pinned revision.

Finally, rationality of the original series would make a fixed integer multiple
of every sufficiently late actual tail integral. Nothing proved here makes that
integer sequence polynomial or a finite choice of polynomials. For illustration,
`floor(a^s F(x_a))` is an integer sequence with the same leading normalized phase
profile; it is not asserted to obey the actual tail recurrence. The unresolved
arithmetic task is still to exclude the eventual integral reduced tails for the
actual numerators and every possible denominator. The error `o(a^s)` gives no
unit-scale fractional-part control. Thus the acceptance decision preserves the
candidate's partial-result and unresolved-problem status exactly.
