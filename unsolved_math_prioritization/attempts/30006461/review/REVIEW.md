# Independent review: multiplication-table profile obstruction

**Verdict: PASS_SCOPED_FOURIER_OBSTRUCTION.** The elementary reduction, countermodels, approximation warning and conditional quantitative certificate are correct. No required correction was found. The actual multiplication-table nonconstancy problem remains **unsolved after one approach**.

Reviewed on 2026-09-30 by a separate AI reviewer, gpt-6-astra with xhigh reasoning. No human peer review or novelty is claimed.

## Frozen artifact and review boundary

OBSTRUCTION.md SHA256: **1fcff39750423d8e4b31d84bb4816f76378fb70f0c855beb2f9fd5008d0a2332**.

The reviewer read the full artifact and verifier, the complete OWR contribution on printed pages 2725–2727, the permutation manuscript's introduction and measure statements, the proof of its kernel Fourier formula, and the relevant convergence/formula passages in Sections 15–17. The OWR theorem page was also visually checked. The review does not independently validate the entire 116-page permutation proof, any unprovided multiplication-table proof, or the source's numerical upper ratio bound.

The submitted verifier reproduces its receipt byte-for-byte: **3,864 exact assertions pass**. An independently written checker passes **4,204 exact assertions**. These are elementary model controls; neither set computes the actual arithmetic measures.

## 1. Original target and source precision

The [OWR 51/2025 report](https://ems.press/content/serial-article-files/52435), published on 4 March 2026, announces the multiplication-table asymptotic and explicitly conjectures strict nonconstancy of its profile. The phase is the fractional part of log(log n)/log 2. The conjecture asks only for a ratio greater than one, not an assigned positive minimum oscillation.

The displayed definition of M(n) on page 2725 restricts x to [n], but the immediately following prose says it counts distinct entries in the full n-by-n table. The artifact records this inconsistency and uses that unambiguous prose and the standard multiplication-table definition. It does not silently convert the flawed display into a new target.

The complete [Green–Sawhney manuscript, arXiv:2604.28116v1](https://arxiv.org/abs/2604.28116v1), dated 30 April 2026, concerns the permutation probability p(k), with phase the fractional part of log k/log 2. The introduction and reference [27] explicitly call the multiplication-table paper forthcoming. The arXiv record inspected in this review lists v1 and no journal reference; “full manuscript available” must not be read as a claim of journal peer review.

Its Theorem 1.1 includes a positive scalar c₀, and its kernel is the reflection g(x) = G(−x) of the OWR kernel. Propositions 1.3 and 1.4 define the permutation measures, not an identified pair of arithmetic measures. The artifact preserves all these distinctions.

Bounded independent searches found talks, the OWR announcement, and the full permutation preprint, but no verified resolution of the arithmetic nonconstancy target. A search result or conference announcement describing a resolution of the asymptotic multiplication-table problem would not by itself prove the separate strict-oscillation conjecture.

## 2. Kernel Fourier transform and common-mode equivalence

Put a = log(log 2)/log 2. Then −1 < a < 0. The periodized kernel is positive and smooth: at the positive end its leading geometric decay is (log 2)^t, and at the negative end it is controlled by (2 log 2)^t. Every fixed derivative has the same integrable tail structure, with additional exponentially damped terms at the positive end.

With the artifact's Fourier convention, unfolding and u = 2^t give the argument s = a − 2πim/log 2. Integration by parts is legitimate for −1 < Re s < 0: the boundary term u^s(1−e^(−u))/s vanishes both at zero and at infinity. The integral is −Γ(s), yielding the stated coefficient −Γ(s)/log 2. The gamma function has no zeros and none of these s is a pole.

This is the reflected form of the already established Lemma 10.1 in the permutation paper. The sign is correct. Reflection changes coefficient m to coefficient −m; it does not identify the measures.

For finite positive measures with nonzero masses, convolution coefficients multiply and normalization to probabilities removes only the positive total-mass factor. Therefore the profile is constant precisely when every nonzero Fourier coefficient of the normalized convolution vanishes. Uniqueness of finite measures from trigonometric-polynomial integrals then gives Haar measure. This argument also supplies a positive lower bound for the profile, namely the product of the masses times min G.

The exact negation is a **single shared nonzero mode** at which both factors have nonzero coefficients. Two unrelated nonzero modes do not suffice. The established permutation paper already notes the corresponding reduction for its own measures; the artifact does not claim this as new.

## 3. Strictly positive countermodels and nonconstant approximants

For distinct positive integers r and s, the two cosine densities have integral one, lower bounds 1−|b| and 1−|c| greater than zero, and distinct nonzero Fourier supports. Their convolution is exactly Haar measure. Thus they are valid smooth, strictly positive, individually nonuniform controls on the incorrect implication being tested.

They are not asserted to be the actual arithmetic measures. They consequently refute neither the profile conjecture nor any specific arithmetic measure formula.

For the uniform q-point atomic measure, the geometric-series identity gives coefficient one exactly at multiples of q and zero elsewhere. Since the kernel's coefficient at q is nonzero, its convolution with this measure is nonconstant for every q. Nevertheless the uniform Riemann-sum bound is valid: on each interval of length 1/q, integrate the Lipschitz bound from its left endpoint to obtain total error at most Lip/(2q). Apply this to t ↦ G(x−t), whose Lipschitz constant is independent of x.

This proves uniform convergence to the constant mean, not just weak convergence. The surviving frequency moves with q, so it supplies no fixed-mode certificate in the limit. The q = 1 case and arbitrary odd or composite q pose no mathematical exception.

## 4. Quantitative certificate (10)

Subtracting the midpoint of the range from a real continuous function does not change any nonzero Fourier coefficient. The resulting function has absolute value at most half its oscillation. Hence oscillation is at least twice the modulus of each nonzero Fourier coefficient.

The two certified coefficient errors imply the lower bounds |ν̂(m)| ≥ |z|−ε and |ν̂′(m)| ≥ |z′|−ε′. Multiply these with the nonzero kernel coefficient. Finally use min f ≤ mean f = AB Ĝ(0), where Ĝ(0) is positive, and divide by the positive minimum. This gives the displayed ratio lower bound with exactly its factor of two.

Strict positivity of both error margins is essential. No pair of such arithmetic certificates is supplied. The permutation paper's limit descriptions and polynomial convergence estimates, including implicit constants, are not automatically a certified finite-stage error calculation; importing them for different arithmetic measures would require an additional justified identification.

## 5. Conditional cluster-set consequence

Under the announced asymptotic, boundedness of the continuous profile changes the multiplicative o(1) into an additive error tending to zero for the normalized sequence R(n).

For any fixed phase t, take n_j = floor(exp(2^(j+t))). The logarithmic change due to the floor tends to zero sufficiently rapidly that log₂(log n_j) − (j+t) tends to zero. At t = 0, fractional parts may approach one from below; convergence on the circle, as the artifact explicitly uses, handles this correctly.

Every phase and hence every profile value is a subsequential limit. Conversely, compactness of the circle supplies a phase limit along a subsubsequence of any convergent subsequence of R(n). The continuous image of the connected circle is the closed interval between the profile's extrema. Its minimum is positive. The cluster-set statement, the nonconvergence equivalence and the limsup/liminf ratio therefore all follow, conditional on the announced asymptotic.

This does not establish that the interval has positive length.

## 6. Independent checks and disposition

The submitted 3,864 controls reproduced unchanged. The independent 4,204 controls use:
- physical-space rational convolution on cyclic groups, rather than only multiplying Fourier dictionaries
- nonuniform positive mass-one measures from disjoint order-two and order-three characters
- translated tent-function quadrature for every q from 1 to 80
- exact positive cosine-model ratio bounds, including nonzero error margins
- shared-mode quantifier controls

The checker is standard-library Python and writes independent_results.json beside itself. The frozen OBSTRUCTION.md must also be adjacent. These controls neither evaluate gamma numerically nor identify an arithmetic measure.

Checked source PDF hashes:
- OWR: **0ab42f4636cc8f6fb9d3165313c5501ceef1a521f4ecb9a981e022fb68d0f4e1**
- Green–Sawhney v1: **bc148d3c8b95d7144aa88b9de23f218af3a63b9d8231b99b4ee5d5421829f7de**

Retain **unsolved, 1/5**, the announced-arithmetic/full-permutation-manuscript distinction, and the explicit absence of a common nonzero Fourier-mode certificate for the actual measures. No correction is required, and no constant or nonconstant arithmetic profile has been proved here.
