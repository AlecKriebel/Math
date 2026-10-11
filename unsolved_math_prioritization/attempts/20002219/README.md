# Bounded-interval Schur ratios: audited partial progress

Target: 20002219 / AIM-LINEAR_ALGEBRA-0013, AIM total positivity Problem 1.45.

Status: ACCEPT_PARTIAL_AS_WRITTEN. The arbitrary-partition, arbitrary-dimensional bounded-interval classification remains unresolved. No mathematical correction is required, and no novelty or priority is claimed.

This is an AI-assisted, unrefereed mathematical edition. Acceptance means an independent internal AI audit of the stated partial results. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The full authored proof and full mathematical audit are retained in PROOF.md and AUDIT.md. Copied source documents, source text and images, executable code, raw datasets, raw search responses and private coordination material are not distributed. References to checking programs describe historical verification; those programs are not included.

Source retrieval, inspection and mathematical execution statements describe the original candidate and independent audit of October 11, 2026 UTC. Editorial preparation authenticated their sealed bytes, but performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Finite checks support exact identities only; the universal analytic and sign arguments must be read in full.

## Accepted results

- Complete N=2 interval classification for nondegenerate positive intervals with 1 in their closure, including finite/infinite width, degree-zero cases, threshold uniqueness, excluded endpoints, equality and attainment. The independently re-proved imported example (3,3)/(4,1) has sharp threshold 1+sqrt(2) on [1,B]^2.
- One exact N=3 pair: lambda=(5,1,1), mu=(4,3,0). For every nonempty positive interval I, the normalized ratio (24/15)s_lambda/s_mu is at least 1 throughout I^3 exactly when (sup I)/(inf I) is at most rho, where rho is the root greater than 1 of 5rho^3-6rho-4=0. A zero lower endpoint or infinite upper endpoint means infinite quotient. The full six-coefficient Bernstein identity, continuum positivity argument, sharp counterexample and endpoint-equality classification are retained.
- The positive-part pair (6,2,2)/(5,4,1) gives the identical ratio. The equal-degree partitions are incomparable by majorization; this is not a general vertex-minimum theorem.
- In general dimension, an explicit sufficient one-sided logarithmic radius and an equal-degree covariance-difference local sufficient/obstructing test. The radius is not claimed sharp, and a zero covariance difference remains undecided.

The comparison uses the reference value at 1. It asserts a minimum at 1 only when 1 belongs to the interval. No ratio is evaluated at zero or infinity. The N=2 theorem does not classify intervals whose closure excludes 1; the special N=3 theorem covers every nonempty positive interval.

## Reading order

1. PROOF.md retains every original mathematical paragraph, all equations (1)-(17), and the complete written proofs.
2. AUDIT.md retains the full independent mathematical audit, including the analytic shape arguments, exact Bernstein certificate, equality cases, local radius and covariance justification.
3. ACCEPTANCE.md and ACCEPTANCE.json state the exact acceptance and exclusion boundaries. No correction patch was required.
4. SOURCES.json records public source identities and historical inspection scope for both the candidate and audit. VERIFICATION.json describes the historical finite checks and byte authentication without distributing raw computational outputs.
5. MANIFEST.json lists exactly eight files and hashes the other seven; its own hash is independently pinned in the publication description.

## Source scope

The original AIM Problem 1.45 was read in the retained archived page after the direct page returned HTTP 502. Khare–Tao's Theorem 10.1 proof and reciprocal conclusion on PDF pages 51-54 were inspected; their necessity argument uses unbounded scaling and cannot simply be transferred to a fixed finite box. The later strict-monotonicity paper's statements and the Jack/Macdonald paper's introduction were inspected only within the recorded limits. No whole-paper audit or exhaustive literature search is claimed.

- AIM statement: http://aimpl.org/totalpos/1/
- Archived statement: https://web.archive.org/web/20230414041754id_/http://aimpl.org/totalpos/1/
- Khare–Tao: https://arxiv.org/abs/1708.05197v6
- Belton–Guillot–Khare–Putinar: https://arxiv.org/abs/2310.18020
- Chen–Khare–Sahi: https://arxiv.org/abs/2509.19649
