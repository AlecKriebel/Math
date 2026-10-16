# Independent deductions used in the priority comparison

These are authored mathematical deductions, not quotations or claims that an external source states them. Source theorem hypotheses are catalogued separately in EVIDENCE_LEDGER.json. They establish overlap or separation from those hypotheses, never research priority by themselves.

## 1. The nonsymmetric quadratic specialization is already in a primary preprint

In the general-function theorem of arXiv:1806.10352v1, use the statistic function F(x)=x², k=1, and kernel exponent 0<α<1/2. For any β<2,

    a := max{β, 1/(1−α)} < 2.

Choose r=(a+2)/2. Then 1<r<2, F is C^r, and the required derivatives at zero are only F(0)=F′(0)=0. Thus its first marked-jump stable regime applies. Its normalization is F(n^α ΔX)=n^(2α)|ΔX|². Its sign condition for M1 also holds because x² is nonnegative. No symmetry of the Lévy driver is imposed in that preprint's model definition. This is a checkable specialization, not a reliance on its abstract.

Writing h(x)=x_+^α−(x−1)_+^α, substitution j=l−1 gives the exact identity

    W_α(1−u)=Σ_(j≥0) h(j+u)².

Hence the phase convention agrees after replacing a uniform mark U by 1−U. This deduction does not extend that theorem to β=2: then any r>β exceeds 2, and F″(0)=2 violates the required vanishing derivatives. The explicit β<2 hypothesis independently precludes that endpoint.

## 2. The candidate's non-monotone exponential tails do not create a strong novelty lane

There is a routine kernel localization for a bounded-quadratic-rate driver. Let χ be a C¹ cutoff equal to one near zero and zero outside a compact interval; put g_local=χg and h=(1−χ)g. Then h vanishes near zero, h′∈L¹∩L², and the convolution h*dY has an absolutely continuous version. Its drift derivative is bounded by B||h′||₁, while the martingale isometry bounds the expected squared derivative integrated over [0,T] by KT||h′||₂². Consequently its Δ^(−2α) increment-square sum tends to zero, since it is at most Δ^(1−2α) times that derivative energy.

The compactly supported g_local satisfies the eventual decreasing-absolute-derivative condition by choosing the threshold beyond its support; on the remaining compact interval its near-zero derivative bound can be enlarged. Thus the tail condition difference can be removed by this elementary reduction in the square-integrable overlap. This does not turn a non-Lévy driver into a Lévy driver, and does not remove a β<2 requirement.

## 3. A finite-quadratic-rate measure can have index two

For

    ν(dz)=1_(0<|z|<exp(−1)) |z|^(−3) log(1/|z|)^(−2) dz,

the change v=log(1/z) gives

    ∫|z|^q ν(dz)=2∫_1^∞ exp((2−q)v)/v² dv.

This is finite for q=2 (value 2) and q>2, and diverges for every q<2. The Blumenthal–Getoor infimum is therefore 2. For ε≤exp(−1),

    ∫_(|z|≤ε) z²ν(dz)=2/log(1/ε)→0.

There is no positive power ε^δ that bounds this tail by Cε^δ for all sufficiently small ε. The candidate's isometry/truncation estimate only needs convergence to zero. This separates its explicit assumptions from β<2 or the existence of a jump moment with exponent strictly below two. It does not separate the result from every conceivable known L² theorem; that requires a controlling source.

## 4. A deterministic compensator can change shape beyond scalar volatility

Let ν_s=δ₁ for s<1 and ν_s=δ₁+δ₂ for s≥1, on the entire real line. Realize its Poisson random measure by an always active rate-one unit-mark Poisson noise plus an independent rate-one mark-two noise active after time 1. Compensate all jumps and take b=0. This is an admissible candidate driver with deterministic quadratic-rate bound K=5 and a diffuse time compensator.

If Y were σ_-dL for a fixed scalar Lévy driver, at each point with σ≠0 its compensator measure on nonzero marks would be the scalar pushforward of a single fixed measure. Such a pushforward preserves total mass. The two displayed measures have total mass 1 and 2; zero volatility instead gives zero mass. Thus this compensator cannot be a scalar dilation of one fixed Lévy measure. A general marked-Poisson representation with a mark-dependent coefficient remains possible and is a different representation class.

This example proves strict noncontainment in the scalar representation class. The example itself is elementary finite activity and offers no priority certificate for the full theorem. Finite sums of known noises and separate jump impulses can often be handled by routine extensions of the published method.

## 5. What would constitute anticipation of the remaining class

A verified earlier theorem would need to deliver the same weighted jump-square limit for a singular convolution, allow an arbitrary predictable measure ν_s(dz)ds (or a genuinely equivalent marked-Poisson coefficient model), impose at most an appropriate L² rate/regularity condition rather than an exponent below two, and give the required original-sigma-field stable convergence. A model that merely defines more general ambit noise or admits state-dependent compensators does not supply this limit. Likewise, a limit theorem for increments of an observed semimartingale is not automatically a theorem for its smoothed, generally non-semimartingale convolution.

check_scope_separators.py reproduces exact auxiliary-exponent and finite-measure arithmetic certificates. The integral derivations and non-dilation proof above are the analytic certificates.
