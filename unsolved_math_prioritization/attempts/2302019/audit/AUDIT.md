# Independent audit of reconstructed Problem 2.19 partial results

Audit ID: `2302019-independent-reconstruction-audit-20261005-v1`  
Date: 2026-10-05 UTC  
Author packet: `2302019-reconstruction-20261005-v1`  
Author manifest SHA-256: `6584a3d052edae771b709241b7ee909e7684efe318c0045e7ad36118f6008f12`

## Verdict and exact scope

**PASS for the stated partial results and their explicit limitations. The
general fixed-nonreal-point sharp-bound problem remains unsolved by this
packet. No mandatory mathematical correction was found.**

This is a fresh audit of the authenticated reconstruction, not a transfer
of acceptance from unavailable historical files. The reviewer independently
checked the mathematical deductions, source scope, executable checks, and
freeze. The frozen author directory was not edited. This AI-assisted audit
is not human peer review, a novelty determination, or a proof of the target.

Acceptance covers:

1. The exact exponential-type convention and degenerate cases.
2. Compactness and attainment of each fixed-point extremum.
3. The step-Poisson bound and the strict supremum gap for unequal positive caps.
4. The Bernstein ramp and its explicit positive penalty.
5. The globally admissible integrated-sinc witness and the rational gap.
6. Equal half-axis suprema for finite real-frequency sums, and the resulting
   obstruction to locally uniform approximation on any nonempty open set,
   under a common type bound and global admissibility.

Acceptance does not cover optimality of the ramp, identification of the
Gol'dberg--Levin envelope, reproduction of Eremenko's conformal-map formula,
a complete contemporary literature search, or any general nonreal extremizer.

## 1. Classical hypotheses and degenerate cases

Write M=max(A,B). The two open-half-axis caps imply |f(0)|<=min(A,B)
by continuity, so the entire real line has bound M. The bounded-real-axis
Phragmen--Lindelof estimate and Bernstein inequality apply to complex-valued
entire functions of exponential type at most K.

There is no circularity in using the source's stronger-looking global
growth convention. For every epsilon>0 the author's definition supplies
|f(z)|<=C_epsilon exp((K+epsilon)|z|). Apply the classical vertical estimate
with parameter K+epsilon and the same real-axis bound M, then let epsilon
decrease to zero at fixed z. This gives

    |f(x+iy)| <= M exp(K|y|).

It consequently supplies the fixed global constant M in the source growth
condition with exponent K. The reverse implication is immediate. Thus the
two classes agree in this bounded-real-axis setting. This argument also
handles K=0 without assuming a positive type margin.

Bernstein is valid for complex f; real-valuedness was not silently added.
If one starts with its real-entire formulation, fix a real x and choose a
unit phase eta making eta f'(x) nonnegative real. The real-entire function

    h(z) = (eta f(z) + conjugate(eta f(conjugate(z))))/2

has type at most K, real-axis modulus at most M, and h'(x)=|f'(x)|.
The real formulation therefore implies the required complex formulation.
The checked 1988 source states the classical inequality for entire f
without a real-valued hypothesis.

If either cap is zero, the function vanishes on an interval and hence
identically. If K=0, the vertical estimate makes f globally bounded;
Liouville then reduces the extremum to constants of modulus min(A,B).
For A=B>0, the signed exponential has exactly the stated type and cap and
attains A exp(K|y|), including the correct sign in each half-plane.
The subsequent positive-cap logarithms, L, a, and 1/K are used only after
the stated restrictions A,B,K>0. No zero-denominator limiting argument is
substituted for these exact degenerate cases.

## 2. Compactness and the attainment step

The vertical estimate is uniform over the entire admissible class, unlike
the individual constants C_epsilon. It bounds that class on every compact
subset of C. Montel thus gives a locally uniform subsequential limit, and
the same bound rules out an infinite limit. Uniform convergence on compact
sets makes the limit entire. Evaluation at each real t preserves both
caps, and evaluation at each complex z preserves the common vertical
bound. In particular the limit retains type at most K.

The class is therefore sequentially compact in the metrizable compact-open
topology and is nonempty. A maximizing sequence at a fixed z has a limit
in the class attaining its finite supremum. The signed exponential with
amplitude min(A,B) proves the stated lower bound, while the common
vertical estimate proves the upper bound. No claim about interchange of
suprema, uniform convergence on all of R, or closure of arbitrary
unbounded-type families is needed.

This compactness argument is essential to the strict supremum claim in
Section 3. Merely observing strict inequality for each f would not suffice.

## 3. Step-Poisson bound, branch, and equality

For y>0, multiplying f by exp(iKz) cancels the allowed upward vertical
growth. Thus g is bounded on the upper half-plane. With

    alpha = (log A-log B)/pi,
    O(z) = B exp(-i alpha Log z),

the upper branch gives |O(z)|=B exp(alpha Arg z). Its boundary moduli
are B on the positive ray and A on the negative ray; the sign and weights
are correct. Both O and 1/O are bounded because 0<Arg z<pi and both caps
are positive. Thus g/O is bounded and holomorphic.

The boundary-modulus maximum principle is applicable with the finite
exceptional boundary points 0 and infinity. One explicit justification is
to map the half-plane to the disk, use the Poisson inequality for the
bounded subharmonic modulus on smaller disks, and let their radii increase
to one. Boundedness and the boundary upper limits outside finitely many
points give the desired bound by dominated convergence. Neither a
boundary logarithm of f nor absence of zeros of f is assumed.

Equality at an interior point would force g/O to be a unimodular
constant. Taking boundary moduli at nonzero real points would then give
|f(t)|=A for negative t and |f(t)|=B for positive t. Continuity at zero
contradicts A!=B. Attainment from Section 2 converts this nonattainment
into S<U_step at each fixed nonreal point. The gap is point-dependent;
the packet does not claim a uniform positive gap over all parameters or
points. The lower half-plane follows from coefficient conjugation.

## 4. Bernstein ramp and every explicit constant

For 0<A<B and K>0, |f(0)|<=A and |f'(s)|<=KB for every real s.
Integration along the real interval, followed by the triangle inequality,
gives |f(t)|<=A+KBt for t>0. Combining this with the cap B gives precisely
the displayed envelope with L=(B-A)/(KB). It is positive, continuous,
bounded between A and B, and has bounded logarithm.

Its Poisson extension V is harmonic and satisfies log A<=V<=log B.
The upper half-plane is simply connected, so a harmonic conjugate exists;
Q=exp(V+i V_tilde) is holomorphic, zero-free, and has A<=|Q|<=B.
Continuity of log E gives the requisite limiting boundary modulus.
No boundedness of V_tilde is required. The quotient exp(iKz)f(z)/Q(z)
is bounded, and the same bounded-analytic maximum principle applies.

The difference from the step envelope is supported exactly on (0,L).
Subtracting the logarithmic Poisson integrals gives the stated D, with
the correct factor 1/pi. It is strictly positive since the kernel and
log(B/(A+KBt)) are positive in the interior of that interval.

On [0,L/2], the linear envelope is at most (A+B)/2, and
|t-x|<=|x|+L/2. Multiplying the resulting lower integrand bound by interval
length L/2 gives exactly

    d = L*y*log(2B/(A+B)) /
        (2*pi*((|x|+L/2)^2+y^2)).

All factors are positive under the stated hypotheses. Consequently
S<=U_ramp<=U_step exp(-d)<U_step is correct. Replacing y by |y| in the
kernel handles coefficient conjugation; reflection z to -z exchanges the
caps for A>B. No unjustified claim that this analytic envelope is attained
or is the sharp nonreal bound is present.

## 5. Integrated-sinc witness and quantitative separation

The primitive J_a exists globally because its integrand is entire. On R
the derivative is nonnegative and its zeros are isolated, so J_a is
strictly increasing, not merely nondecreasing. Oddness follows from the
even integrand. Integration by parts has vanishing endpoint terms, and
the damped Dirichlet integral has the stated arctangent value and Abel
limit. Thus J_a tends to +/-pi/(2a) on the two real tails.

The choice delta=min(A,B-A) ensures both nonnegativity of the negative
tail A-delta and the upper cap A+delta<=B. The open ranges stated for
F on each half-axis therefore imply the modulus caps globally. Its
negative and positive half-axis suprema are respectively A and A+delta;
neither requires attainment at a finite point. Delta is strictly positive
only in the asymmetric positive-cap case, exactly as assumed.

The representation s(w)=integral_0^1 cos(vw)dv proves
|s(w)|<=exp(|Im w|). Straight-path integration gives
|J_a(z)|<=|z|exp(2a|z|). With a=K/4, the excess polynomial factor is
absorbed using, for example,

    r exp(-Kr/2) <= 2/(eK),  r>=0.

Hence F satisfies a fixed-constant exp(K|z|) estimate; no unproved
closure statement about primitives at limiting type is used.

For 0<=t<=1/K, at<=1/4. The alternating sine-series lower bound yields
s(at)>=95/96>0. Squaring and integrating over length 1/K gives

    F(1/K)-A >= delta*(95/96)^2/(2*pi)
               > (9025/73728)*delta.

The coefficient 2a/K is 1/2, the denominator 96^2 is 9216, and the
strict final inequality follows from pi<4. These constants were checked
independently. The witness is not asserted to be extremal.

## 6. Recurrence and local-uniform obstruction

The torus pigeonhole argument is valid for arbitrary finite real
frequencies and arbitrary complex coefficients, not just commensurate
frequencies. Q^N+1 points in Q^N half-open cubes yield a positive integer
q_Q<=Q^N with all coordinate distances to integers at most 1/Q.

If these q_Q are unbounded, an increasing subsequence also has Q tending
to infinity, and its phases converge simultaneously to one. If they are
bounded, one fixed q occurs for unbounded Q; every coordinate distance
for that q is then zero, so increasing multiples give exact recurrence.
These are exhaustive alternatives. Positive and negative translates of
any fixed real t0 eventually lie on their respective rays and converge
in value to p(t0). Taking suprema proves equality of both ray suprema
with the whole-axis supremum. Constants, empty sums, repeated frequencies,
and cancellations cause no difficulty.

A globally admissible such p therefore satisfies |p(t)|<=A on all R
when A<B. The reverse triangle inequality at 1/K gives the displayed
witness separation even for complex p(1/K).

For the stronger open-set statement, the common type bound K and whole-
axis bound A give the uniform vertical estimate A exp(K|y|) for every
approximant. A subsequence converges locally uniformly on all C to an
entire G with |G(t)|<=A on R. Convergence to F on any nonempty open set
forces G=F there, and the identity theorem then forces equality on C.
The positive-real witness value contradicts |G|<=A. The open set need
not meet R or be connected. This argument does not require the entire
sequence to converge globally. Removing the common type bound, replacing
global caps by sampled caps, or using quadrature outside the admissible
class would invalidate this proof; the packet explicitly excludes these
extensions.

## 7. Source audit and historical scope

The complete Problem and Update 2.19 in the 2018 arXiv version were
checked in local PDF extraction, rendered imagery, and live web text.
The source's equal-cap upper-half-plane expression is consistently
extended to |y| in the packet. Bibliographic references 239 and 321
were also checked. The [2018 arXiv source](https://arxiv.org/pdf/1809.07200v2)
and [2019 publisher record](https://link.springer.com/book/10.1007/978-3-030-25165-9)
are distinct; the latter's full book text was not inspected.

Eremenko's [2003 survey](https://www.math.purdue.edu/~eremenko/dvi/progr.pdf),
entry 2.19 and reference 15, supports the historical distinction between
the real-axis result and the unequal-cap complex-point target. Its strict
positive-ray inequality is not imported into the packet's closed-cap
class, which follows the 2018 problem statement. Its historical status
does not establish the state of the literature in 2026.

The [1988 publisher record](https://www.mathnet.ru/eng/dan/v300/i3/p544)
and all three pages of web-extracted Russian text were independently
inspected. The opening and Theorem 1 concern the real-axis envelope;
page 545 states the classical Bernstein inequality. Retrieval by clicking
the record's PDF link succeeded after a direct web-open failed. OCR
defects remain, the page-image request failed, and local PDF bytes and
the English translation were not verified. None of the author's new
deductions depends on decoding the conformal-map formula.

The [Gol'dberg--Levin record](https://www.mathnet.ru/eng/dan29782) failed
web retrieval in this audit. Bibliographic corroboration was available
in the other inspected sources. No full-text or proof verification of
that work, and no identification with U_step, is asserted.

SOURCE_VERIFICATION.json records exact inspected PDF hashes and sizes,
public URLs, and access limits. Source PDFs, extracted source text, page
images, and unrelated data are not included in the audit deliverables.

## 8. Executable replay, independent attack, and integrity

The supplied verifier replayed byte-for-byte against EXPECTED_CHECKS.json:

- 832 exact rational controls: 56 coefficient/primitive controls,
  2 rational constants, 594 parameter controls, and 180 rational-frequency
  arithmetic checks.
- 2,413 floating-point smoke controls: 27 witness-gap checks, 27 checks at
  zero, 324 real-value checks, 2,025 checks over 405 upper-half-plane
  parameter points, and 10 sample period checks.

These are arithmetic and sample controls, not 3,245 theorem proofs.
The finite rational-frequency samples do not verify irrational recurrence;
the written torus proof supplies that result. The fixed 100-step entire
series and Simpson quadrature have no certified remainder/error enclosure.

The separately authored replay_audit.py additionally passed:

- Six adversarial integrity mutations, each rejected: same-length proof
  corruption, missing file, extra file, duplicate manifest path, symlink,
  and false byte count.
- Both optimized-Python guard checks: each author script refuses -O.
- One trust-boundary test: coherent proof-plus-manifest rewriting passes
  internal consistency as expected, but fails the separately fixed manifest
  digest. Thus an unauthenticated manifest is not an authenticity guarantee.
- 859 independent, non-certified 70-decimal smoke checks with mpmath 1.3.0,
  including 168 upper-half-plane points and cap ratios from 10^-6 to
  1-10^-8. The witness uses an independently derived sine-integral
  expression. Poisson quadrature uses t=x+y tan(u), making the kernel
  measure du, rather than the author's Simpson rule.

The independent numerical checks test potential sign, normalization,
near-boundary, and extreme-ratio failures; they are not interval-certified
or substitutes for the analytic proofs. Full output is in AUDIT_CHECKS.json.
The original eight-file inventory and external manifest digest were
verified again after all tests. The author packet remained unchanged.

## 9. Corrections, binding, and disposition

CORRECTIONS.md records no mandatory changes and three optional expository
clarifications. The exact original freeze passes without those edits.
AUDIT_BINDING.json ties this disposition to the author manifest and proof
hash. AUDIT_MANIFEST.json inventories these new audit files separately.

The accepted conclusion is a coherent set of partial results, including
the stronger open-set approximation obstruction. The unknown sharp
nonreal modulus and its maximizing entire function remain the missing
step. This audit does not convert the reconstruction's unsolved status
into a solution or establish a novelty claim.
