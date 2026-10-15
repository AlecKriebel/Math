# Independent audit: explicit nonlinear continuum-cover gap

Audit date: 12 October 2026 (UTC).

## Verdict and exact accepted object

**ACCEPTED UNCHANGED.** The original theorem, its rational margin `1/6075`, and its optional optimized margin `(18 - 8 sqrt(5))/675` follow from the stated measurable continuum hypothesis. No correction, replacement proof, or strengthened regularity assumption is required.

The accepted mathematical text is the [complete continuum proof](CONTINUUM_GAP_PROOF.md). This report expands and independently verifies that proof. No mathematical correction was required.

The audit establishes the following implication, and only this implication:

If a Lebesgue measurable function `d : [0,1] -> [0,1]` satisfies

    d(x)+d(y)+d(z)+d(x+y+z)
      >= 1 + (2/3)(d(x)d(y)+d(x)d(z)+d(y)d(z))             (N)

for three-dimensional Lebesgue almost every `(x,y,z)` with `x,y,z>0` and `x+y+z<1`, then

    integral_0^1 d >= 1216/6075
                    = 1/5 + 1/6075,

and in fact

    integral_0^1 d >= 1/5 + (18-8 sqrt(5))/675.

Nothing here proves that a finite arithmetic deletion problem, a weak limit of deletion profiles, or any Bose--Chowla construction satisfies (N). In particular, the spectral pair law and any passage from finite incidence counts to the exact nonlinear continuum inequality are outside this audit. The conditional number `4859/6075` is checked only as `1 - 1216/6075`.

## 1. Measurable-function and null-set preliminaries

Extend `d` by zero to all of `R`, writing the same symbol for its extension. Then `0<=d<=1` everywhere and `d` is in `L1(R)`. A Lebesgue measurable function may, if desired, first be replaced by a Borel representative. This changes none of the assertions used in the proof: the coordinate maps, the sum map from `R^3` to `R`, and the affine parameter maps of nonzero slope pull back one-dimensional null sets to null sets in the relevant domains. For the sum map this follows, for example, by using the invertible linear coordinates `(x,y,s=x+y+z)` and Fubini. Thus there is no measurability or representative ambiguity hidden in the integrals.

Define the translation modulus

    omega(h) = sup_{|v|<=h} ||d(.+v)-d||_L1(R).

Then `omega(h)->0` as `h->0`. To verify the uniform statement, take a continuous compactly supported `g` with `||d-g||_1<eta`. Translation is an isometry, so the displayed supremum is at most `2 eta + sup_{|v|<=h} ||g(.+v)-g||_1`; the second term tends to zero by uniform continuity on a common compact support. First let `h->0` and then `eta->0`.

If `r(t)=t+c` or `r(t)=c-t`, substitution gives

    integral_I |d(r(t)+v)-d(r(t))| dt <= omega(h)

whenever `|v|<=h`, because both affine maps have derivative of absolute value one. Finally, for `a,b,a',b'` in `[0,1]`,

    |ab-a'b'| <= |a-a'|+|b-b'|.

This estimate will be applied to the fixed given `d`, rather than to a sequence of functions with an unproved uniform translation modulus. That distinction is essential and is correctly maintained in the original proof.

## 2. The singular coupling and its lawful interior approximation

Fix `0<delta<1/100`, put `epsilon=delta/10`, and choose a nonnegative smooth probability density `rho_epsilon` supported in `[-epsilon,epsilon]`. The proof requests an even density; evenness is harmless but not needed for the estimates.

Set `I_delta=[delta,1/5-delta]`. For each `t` in this interval, use the source triple

    r_1(t)=t,
    r_2(t)=t+1/5,
    r_3(t)=3/5-t.

Its sum is `4/5+t`. Average uniformly over the six source permutations and independently add three noises with density `rho_epsilon`. The resulting finite measure on `R^3` has mass

    |I_delta| = 1/5-2delta.

It is the convolution of a compactly supported finite measure with the product of three smooth compactly supported densities. Consequently it has a nonnegative `C-infinity` compactly supported density `W_delta`. Differentiation under the finite-measure integral proves this smoothness directly.

The smallest possible source coordinate is at least `delta-epsilon=9delta/10>0`. The largest possible source sum is at most

    4/5+(1/5-delta)+3epsilon = 1-7delta/10 < 1.

Thus the support of `W_delta` is a compact subset of the open simplex. Because `W_delta` is absolutely continuous with respect to three-dimensional Lebesgue measure, the exceptional null set where (N) might fail has zero `W_delta` mass. Integrating (N) against `W_delta` is therefore valid. The proof never applies (N) directly to the null-supported original curve.

### 2.1 Exact marginal accounting

Before noise, summing the three source marginals gives precisely `1_{U_delta}` times Lebesgue measure, where

    U_delta = [delta,1/5-delta]
              union [1/5+delta,2/5-delta]
              union [2/5+delta,3/5-delta].

The reflected third source has unit absolute derivative and image equal to the third interval. Uniform source permutations leave this aggregate unchanged. In fact each single source-role marginal after permutation is one third of the aggregate, which confirms that there is no missing factor of three.

After noise the aggregate source density is

    S_delta = 1_{U_delta} * rho_epsilon.

The target density is

    T_delta = 1_{V_delta} * rho_epsilon * rho_epsilon * rho_epsilon,
    V_delta = [4/5+delta,1-delta].

The convolution formulas have total masses `3(1/5-2delta)` and `1/5-2delta`, respectively, as they must. Convolution of an indicator bounded by one with probability densities remains between zero and one.

The source support is contained in

    [9delta/10, 3/5-9delta/10],

and the target support is contained in

    [4/5+7delta/10, 1-7delta/10].

The separation between their nearest endpoints is `1/5+8delta/5>0`. Hence the aggregate four-role density `S_delta+T_delta` is bounded by one. Both source and target supports remain inside the two corresponding limiting intervals.

Smoothing does not literally keep the unmollified interval indicators fixed. It gives exactly the convolved marginals above, preserving the stated masses and density bound. In this case their convergence can be quantified without invoking any regularity of `d`:

    ||S_delta-1_(0,3/5)||_1 = 6delta,
    ||T_delta-1_(4/5,1)||_1 = 2delta.

Indeed each smoothed density is at most the corresponding limiting indicator almost everywhere, so the L1 difference is simply the difference of their masses. Therefore the integrated left side of (N) against `W_delta` converges to

    integral_0^(3/5) d + integral_(4/5)^1 d.

The absolute error is at most `8delta`, uniformly for all functions with values in `[0,1]`.

### 2.2 Pair-product limit for this fixed measurable function

Let

    Q = integral_0^(1/5) [d(t)d(t+1/5)
                          +d(t)d(3/5-t)
                          +d(t+1/5)d(3/5-t)] dt.

The sum of the three source pair products is invariant under permutation. Since the three noises are independent and identically distributed, its integral under the permuted noisy law can be computed with the sources in their original order. Each pair-product error is bounded by the two associated single-coordinate errors; each source occurs in two pairs. Integrating over `t` and averaging the noises therefore bounds the noisy-versus-unnoisy error over `I_delta` by `6 omega(epsilon)`.

The removed two parameter ends have combined length `2delta`, and the sum of three pair products is at most three. Extending the parameter integral from `I_delta` to `(0,1/5)` contributes at most `6delta`. Thus, explicitly,

    |integral W_delta * (three source pair products) - Q|
       <= 6 omega(delta/10) + 6delta -> 0.

This is a fixed-function L1 continuity argument. It neither assumes that (N) holds along the curve nor invokes weak convergence as a substitute for convergence of nonlinear products. The source proof is correct on this potentially delicate point.

### 2.3 The resulting gap inequality

The constant right-side term integrates to `1/5-2delta`. Passing to the limit now proves

    integral_0^(3/5) d + integral_(4/5)^1 d >= 1/5+(2/3)Q.

Write

    e = integral_0^1 d - 1/5,
    G = integral_(3/5)^(4/5) d,
    J = integral_0^(1/5) d(t)d(t+1/5) dt.

The two unretained pair products in `Q` are nonnegative. Subtraction of the gap integral gives

    e >= G+(2/3)J.                                        (A)

In particular `e>=0`. No uniqueness assertion about a linear minimizer, compactness argument, or approximation of minimizers enters this step.

## 3. The scaled first-moment cover bound

Dropping nonnegative quadratic terms from (N) gives

    d(x)+d(y)+d(z)+d(x+y+z) >= 1                          (L)

almost everywhere in the simplex.

For any measurable `f:[0,1]->[0,1]` satisfying (L), the preceding interior coupling proof without the pair terms yields

    integral_0^(3/5) f + integral_(4/5)^1 f >= 1/5.

Nonnegativity on the missing interval implies `integral_0^1 f>=1/5`. This is the required first-moment certificate and does not rely on the nonlinear limit argument.

For every fixed `0<a<=1`, set `f(u)=d(au)`. The map `(u,v,w)->(au,av,aw)` sends the unit simplex into the original simplex and has nonzero determinant `a^3`. The preimage of the exceptional null set remains null. Consequently `f` satisfies (L), giving

    integral_0^a d = a integral_0^1 f >= a/5.

There is no need to choose one null set uniformly over all `a`: the argument proves the conclusion for each fixed `a`, and the proof uses only `a=1/15`.

At this scale, `M=integral_0^(1/15) d>=1/75`. Put

    T={t in (0,1/15):d(t)>=1/10},
    beta=|T|.

The upper range bound `d<=1` and the threshold bound off `T` give

    M <= (1/10)(1/15-beta)+beta
       = 1/150+(9/10)beta.

Therefore `beta>=1/135>0`. The factor `9/10` is correctly retained. This sharp elementary level-set estimate is what supports the stated rational constant.

## 4. The E-cubed integration and convolution estimate

Define `E=1/5+T` and `u=integral_E d`. Translation preserves measure, so `|E|=beta`. Every point of `E` lies strictly between `1/5` and `4/15`. Hence every triple in `E^3` has positive coordinates and sum strictly between `3/5` and `4/5`; it is inside the simplex.

The set where (L) fails has zero three-dimensional Lebesgue measure, and its intersection with `E^3` also has measure zero, irrespective of the shape or regularity of `E`. Fubini/Tonelli applies to all nonnegative bounded integrands. Each source term integrates to `beta^2 u`, so their total is `3 beta^2 u`.

Let `q=1_E*1_E*1_E`. A change of variable `s=x+y+z`, followed by Tonelli, gives

    integral_(E^3) d(x+y+z) dx dy dz = integral_R d(s)q(s) ds.

For every `s`,

    q(s)=integral_(E^2) 1_E(s-x-y) dx dy <= beta^2.

It vanishes outside the closure of `(3/5,4/5)`, and endpoints are immaterial. It follows that the target integral is at most `beta^2 G`. Integrating (L) over `E^3` therefore yields

    beta^3 <= 3 beta^2 u + beta^2 G.

Since the previous section establishes `beta>0`, dividing by `beta^2` is legitimate:

    G+3u >= beta.                                         (E)

Meanwhile nonnegativity and the definition of `T` imply

    J >= integral_T d(t)d(t+1/5) dt >= (1/10)u.             (D)

Combining gives `G+30J>=beta>=1/135`. From (A),

    45e >= 45G+30J >= G+30J >= 1/135,

because `G>=0`. Thus `e>=1/6075`, proving the accepted rational result.

## 5. Exact six-inequality certificate

In the coordinate order `(constant,e,G,J,M,beta,u)`, the six input rows are

    A: (0,       1,-1,-2/3, 0,  0,    0)
    B: (-1/75,   0, 0, 0,   1,  0,    0)
    C: (1/150,   0, 0, 0,  -1,  9/10, 0)
    D: (0,       0, 0, 1,   0,  0,   -1/10)
    E: (0,       0, 1, 0,   0, -1,    3)
    F: (0,       0, 1, 0,   0,  0,    0).

All rows represent expressions known to be nonnegative. Their weights are

    (45, 10/9, 10/9, 30, 1, 44).

All weights are nonnegative. Direct dense-vector rational arithmetic gives the combined row

    (-1/135, 45, 0, 0, 0, 0, 0).

For clarity, the cancellations are:

- Constant: `-(10/9)/75+(10/9)/150=-1/135`.
- `G`: `-45+1+44=0`.
- `J`: `45(-2/3)+30=0`.
- `M`: `10/9-10/9=0`.
- `beta`: `(10/9)(9/10)-1=0`.
- `u`: `30(-1/10)+3=0`.

Thus the certificate is exactly `45e-1/135>=0`. In particular no hidden positivity assumption on `M`, `beta`, `u`, or `J` is needed for this concluding formal combination; all necessary analytic facts have already been used to establish its rows.

The corresponding constants are exactly

    e >= 1/6075,
    1/5+1/6075 = 1216/6075,
    1-1216/6075 = 4859/6075.

## 6. Optional optimization, including global maximality

Take a general threshold `0<tau<1/5`, while keeping `a=1/15`. The same level-set calculation yields

    beta >= a(1/5-tau)/(1-tau).

The translated triple calculation and threshold pair bound yield

    G+(3/tau)J >= beta.

Since `9/(2tau)>1` on the entire threshold interval, (A) and `G>=0` imply

    (9/(2tau))e >= G+(3/tau)J >= beta.

Consequently

    e >= (2/135) F(tau),
    F(tau)=tau(1/5-tau)/(1-tau).

Let `r=1-2/sqrt(5)`. It satisfies `0<r<1/5` and `r^2-2r+1/5=0`. There is a particularly direct global maximum certificate:

    r^2-F(tau) = (tau-r)^2/(1-tau) >= 0

for every `0<tau<1/5`. Equality occurs at `tau=r`, proving the claimed optimization without relying on a numerical critical-point search. Thus

    max F = r^2,
    (2/135)r^2 = (18-8 sqrt(5))/675.

The exact optimized margin is positive and strictly larger than `1/6075`. The latter comparison is equivalent to `sqrt(5)<161/72`; squaring positive quantities gives the exact excess `(161/72)^2-5=1/5184>0`.

For illustration only,

    rational gap   = 0.000164609053497942386831275720164609...
    optimized gap  = 0.000165120266669159153669052815036726...
    optimized total= 0.200165120266669159153669052815036726...

These decimals are not inputs to the proof.

## 7. Computational checks and their limits

The author checker was replayed from its preserved copy under ordinary Python, `python -O`, and `python -OO`. All three modes returned `PASS`. Each run exhaustively checked 256 finite convolution models and 15,625 finite level-set models, in addition to the author's exact arithmetic.

The independent checker uses standard-library exact rational and quadratic-field arithmetic. It does not import or call the author checker. Its 32 checks pass under all three Python modes. In particular it verifies the smoothing endpoint and mass identities symbolically as affine functions of `delta`, the dense-vector six-row certificate, the rational constants, and the global square-identity optimization certificate. This strengthens the endpoint sanity coverage beyond the author script's single sample `delta=1/200`.

All requirements use explicit exceptions, so they remain active under `-O` and `-OO`. Nevertheless these scripts check finite algebra, data identity, and finite sanity models. They are not machine-checked measure theory and do not replace the analytic arguments in Sections 1 through 4 of this report.

## 8. Acceptance scope, dependencies, and preservation

Accepted:

1. The original proof exactly as pinned above.
2. Interior smoothing of the singular coupling with correct aggregate marginals.
3. Fixed-function L1 passage for the nonlinear pair products.
4. The scaled first-moment cover bound for each fixed scale.
5. The positive-level-set estimate with its `1-tau` denominator.
6. Fubini/Tonelli over the arbitrary measurable set `E^3` and the `beta^2` convolution bound.
7. The exact six-inequality rational certificate.
8. The optimized threshold and its exact irrational constant.

Not established or endorsed by this audit:

- Sharpness of the gap or a characterization/uniqueness of minimizers.
- Any independently meaningful novelty claim.
- A spectral or arithmetic pair-incidence law.
- Preservation of nonlinear products in a weak limit of changing functions.
- Any unconditional upper bound for finite arithmetic deletion/retention problems.

The proof's only hypothesis beyond measurability and the range `[0,1]` is precisely (N). Its analytical tools are basic L1 translation continuity, finite-measure convolution, changes of variables, and Fubini/Tonelli. No external mathematical source is used as an authority for acceptance.

The accepted mathematical inputs were preserved unchanged. Independent integrity checks and negative controls passed. No remote state, branch, PR or repository publication was changed by the audit.


## Public editorial notice

All mathematical statements, proofs, examples, substantive audit arguments and scope limitations are retained. EDITION_NOTES.md describes the nonmathematical editorial changes: updated acceptance history, public dependency links and removal of excluded provenance metadata. The distributed edition is identified by MANIFEST.json. The complete one-vertex dependency and its audits are linked in DEPENDENCIES.md. Diagnostic summaries report checks rather than replacing mathematical proof. Independent internal AI acceptance is not external human peer review or proof-assistant certification.
