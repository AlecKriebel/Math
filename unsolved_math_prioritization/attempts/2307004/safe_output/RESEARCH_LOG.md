# Five-approach research log

Problem 2307004 / AMR-022-7004. All timestamps UTC, 2026-10-05. Checkpoint times describe the investigation sequence; tool calls are not separately counted as research turns. Completion estimates concern a fully rigorous sharp-constant solution and are subjective planning estimates, not evidence or calibrated probabilities.

## Readiness, 07:14-07:18

Started with the specified UnsolvedMath URL; web retrieval was unavailable and direct retrieval returned HTTP 403. Read the live rank-688 queue row (queued 0/5), current repository state, compact catalog descriptor, provenance manifest and actual attempts listing. Read-only PR, commit, branch and indexed-code searches found no matching prior target; broader Turán/Atkinson PR matches were inspected and concerned unrelated work. No original selected AI report was available. No inference of prior-report validity was made.

Fresh Hayman-Lingham PDF retrieval matched the earlier cached PDF hash. Visually inspected printed page 161 / PDF page 162, including definition of S_k immediately before Problem 7.4 and the complete Problem/Update. Confirmed arbitrary complex entries, fixed z_1=1, variable n, exponent window 1,...,n and strict inequality.

Literature immediately showed the recorded 1/3 bound is obsolete: Biró's two 2000 papers provide a uniform improvement beyond 1/2 and asymptotic upper bounds. Their full author-hosted PDFs were obtained. This changed the novelty standard before any attempt was promoted.

## Approach 1: low-dimensional exact minimax, checkpoint 07:20

Mechanism: use w=1+z_2 and complete a square in Re(w), |w|^2. Proved the full complex two-point optimum sqrt(3-sqrt(5)) with an explicit attaining configuration inside the disc. Independently established fixed-n normalization equivalence by scaling a largest-modulus root.

Evidence: PROOF.md Sections 1-2; exact polynomial and quadratic-field controls in verify_exact.py.

Result: complete n=2 theorem, partial only. Gap: no uniform lower bound or control of the infimum over unbounded n. Restricting to real roots would discard the minimizer. Estimated exact-target completion: 5%.

## Approach 2: coefficient-phase induction, checkpoint 07:22

Mechanism: use the fixed-root Newton recurrence, a disc centered at the preceding partial coefficient sum, and an invariant comparing that sum with the sum of coefficient moduli. Obtained a self-contained proof that M_n>1/2 for every n.

Evidence: PROOF.md Section 3; exact recurrence checks on rational root tuples. The result and mechanism are classical and credited, not new.

Result: universal bound recovered. Derived the exact barrier q^2<=gamma^2(1-gamma^2)<=1/4 for the proposed scalar invariant, so merely optimizing its cone angle cannot reach q>1/2. Biró's published improvement uses additional identities. Gap: uniform phase information beyond this invariant. Estimated exact-target completion: 8%.

## Approach 3: positive coefficient majorants, checkpoint 07:23

Mechanism: dominate elementary coefficients using the formal exponential of the first n moments. Derived prod_{k=1}^n(1+M/k)>=2 from the fixed root, and M>=1 for the exterior-modulus class from the constant coefficient. Separately solved the real-root restriction using S_2 positivity.

Evidence: PROOF.md Section 4; exact majorant product identities and unit-root construction in the proof.

Result: sharp restricted-class bounds and a rigorous degree-dependent estimate. Gap: the latter tends to zero and loses essential complex cancellation. The exterior/real restrictions are not the original target. Estimated exact-target completion: 8%.

## Approach 4: inverse moment algebra, checkpoint 07:24

Mechanism: replace root variables by proposed first n power sums and invert Newton recurrence. Proved that the single polynomial condition b_n=0 is necessary and sufficient, including lower-degree Q and zero-root cases. Tested the constant complex moment ansatz exactly; its only zeros are u=1,...,n.

Evidence: PROOF.md Section 5; 39 exact root/moment roundtrips, constant-moment factorization controls and a perturbed-moment negative control.

Result: a checkable equivalent extremal formulation and a fully rejected special construction. Gap: proving the sharp zero-free polydisc transfers, rather than solves, the original extremal difficulty. Estimated exact-target completion: 10%.

## Approach 5: two-block cancellation, checkpoint 07:28

Mechanism: keep the first floor(n/2) moments constant and exploit the exact linearity of coefficient n in higher moments. A finite two-parameter exploratory search was used only to propose coefficients; no large exhaustive search was performed. Converted one n=32 proposal to an exact rational certificate, correcting its final moment algebraically.

Evidence: PROOF.md Section 6, CERTIFICATE.json, exact_core.py, verify_exact.py and VERIFICATION.json. The certificate proves every norm is strictly below 29/40 and a recovered monic polynomial has root 1. The two-block mechanism is credited to Biró. The finite certificate is weaker than published bounds.

Result: certified finite upper control, not a global lower bound or sharp asymptotic result. Optional n<=128 floating exploration is non-certifying. Gap: no matching lower bound, no limit theorem, no endpoint determination. Estimated exact-target completion: 10%.

## Freeze, 07:30

Five approaches exhausted; no candidate full solution. The safe artifact is complete for review. A fresh independent audit must precede any remote write. The investigation made no remote changes and contacted no outside researcher.

The unresolved target must not be marked solved, and the five-turn budget must not be reset by calling the partial results a new attempt. New research would need a materially new mechanism and appropriate authorization.
