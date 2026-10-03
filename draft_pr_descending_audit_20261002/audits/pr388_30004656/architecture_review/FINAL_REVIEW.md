# PR 388 Turns 4–5 independent adversarial review

**PASS for the two stated restricted architecture theorems, conditional on retaining the mandatory additive chaining clarification. No new material concern or required repair was found. The broad original conjecture remains unsolved.**

Completed 2026-10-02 17:46 PDT / 2026-10-03 00:46 UTC. Completion estimate for this assigned architecture audit: 100%. This is an AI-assisted independent analytic review with exact computational controls; it is not human peer review or a historical priority certificate.

## Independence and reproducibility

Reconstructed the proofs from the frozen Turn 4 and Turn 5 statements before consulting the preexisting review or implementation. The preserved `INDEPENDENT_DERIVATION.md` had SHA-256 ea04438e875528449e07e4ec389907c199ed4970edfb645a4122f2e62f57b431 at that checkpoint. Subsequent comparison with the preexisting review did not change the mathematical assessment.

Run `python3 independent_controls.py` from this directory. The new implementation imports no candidate or prior-review code and passes **168,007 exact assertions**, with details and script binding in `CONTROLS_RECEIPT.json`. Those checks supplement the analytic proof and do not infer infinite probability claims from finite observations. The source candidate, Git index, main branch and services were not changed.

## Turn 4: precise findings

* Full row rank realizes all strict activation patterns. The empty pattern makes the homogeneous part vanish at some sphere point, allowing the proved global bound G<=3L. Complementary subset gradients and Rademacher averaging then give the coefficient energy <=36L^2. Arbitrarily poor conditioning creates no unsupported inverse bound.
* The output constant cancels through centered labels. Conditioning on all labels leaves iid inputs and deterministic weights z_i with sum z_i=0, sum z_i^2<=n. Independent-copy symmetrization supplies the increment and atom mgfs without wrongly bounding centered absolute ReLU moments directly.
* With the clarification, the base is e_1 and all nets are fixed before observing labels or inputs. Only short possible links are assigned the short-distance tail estimate. Their cardinality is bounded by the product net size; countable union bounds are summable. Continuity and telescoping establish a single event over every direction, including directions chosen by an adaptive network.
* The constants give the stronger lower bound sqrt(n/k)/3072, hence the stated /4096. No n>=d condition was smuggled in. d=2, k=1, k=d, tiny n and all-equal-label failure cases are consistent.

**Required existing correction:** `ADDITIVE_CHAINING_CLARIFICATION.md` must accompany the packet. Without it the reused u_0 notation permits a sample/network-dependent chaining base, which the fixed-direction concentration argument would not justify. It is already corrected additively; no new correction is requested.

## Turn 5: precise findings

* The exact sphere seminorm of x^T A x is eigenvalue spread, established by scalar subtraction and a great-circle tangent limit. Antipodal even/odd projections bound spread and ||b|| separately by L. No ambient operator norm is silently substituted for the sphere norm.
* Equal label counts are selected using labels only. Conditional on the complete label sequence, all selected inputs remain iid spherical. Odd n produces an even selected N with N>=3n/4, without a rounding exception. The signed matrix is exactly trace zero, so scalar shifts in A are harmless.
* The centered spherical-square moment expansion is absolutely controlled for |lambda|<=1/8. Both Chernoff regimes, their boundary dt=4N, and deterministic quadratic/vector nets give the stated conditional failure probabilities. Uniformity over balanced signs is sufficient; it requires no union over label sequences or adaptive matrices.
* The full-sample error bound controls the selected sample. At least one matrix/linear correlation term is large. The branches k<d and k>=d cover all widths, zero/full-rank A, and k=d exactly. Their final constants imply the claimed /8192.
* The fixed activation is globally 2-Lipschitz; rescaling keeps every quadratic-core realization within |t|<=1 on the entire sphere. The conclusion does not extend to arbitrary neurons leaving that core.

## Adversarial controls and disposition

New exact controls include all qualifying label-count pairs for n=16,...,600, all strict activation patterns through k=9 in an invertible construction, arbitrarily small rational singular scales, radial distance inequalities, exact chaining geometric sums and log bounds, both Bernstein regimes, non-diagonal rational sphere quadratics, shifted/low-rank nuclear bounds and scalar-shift pairings.

Negative controls show explicitly that dependent ReLU rows may have zero function but arbitrarily large coefficient energy, and that A=M I may have large operator norm but zero sphere seminorm. These falsify unrestricted extensions of the proof while supporting the necessity of the candidate's stated restrictions.

Accept these two partial results as mathematically supported within their exact scope. No outstanding repair is identified. Retain the original **unsolved** disposition, the additive clarification, and the explicit exclusions; no paper claiming resolution or priority should follow from this architecture review.
