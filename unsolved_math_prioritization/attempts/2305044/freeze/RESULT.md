# Function Theory 5.44: attributed status correction and exact controls

Problem ID 2305044 / AMR-022-5044, queue rank 681. Inspection date: 2026-10-05 UTC.

## Result and classification

1. The original one-parameter question has a published affirmative resolution. The relevant prior publication is R. W. Barnard and K. C. Richards, *A direct proof of Brannan's conjecture for β = 1*, Journal of Mathematical Analysis and Applications 493 (2021), 124534, DOI https://doi.org/10.1016/j.jmaa.2020.124534. Its publisher abstract says that it supplies an analytic proof; an addendum exists at https://doi.org/10.1016/j.jmaa.2020.124666. The full article and addendum were not obtained here. This is a verified literature-status finding, not an independent audit of their full proof.

2. The unrestricted positive-parameter extension is false, including at degree five, so the negative answer does not depend on interpreting the separate degree-three sentence as part of the problem. An exact witness is α=3/2, β=1/32, x=−1:

   A₅(1)=2997183/268435456 > 0,
   A₅(−1)=3171231/268435456,
   |A₅(−1)|−A₅(1)=5439/8388608 > 0.

   A previously published, stronger every-index counterexample theorem appears in DannyExperiments, *Counterexamples to an all-positive Brannan coefficient inequality*, version 1.0.0, 2026-08-08, https://doi.org/10.5281/zenodo.21853316 and https://github.com/DannyExperiments/generalized-brannan-counterexample. The degree-three witness from that work is also reproduced exactly below. No novelty is claimed for the negative answer or its generalization.

3. The unit-square two-parameter assertion has a 2026 claimed resolution: T. M. Dunster, *The general Brannan coefficient conjecture II: Meijer-function approximations*, https://arxiv.org/abs/2606.11621v2. Theorem 1 includes all α,β∈(0,1], all unit-modulus x, and every odd degree at least three. Its introduction explicitly credits the earlier β=1 resolution. The numerical lower-bound components in this manuscript and its companion were not independently certified here. The current arXiv abstract has no journal reference for part II; the version inspected was revised 2026-07-17. This manuscript's claim is not being promoted to a newly independently proved theorem by this package.

Recommended disposition: **attributed literature resolution / independently reproduced counterexample, no new discovery**. Do not label this package a complete independent proof audit of the original β=1 theorem. Do not describe the β=1 question as still open merely because the 2018 source update or the dataset says so.

## Exact target and scope

Use analytic germs at z=0, with both powers normalized to take value one at zero. For |x|=1 and |z|<1, write

F(z;α,β,x)=(1+xz)^α(1−z)^(−β)=Σ A_j(α,β,x)z^j.

The coefficient identity is

A_j(α,β,x)=Σ_{k=0}^j binom(α,k) (β)_{j−k}/(j−k)! · x^k,

where (β)_r is the rising factorial and binom(α,k) is the falling-factorial binomial coefficient. Every A_j is a finite polynomial in x. The quantifier |x|=1 is a coefficient parameter; it does not require evaluating the generating series at |z|=1.

The original target is: for every α∈(0,1), every integer n≥2, and every |x|=1,

|A_{2n+1}(α,1,x)| ≤ |A_{2n+1}(α,1,1)|.

For β=1, A_j(α,1,x)=Σ_{k=0}^j binom(α,k)x^k. Odd partial sums at x=1 are positive, so the right-hand absolute value can be removed. The source also mentions the already-known degree-three case and failure of the even-index analogue. Its further question permits arbitrary α,β>0 and explicitly mentions degree three. Neither α>0,β>0 nor the original α∈(0,1),β=1 domain may be silently replaced by α,β∈(0,1].

The degree-five witness has α>1. It disproves the unrestricted extension, not the original β=1 theorem or the unit-square assertion. The sector lemma in PROOFS.md is a separately stated partial result, not a substitute for the full circle.

## Verification

Run `python3 verify_exact.py`. Only Python's standard library is required. `EXACT_CHECKS.json` records exact rational values, 616 cubic identity/endpoint cases, 496 β=1 endpoint controls, 192 recurrence controls, and 38 checks of identities used in the published every-index construction. Finite grids are controls, not proofs of universal assertions.

`PROOFS.md` gives self-contained mathematical derivations for the reproduced witnesses, an odd-index existence argument, and a sector partial result. `APPROACH_LOG.md` preserves the non-closing Bernstein experiment and the stop decision. `PUBLIC_SOURCE_MANIFEST.json` records source identity and inspection limits without reproducing source files. Publication remains gated on fresh independent review.

AI-assisted research and verification; no human specialist review or new journal acceptance is claimed.
