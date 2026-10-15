# Independent audit of the rational-arc escape packet

Date: 12 October 2026 UTC. Problem 2350 / Erdős 864, row 1741.

## Verdict

**MATHEMATICAL PASS as a scoped analytic partial. No correction to the frozen manuscript is required.**

The audited manuscript is the [complete rational-arc proof](RATIONAL_ARC_PROOF.md). Its accepted mathematical text was verified unchanged at the beginning and completion of the audit.

The following claims are accepted with their stated hypotheses:

1. The exact finite occupied-residue/window capacity inequality for every positive integer modulus and window length.
2. The density-square bound one half for a **congruence-only support certificate** at modulus `m=o(sqrt(L))`, including the shifted equation for a single half-integer coset.
3. The joint residue-profile L² capacity and, under macroscopic uniformity, the nonzero-character budget `1-c²`.
4. The complex signed-simplex inequality with constant `3 sqrt(3)/16`.
5. The lower bound on the aggregate fixed-rational major-arc signed contribution and the consequent negative signed contribution outside every fixed rational-arc family for an avoiding, macroscopically uniform sequence at `c²>=2/3`. The conclusion is subsequential and iterated, exactly as stated.
6. The conditional positive supersaturation statement under the explicitly additional signed minor-arc hypothesis.
7. Feasibility at mass one of the entire compatible, fixed-modulus weak sum/difference packing relaxation.

This is independent internal AI mathematical review of the stated results. It is not external human peer review, journal acceptance, proof-assistant certification, an exhaustive literature review, or a priority claim.

## 1. Audit method and independence

I read the complete frozen proof and reconstructed its arguments below. The universal conclusions are justified by that reconstruction, not finite enumeration. I wrote a separate diagnostic program from the definitions; it neither imports, reads, nor executes the author's checker. Exact arithmetic covers finite window identities, shifted residue certificates and packing, rational complex step functions, complex character phases, compatible profiles, and the constant comparisons. The diagnostic program has explicit exceptions rather than removable Python assertions.

The original author diagnostics are treated as historical metadata; they were not substituted for independent execution. The companion endpoint acceptance statement and relevant conventions from the accepted indicator-phase proof were inspected for interpretation. The independent argument below supplies the needed tail estimate directly. The other controlling inputs were identity-checked, without a claim here to have reread their entire contents.

The primary scholarly PDF was independently opened through the web tool. Only the attribution and variable-count applicability boundary recorded in Section 10 are used. No PDF bytes were retained and no PDF byte hash is asserted.

No remote mutation, publication, queue edit, or change to an accepted proof was made.

## 2. Finite colored-window capacity and uniformity of the growing-modulus error

Let `B` be a strong Sidon subset of `{1,...,L}`. Strong Sidonicity with repetitions is equivalent to uniqueness of every nonzero oriented difference: if `a-b=c-d` is nonzero, then `a+d=b+c`, and equality of unordered pairs forces the identical oriented pair. In particular the positive differences are distinct and `k(k-1)/2<=L-1`, so `k=O(sqrt(L))` independently of the modulus.

For a modulus `m`, write each element uniquely as `r+mt`, with `1<=r<=m`. The mapped coordinate `t+1` lies in `{1,...,N}`, where `N=ceil(L/m)`, even when `m>L`. Across all colors, a positive coordinate difference `d` is represented at most once because it corresponds to the difference `md` in `B`.

For the length-`H` moving counts `h_r`, direct expansion gives

    sum_{r,n} h_r(n)^2
      = Hk + 2 sum_{d=1}^{H-1} (H-d) sum_r r_{C_r-C_r}(d)
      <= Hk + H(H-1).

Each color has mass `H k_r` and support of size at most `N+H-1`. Summing its Cauchy–Schwarz inequality yields

    H² sum_r k_r² <= (N+H-1)[Hk+H(H-1)].

Division by `H²` is exactly equation (2), including `H=1`, empty colors, the empty set, and windows longer than the ambient coordinate interval. The occupied-class bound follows from `k²<=s sum_r k_r²`. Finite character orthogonality gives `sum_j |F(j/m)|²=m sum_r k_r²`; there is no missing factor of `m`.

For the corollary, if `(S+S)` and `(v+S-S)` are disjoint, each has at least `s=|S|` elements (fix one operand), so `2s<=m`. This support condition is exactly exclusion of the congruence `a+b+c-d=v`; it is strictly stronger than excluding just the integer equality. Supersets of the occupied support are allowed, since the capacity inequality with the number actually occupied also implies its weaker version with `|S|`.

The growing-modulus error is genuinely uniform. For `k>=1` set `H=ceil(sqrt(Nk))` and `epsilon=k/N`. Then

    (H-1)/N <= sqrt(epsilon),
    (k-1)/H <= sqrt(epsilon).

Thus the manuscript's argument can be made explicitly quantitative as

    k²/L <= (s/m)(mN/L)(1+sqrt(k/N))²
          <= (1/2)(1+m/L)(1+sqrt(k/N))².

Since `k/N=O(m/sqrt(L))`, the right side tends to one half when `m=o(sqrt(L))`. This does not require a uniform macroscopic profile. The case `k=0` is immediate. This calculation also makes clear why the proof cannot simply discard the restriction on `m`.

For equation (5) the modulus is fixed, and `H=ceil(L^(3/4))` gives `m(N+H-1)(1+(k-1)/H)/L -> 1`. Subtracting the zero character, whose contribution is `k²/L -> c²`, is justified. Equation (5) alone is a rational-point statement; the proof correctly obtains the arc bound from a separate function-valued argument.

## 3. Complex convolution identity and signed-simplex estimate

For `g` supported on `[0,1]`, `||g||_1<=||g||_2`. Its Fourier transform is in `L²` and `L-infinity`, hence in `L⁴` and `L⁶`. The triple convolution is in `L²` by Young's inequality:

    ||g*g*g||_2 <= ||g||_1² ||g||_2.

Plancherel, with the positive-exponent convention in the manuscript, therefore gives

    integral hat(g)^3 conjugate(hat(g))
      = integral (g*g*g)(d) conjugate(g(d)) dd
      = integral_{a,b,c>=0, a+b+c<=1}
          g(a)g(b)g(c) conjugate(g(a+b+c)) da db dc.

The conjugation is in the correct position. For complex `g` this is generally not an energy and need not be real or positive. Absolute integrability follows by applying the same Young and Cauchy–Schwarz estimates to `|g|`; alternatively compactly supported L² approximation establishes the identity by continuity of the quartic form.

Put `h=|g|` and split the absolute simplex integrand into `h(a)h(b)` and `h(c)h(a+b+c)`. Cauchy–Schwarz produces exactly the two integrals stated in the manuscript. In the second, changing variables to `d=a+b+c` leaves `a` ranging over an interval of length `d-c`, with Jacobian one. Thus

    I1 = integral (1-a-b)_+ h(a)² h(b)² da db,
    I2 = integral_{c<=d} (d-c) h(c)² h(d)² dc dd.

For independent `X,Y` distributed with density `h²/M`, where `M=||g||_2²`, and mean `mu`, the pointwise inequalities

    (1-X-Y)_+ <= (1-X)(1-Y),
    |X-Y| <= X+Y-2XY

hold on the full unit square. Consequently `I1<=M²(1-mu)²` and `I2<=M² mu(1-mu)`. This proves

    |Q(g)|² <= M⁴ mu(1-mu)³.

The derivative of `mu(1-mu)³` is `(1-mu)²(1-4mu)`; its maximum is `27/256` at `mu=1/4`. Taking square roots yields `3 sqrt(3)/16`. The zero-function case requires no division by `M`. For real constant `g=c` on `[0,1]`, the simplex volume is `1/6`, so `Q(g)=c⁴/6`.

The checker independently integrates rational complex step functions by exact volumes of intersections of boxes with the simplex, rather than reusing the author's integration code. These tests include genuinely nonreal values and phase cancellations. They support, but do not replace, the above L² proof. No optimality of the constant is accepted or needed.

## 4. Measure limits and the joint L² budget

For fixed `m`, the finite collection of positive measures `nu_{L,r}` has uniformly bounded total mass and common compact support. A subsequence therefore gives weak limits `nu_r`. Weak convergence of products on this compact set, followed by the continuous difference map, justifies convergence of each autocorrelation measure.

The key finite inequality is a measure inequality, not merely an integrated count:

    sum_r nu_{L,r} * tilde(nu_{L,r})
      <= (k/L) delta_0
          + (1/L) sum_{d in m Z, 0<|d|<L} delta_{d/L}.

The diagonal coefficient tends to zero. The second term is a Riemann sum converging to `(1/m)` times Lebesgue measure on `[-1,1]`. Testing against nonnegative continuous compactly supported functions proves

    sum_r nu_r * tilde(nu_r) <= (1/m) lambda

on the whole real line. Using the larger unrestricted Lebesgue measure is valid and sufficient.

For the normalized box mollifier `eta_epsilon`, Tonelli gives

    sum_r ||nu_r * eta_epsilon||_2²
      = integral (eta_epsilon * tilde(eta_epsilon))
          d(sum_r nu_r * tilde(nu_r))
      <= (1/m) integral (eta_epsilon * tilde(eta_epsilon))
      = 1/m.

The last kernel has integral one, not a height-dependent normalization. Weak compactness in the finite Hilbert direct sum `(L²)^m`, together with distributional convergence of the mollified measures to `nu_r`, identifies the weak L² limits as densities `f_r`. They are nonnegative, supported on `[0,1]`, and weak lower semicontinuity gives `sum_r ||f_r||_2²<=1/m`. This handles possible singular candidate limits; absolute continuity has been proved rather than assumed.

Under (U), the sum of these measures is `c` times interval measure, so `sum_r f_r=c` almost everywhere on `[0,1]`. Pointwise finite Parseval and integration then give

    sum_{j=0}^{m-1} ||g_j||_2²
       = m sum_r ||f_r||_2² <= 1.

The zero character is `g_0=c 1_[0,1]`. Subtracting its squared norm yields the claimed joint budget. In particular the hypotheses already force `0<=c<=1`. The `f_r` need not be constant. This step makes no invalid inference from macroscopic uniformity to separate residue equidistribution or a global Fourier supremum estimate.

## 5. Arc disjointness, convergence, phases, and order of limits

With `m,K` fixed, the centers `j/m` have separation `1/m`, so the arcs are disjoint for `L>2mK`. The zero arc is interpreted on the circle, including its wrap across zero; parameterizing it by `t in [-K,K]` counts each point once up to endpoints.

The identity

    F_L(j/m+t/L)/sqrt(L)
      = sum_r e(jr/m) integral e(tu) d nu_{L,r}(u)

shows pointwise convergence to `hat(g_j)(t)`. The derivatives in `t` are bounded in absolute value by `2 pi k/sqrt(L)` because `0<=b/L<=1`. Uniform boundedness and this equicontinuity upgrade convergence to uniform convergence on each fixed compact interval. The extra character factor converges to `e(-v j/m)` when `v` is fixed.

Under `alpha=j/m+t/L`, four Fourier factors contribute `L²`, the differential contributes `1/L`, and the theorem divides by `L`. The net factor is one. This verifies the normalization in equation (12).

For each fixed `K`, compact uniform convergence gives the inner major-arc limit. For the subsequent limit `K -> infinity`, each limiting transform is in `L⁴`, so its signed quartic integrand is absolutely integrable. There are only finitely many characters. No uniform-in-`m` tail statement, simultaneous `K(L)` limit, or growing-denominator claim is used.

The nonzero contribution is bounded by

    C0 sum_{j!=0} ||g_j||_2⁴
       <= C0 (sum_{j!=0} ||g_j||_2²)²
       <= C0 (1-c²)².

All phases have modulus one. The zero term is `c⁴/6`, giving `A_{m,v}>=Delta(c²)`. For an exactly avoiding sequence the total integral is exactly zero for every `L`; subtracting the major arcs gives the inner complement limit automatically. It is not necessary to assume compactness or existence of the untruncated minor-arc integrals separately.

A diagonal extraction gives limits for every fixed modulus, with compatibility inherited from the exact reduction identities at finite `L`. The phrase “every fixed denominator” can also be made literal for the smaller family consisting exactly of reduced fractions with denominator at most `Q`: take `m=lcm(1,...,Q)` and apply the same nonzero-character estimate to just the subset of its characters representing that family. The zero character is retained and the same joint budget bounds any subset. Thus no argument relies incorrectly on a monotonicity of signed integrals when passing from the full `m` grid to the denominator-at-most-`Q` family.

The conclusion concerns net signed contribution. It does not say that all fourth-energy mass escapes, that each individual complement point has negative phase, that one fixed irrational neighborhood must carry the contribution, or that a growing rational cutoff can be interchanged with the limits.

## 6. Residual replacement and the half-integer gauge

Let `G=(k/L)D_L` and `R=F-G`. The exact strong-Sidon fourth moment is `integral |F|⁴=2k²-k=O(L)`. Also `integral |G|⁴=O(L)` and hence `integral |R|⁴=O(L)` by the elementary fourth-power triangle bound.

The standard Dirichlet estimate `|D_L(alpha)|<=min(L,1/(2||alpha||))` gives, for `K>=1` and fixed `K` followed by large `L`,

    integral_{||alpha||>K/L} |G(alpha)|⁴ = O(L K^(-3)).

On the complement of any of the manuscript's major-arc families, this applies because the zero arc is included. Telescoping the quartic expression and applying Hölder gives

    integral_complement |F³ conjugate(F) - R³ conjugate(R)|
       <= ||G||_{4,complement} (||F||_4+||R||_4)³
       = O(L K^(-3/4)).

A unit-modulus phase does not alter the estimate. Therefore the normalized complement difference tends to zero in precisely the prescribed iterated limit. On nonzero fixed rational arcs `G/sqrt(L)` tends uniformly on compact scaled neighborhoods to zero; at the zero arc it tends to `c` times the interval transform, and `R/sqrt(L)` tends to zero by (U). The residual interpretation following Theorem 5 is therefore valid.

For a radius set contained in `Z+1/2`, translate by `+1/2` to the integer set `A`. Strong Sidonicity and differences are unchanged. Direct expansion gives

    a_A+b_A+c_A-d_A = a_B+b_B+c_B-d_B + 1.

Thus the forbidden integer equation is the shift `v=1`. Since `F_B=e(-alpha/2)F_A`, the signed quartic expression is `e(-alpha)F_A³ conjugate(F_A)`, giving exactly the phase `e(-j/m)` in the rational-arc limit. The sign is correct. The endpoint change is `O(1)` and is asymptotically harmless. No dilation by two and no conclusion for a mixed union of integer and half-integer cosets is being smuggled in.

## 7. Gap constants and the conditional supersaturation conclusion

Write `x=c²` in `[0,1]`. With `C0=3 sqrt(3)/16`,

    Delta(x)=x²/6-C0(1-x)²,
    Delta'(x)=x/3+2C0(1-x)>0.

At the threshold,

    Delta(2/3)=2/27-sqrt(3)/48>0.

The manuscript's squared-integer positivity check is valid; the diagnostic uses a separate rational squared comparison. At `c=1`, the joint nonzero budget is zero, so every nonzero profile vanishes and the escape value is exactly `-1/6`.

For a general sequence, `0<=T_v/L<= (2k²-k)/L` permits extraction of a convergent subsequence. The same major-arc identity then makes the iterated complement limit equal to `tau-A_{m,v}`. Hypothesis (H) therefore implies `tau>=Delta(c²)-eta` exactly as claimed.

For `eta=0`, positivity is equivalent to

    x > sqrt(6C0)/(1+sqrt(6C0)).

This threshold is below `2/3`. The difference from the endpoint target coefficient is

    Delta(x)-x(3x-2)/14 = x(3-x)/21-C0(1-x)².

It is concave, and its endpoint values on `[2/3,1]` are positive; hence it is positive throughout that interval. The algebra and direction of comparison are correct.

**The audit does not establish (H).** Neither the compact-profile convergence nor the L² rational budget controls the negative signed contribution outside all fixed major arcs. No unconditional positive supersaturation, unconditional improvement of the interval constant, or solution of Erdős 864 follows.

## 8. Shifted weak packing and full fixed-modulus compatibility

Let `d(n)` count positive differences and let `u(n)` count unordered sums with repetitions. Strong Sidonicity makes both occupancies at most one. If `T_v=0`, a simultaneous occupancy of `d(n)` and `u(n+v)` would give `a+b=v+(d-c)`, a forbidden quadruple. Thus, at each positive integer site,

    d(n)+u(n+v)<=1.

Restricting to `n congruent s modulo m` and dividing the counting measures by `L` yields a capacity `1/m` in the weak limit. Ordered sum convolution differs from twice unordered occupancy only on diagonal sums; their normalized total discrepancy is `O(k/L)=o(1)`. The difference profile at class `s` is `sum_r f_{r+s}*tilde(f_r)`, whereas the sum at the shifted site is in class `s+v`. The spatial translation is `v/L` and disappears for fixed `v`. Finitely many sites near zero have vanishing normalized mass. These facts give equation (17), including its residue shift and factor one half.

The independent nonzero-difference capacity similarly gives `D_{m,s}<=1/m` on the whole real line. Initially weak inequalities yield density inequalities almost everywhere; convolutions of compactly supported L² functions are continuous, so the displayed inequalities also hold pointwise where asserted. No disjointness of limiting density supports has been inferred from microscopic disjointness.

For `0<=c<=1`, choose every residue density equal to `(c/m)1_[0,1]`. Reduction from modulus `m` to a divisor `d` sums exactly `m/d` densities and returns `(c/d)1_[0,1]`. The autocorrelation and sum convolution are

    D_{m,s}(t)=(c²/m)(1-|t|)_+,
    S_{m,s}(t)=(c²/m)(1_[0,1]*1_[0,1])(t).

For positive `t`, their required combination is `(c²/m)(1-t/2)` on `(0,2)` and zero beyond. It is at most `1/m`, independently of the residue shift. The L² capacity is `c²/m<=1/m`. Hence every fixed-modulus constraint and all reduction compatibilities are simultaneously feasible at mass one.

The manuscript uses `c<=1` after having defined `c` as a nonnegative normalized cardinality; the implicit lower bound `c>=0` is understood. The mass-one maximality in this relaxation follows from the ordinary `m=1` L² bound and Cauchy–Schwarz on a unit interval. This is feasibility of weak data, not construction of strong Sidon integer sets with exact microscopic avoidance. The relaxation does not include the signed minor-arc condition.

## 9. Carry distinction and expressly excluded conclusions

The proof consistently separates three different objects:

- A support certificate excludes all congruent quadruples with residue value `v`.
- A fixed-rational arc keeps macroscopic position as well as residue information and is described by complex profile integrals.
- The integer count `T_v` is only one Fourier coefficient. Congruent coincidences can occur at every carry `v+jm`.

Integer avoidance alone does not authorize replacing the third object by the first. The shifted packing argument records necessary occupancy capacity, not identification of microscopic overlap from weak profiles. The proof makes no such illicit transfer.

Not accepted or claimed here: the missing signed decorrelation theorem; a nonuniform-profile version of the rational escape conclusion with the same zero-arc constant; a realization of the mass-one compatible profiles by exactly avoiding integer sets; any growing-cutoff theorem; a sharpness theorem for `C0`; novelty or worldwide literature status; or completion of the original problem.

## 10. Primary-source applicability check

Independently inspected: Miquel Ortega and Sean Prendiville, [Extremal Sidon Sets are Fourier Uniform, with Applications to Partition Regularity](https://jtnb.centre-mersenne.org/item/10.5802/jtnb.1239.pdf), Journal de Théorie des Nombres de Bordeaux 35 (2023), 115–134, DOI [10.5802/jtnb.1239](https://doi.org/10.5802/jtnb.1239).

The official PDF states Fourier uniformity in Theorem 1.2, residue-class equidistribution in Corollary 1.6, and smooth Bohr-neighborhood equidistribution in Corollary 1.7. Theorem 1.15 explicitly assumes at least five variables and a nonempty zero-sum coefficient subset. It does not supply the four-variable signed estimate needed here. The manuscript correctly treats this source as background attribution, not as a missing proof. The discussion distinguishes dense from extremal Sidon sets. The PDF's displayed scope agrees with the manuscript's cautious use. Only public bibliographic metadata and this applicability summary are retained; no copied source document or PDF-byte identity is asserted.

## 11. Verification record and preservation

The [complete acceptance statement](RATIONAL_ARC_ACCEPTANCE.md) accompanies this audit. Independent diagnostic output passed in normal, `-O` and `-OO` modes with byte-identical results. Independent integrity checks and mutation controls passed without changing the accepted mathematical text.

A passing finite checker is not the proof of an asymptotic assertion. Conversely the exact written arguments above are not a claim that every unproved condition in the research program has been established. The accepted outcome is the rational-capacity and signed-escape partial, with its explicit conditional supersaturation boundary.


## Public editorial notice

All mathematical statements, proofs, examples, substantive audit arguments and scope limitations are retained. EDITION_NOTES.md describes the nonmathematical editorial changes: updated acceptance history, public dependency links and removal of excluded provenance metadata. The distributed edition is identified by MANIFEST.json. The complete one-vertex dependency and its audits are linked in DEPENDENCIES.md. Diagnostic summaries report checks rather than replacing mathematical proof. Independent internal AI acceptance is not external human peer review or proof-assistant certification.
