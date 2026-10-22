# Independent adversarial mathematical review of PR #1274

Review family: candidate adversary. Target: problem 2307072, Hayman–Lingham 7.72. Submitted head: `fc334f4bd5d8cbc2a241293e2b1419d35c7eead1`.

**Verdict: PASS for the full negative mathematical answer under the printed conventions. No unresolved mathematical concern was found.** This verdict covers the explicit polynomial family for every positive integer parameter and the separate bounded input with essentially unbounded transform. It does not establish historical priority, present-day openness, or external human peer review. This review is AI-assisted.

## Inputs, independence, and source inspection

I read the full submitted `PROOF.md`, `AUDIT.md`, `SOURCE_VERIFICATION.json`, `README.md`, `PUBLIC_MANIFEST.json`, and `EDITORIAL_MAP.json`. `INPUT_AUTHENTICATION.json` independently checks the byte count, SHA-256, and Git blob SHA-1 of all six files against the immutable submitted snapshot, including exact six-file membership. These are current submitted artifacts, not an assumption that the inherited audit is correct.

I did not read another review family's report, computations, or source notes. The task itself identified the intended conventions and potential failure points; the submitted proof exposed its candidate formulas. Thus this is an independent adversarial verification, not a blind independent discovery. The new checking program was implemented from scratch using only the Python standard library and exact fractions. Neither historical checking code nor another family's implementation was available to this review.

The primary PDF was freshly retrieved from `https://arxiv.org/pdf/1809.07200v2` with HTTP 200. It has 1,706,228 bytes and SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`, agreeing with the submitted pin. I rendered and visually inspected the complete PDF page 184, printed page 183; I also checked the version-specific arXiv record at `https://arxiv.org/abs/1809.07200v2`, which gives revision date 21 September 2018. The printed problem uses the bilinear product, all area-integrable analytic test functions, the negative coefficient −1/π, the unit-disc integration region, and polynomials in both variables. The polynomial question includes the proposed uniform inequality. The earlier no-progress sentence is not evidence of current openness. The local source PDF, extracted page, and rendered image are private inspection inputs under `_local`, excluded from the authored manifest. Source byte identity authenticates this retrieval, not the mathematics.

## Exact target and possible ways it could fail

The required statement is that neither (i) membership of every bounded bilinear annihilator input in the bounded-output space nor (ii) a universal output/input bound, even after restricting inputs to polynomials, holds. The two counterexamples have different jobs. A growing sequence of bounded polynomial transforms alone would not disprove membership for an individual general input. An infinite value at one isolated point would not establish an infinite essential norm. Confusing bilinear and sesquilinear annihilation would invalidate the examples. A Cauchy primitive with an unidentified entire correction, a boundary jump, or a point mass at zero could also invalidate the proposed transform calculation. I checked these possibilities separately below.

## Independent derivation of annihilation and normalization

Let t=|z|². Write the input as exp(2iθ)a(t). If φ is analytic and integrable in area, boundedness of a makes the product absolutely integrable. Polar Fubini therefore applies without any assumption about the boundary behavior or global summability of the Taylor series. For each fixed interior radius, uniform convergence of the Taylor series on that circle permits angular integration. Every exponent in exp(2iθ)φ(rexp(iθ)) is n+2 for n≥0. Every angular integral vanishes. This proves annihilation against the entire required analytic L1 space, including tests with unbounded boundary behavior.

For the polynomial family, P_m(t)=Σ_{j=0}^{m−1}(1−t)^j and a_m(t)=tP_m(t)=1−(1−t)^m. This is a polynomial, with 0<a_m(t)<1 on the open interval and limit one as t tends to one. For every 0<ε<1, the annulus t>1−ε^(1/m) has positive area and a_m(t)>1−ε. Hence the input's essential norm is exactly one. The general input a(t)=1 has modulus one away from its immaterial assigned origin value.

As a deliberate convention test, the same polynomial input would **not** annihilate the sesquilinear test z²: its normalized pairing would be ∫_0^1 t a_m(t)dt=1/2−1/((m+1)(m+2))>0. Thus the absence of conjugation in the visually checked primary statement is essential, and not an interchangeable convention. The exact program checks this positive moment independently for all sampled m.

## Independent identification of the full Cauchy primitive

One way to find the candidate is to seek u(z)=zq(t). Then dbar(u)=z²q′(t). Solving q′=P_m with q(1)=0 yields q_m(t)=−∫_t^1 P_m(s)ds. For the general angular input, the corresponding equation is tq′(t)=a(t). In particular q(t)=log t for a=1. These differential equations suggest the formulas, but do not by themselves identify the convolution or rule out a holomorphic correction.

For that identification, I independently used a contour residue calculation. At a fixed radius r unequal to |z|, put w=exp(iθ). The angular Cauchy integral is (1/i)∮ w/(z−rw)dw. It is zero if r<|z|. If r>|z|, its only pole inside the circle is w=z/r with residue −z/r², so the angular integral is −2πz/r². The full Cauchy kernel is absolutely integrable against bounded compactly supported inputs; radial Fubini is valid and the exceptional radius can be omitted. Substituting s=r² gives

Cf_a(z)=−z∫_{|z|²}^1 a(s)/s ds inside the disc, and zero outside.

At zero the angular integral is zero directly. For bounded a, the inside formula is bounded in absolute value by ||a||∞ |z| |log|z|²|, which tends to zero at zero. It also tends to zero at the unit circle. Consequently it is the actual full-plane Cauchy transform, with no unspecified holomorphic term. For the polynomial family this gives q_m(t)=−Σ_{k=1}^m(1−t)^k/k. For a=1 it gives u=zlog t. The sign and radial factor agree with the submitted proof.

## Distribution, principal value, and boundary tests

For E(z)=1/(πz), punctured-domain integration by parts gives dbar(E)=δ_0 and dz(E)=−pv(1/z²)/π. In the dz identity, the inner boundary term is a multiple of ∫exp(−2iθ)ψ(εexp(iθ))dθ, which tends to zero. In the dbar identity the angular factor is one and the same normalization gives ψ(0). The principal-value distribution exists because the constant part of a smooth test has zero angular integral, and the remaining O(r) factor makes the local absolute error integrable. This checks the minus sign independently of the candidate primitive.

Since the input is bounded with compact support, convolution identifies the distributional dz derivative of its Cauchy transform with the indicated Beurling kernel distribution. This step does not require a Calderón–Zygmund mapping theorem, assumed L∞ boundedness, or an inversion result that would be circular here.

There is also a pointwise check where the input is C1. On a small centered disc, subtract its value at the evaluation point. The constant kernel integral vanishes, while the remainder is bounded by L/|h|. Its omitted ε-disc has absolute contribution at most 2πLε before the fixed factor 1/π. The bound is uniform on compact subsets of the C1 region. The nonsingular remaining convolution is continuous there. Thus the ordinary circular principal value exists at all these points, is continuous locally, and equals the distributional derivative. Polynomial inputs are C1 at every point inside the disc; the single angular input is C1 away from zero. Its failure to be C1 at zero is explicitly handled, not assumed away.

For u_m=zq_m(t), the trace at the unit circle is zero and there is no singularity at zero. Zero extension has no boundary measure in its first weak derivatives; bounded interior derivatives and zero exterior derivatives give a global W1,∞ function. For u=zlog t, continuity at zero follows from rlog r→0 and the unit-circle trace again vanishes. On an ε-punctured disc, the inner boundary error is bounded by a constant times ε²|log ε|, tending to zero. Its first derivatives are locally integrable, indeed in every finite Lp since ∫_0^1 r|log r|^p dr is finite. These estimates rule out a delta mass at zero or a circle measure. A jump in the derivative at the circle does not create a measure in the first derivative of a continuous primitive. No second derivative is used in the claimed formula.

The resulting full-plane derivatives are

- dbar(u_m)=v_m times the disc indicator, and dz(u_m)=G_m(t) times that indicator;
- dbar(u)=z/bar(z) times the disc indicator, and dz(u)=(1+log t) times that indicator.

These are almost-everywhere statements; no boundary-circle point value is needed. Exterior principal values vanish because the input is locally zero there and the full Cauchy transform is identically zero outside.

## All-parameter exact norm argument

Differentiating zq_m(t) gives G_m(t)=q_m(t)+tP_m(t). Therefore

G_m(t)=1−(1−t)^m−Σ_{k=1}^m(1−t)^k/k.

Its endpoints are G_m(0)=−H_m and G_m(1)=1. On 0<t<1 its derivative is P_m(t)+m(1−t)^(m−1)>0. This is an all-m argument: positivity comes from the finite sum of positive terms, not a coefficient sign pattern or a finite numerical test. As H_m≥1, these facts give the upper essential-norm bound H_m.

For an explicit positive-area lower bound, P_m(t)≤m and G_m′(t)≤2m on [0,1]. Given 0<η<H_m, let δ=min(1,η/(2m)). On 0<t<δ, G_m(t)<−H_m+η, so |G_m(t)|>H_m−η. This region has area πδ>0. Hence the essential norm equals H_m; the argument never relies only on the isolated value at zero. At zero the absolutely convergent original integral also gives −∫_0^1P_m(t)dt=−H_m, independently checking the sign and π normalization. The endpoint case m=1 gives G_1(t)=2t−1 and norm one, as required.

Finally H_(2^k)≥1+k/2 by grouping successive dyadic blocks, so H_m is unbounded. There is no universal polynomial bound. Every fixed polynomial witness still has a bounded transform; this is the correct scope of the polynomial conclusion.

## Single-input essential unboundedness

For u=zlog t, dz(u)=1+log t at every nonzero point inside the disc by the pointwise argument above. For M≥1 the positive branch never exceeds M; the negative branch has |1+log t|>M exactly when 0<t<exp(−M−1). The corresponding area is πexp(−M−1)>0. Thus the essential norm is infinite independently of any choice at zero.

At zero the truncated original transform is −2∫_ε^1 dr/r=2log ε, tending to negative infinity. This isolated divergent principal value is compatible with the almost-everywhere result, but is not used as evidence for essential unboundedness. The formula also agrees with the pointwise m→∞ limit of G_m(t) for every fixed 0<t<1, because Σ_{k≥1}(1−t)^k/k=−log t. This limit is a consistency check, not a substitute for the direct single-input calculation.

## Independent exact computations and adverse controls

`check_independent.py` expands the nested input polynomial directly in exact integer coefficients, constructs a bivariate monomial primitive with a fixed zero boundary trace, differentiates it with independent formal Wirtinger operators, and compares its result to the closed radial formula. For m=1 through 80 it checks input normalization identities, the origin integral, the bivariate dbar equation, zero trace, the product rule, the closed expression, both endpoint values, and the derivative identity. It also checks exact interior values and the deliberately wrong-pairing positive moment.

A separate invariant checks ∫_0^1G_m(t)²dt=∫_0^1a_m(t)²dt=1−2/(m+1)+1/(2m+1). This follows independently by integrating d(tq_m(t)²)/dt, whose endpoint terms vanish. The program also checks its polarized counterpart for 79 adjacent pairs. This invariant would expose many sign, boundary, or coefficient mistakes in the reconstructed transform. It does not by itself determine the sign, which is fixed by the direct original-kernel origin integral.

All **1,200 exact checks** pass under normal Python, `-O`, and `-OO`. The three JSON results are byte-identical, 411 bytes each, SHA-256 `bb3fc9904ab01fa5f7066e6e6fb0ce4148c58cfc9a10de37d34e59c456d8a082`. A deliberate false guard exits unsuccessfully with the intended ValueError under each mode; no validation depends on removable assertions. `EXECUTION_RECEIPT.json` records interpreter and program identities and those adverse-control outcomes. These are fresh independent checks, not a claimed rerun of the old 512 checks whose original code was absent from the submitted packet. Finite checks are ancillary: the analytic and all-m arguments above carry the conclusion.

## Limits and disposition

The current submitted proof is mathematically sound for the full printed question. No repair is requested on mathematical grounds. No historical priority investigation was performed in this family; the packet's inherited historical source or attribution assertions are not promoted to newly verified findings here. Current output ranges in the editorial map can be checked against the submitted bytes, but unavailable historical input bodies cannot be authenticated by merely reproducing their stated hashes. Source provenance, publication framing, exact author credit, and preprint readiness still require the parent workflow's separate audits.
